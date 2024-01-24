const { ipcMain } = require("electron");
const { spawn } = require("child_process");
const {
  logProgress,
  cleanupOldLogFiles,
} = require("../../../app/main/logToFile");
const path = require("path");
const createConfigStore = require("../../../app/main/configUtils.js");
const fs = require("fs");
// const getFileObject = require("../../../app/main/fileUtils").changeFileExtension;

// function convertFFmpegToPercent(line, durationInSeconds) {
//   if (line.includes("time=-")) {
//     return "0%";
//   } else {
//     const timeMatch = line.match(/time=(\d+):(\d+):(\d+)\.(\d+)/);
//     if (timeMatch) {
//       const hours = parseInt(timeMatch[1]);
//       const minutes = parseInt(timeMatch[2]);
//       const seconds = parseInt(timeMatch[3]);
//       const totalMilliseconds =
//         hours * 3600000 + minutes * 60000 + seconds * 1000;
//       const progress = (totalMilliseconds / (durationInSeconds * 1000)) * 100;
//       const percent = `${progress.toFixed(1)}%`;
//       return percent;
//     }
//   }
// }

function convertFFmpegFrameCountToPercent(line, totalFrames) {
  if (line.includes("frame=")) {
    const frameMatch = line.match(/frame=(\d+)/);
    if (frameMatch) {
      const currentFrame = parseInt(frameMatch[1]);
      const progress = (currentFrame / totalFrames) * 100;
      const percent = progress.toFixed(1);
      return percent;
    }
  }
  return 0;
}

function checkValidOutput(filePath, root) {
  const getSize = fs.statSync(filePath).size;
  if (getSize == 0) {
    root.webContents.send("invalid-output", filePath);
  }
}

module.exports = (root) => {
  let currentJob = 0;
  const jobQueue = { uncompleted: [], failed: [], inProgress: [] };
  let pauseJob = false;
  let queueInProgress = false;

  ipcMain.handle("add-job", async (_, args) => {
    currentJob = currentJob++;

    const modifiedJobCommand = {
      currentJob: currentJob,
      fileName: args.fileName,
      outputPath: args.outputPath,
      pipe1: args.pipe1,
      pipe2: args.pipe2,
      // duration: args.duration,
      frameCount: args.frameCount,
    };
    jobQueue.uncompleted.push(modifiedJobCommand);

    return { currentJob: currentJob, jobName: args.fileName };
  });

  ipcMain.on("start-queue", async () => {
    pauseJob = false;

    if (!queueInProgress) {
      queueInProgress = true;
      await processJobs();
      queueInProgress = false;
      root.webContents.send("hide-progress-bar");
    }
  });

  ipcMain.on("remove-job-from-queue", (_, job) => {
    // get only the job number
    const currentJobToRemove = Number(job.split("job-id-")[1]);

    // find the index of the item with the specified currentJob value
    const indexToRemove = jobQueue.uncompleted.findIndex(
      (job) => job.currentJob === currentJobToRemove
    );

    if (indexToRemove !== -1) {
      // remove the item at the found index
      jobQueue.uncompleted.splice(indexToRemove, 1);
    } else {
      // handle the case where the item with the specified currentJob value was not found
      // TODO decide if we want to do anything further here
      console.log(`Item with currentJob ${currentJobToRemove} not found.`);
    }
  });

  ipcMain.on("pause-queue", () => {
    pauseJob = true;
  });

  async function processJobs() {
    while (jobQueue.uncompleted.length > 0) {
      // check to ensure queue isn't paused
      if (pauseJob) {
        return;
      }

      // Get the next job
      const job = jobQueue.uncompleted.shift();

      // Move it to inProgress
      jobQueue.inProgress.push(job);

      // Update current selected job in the UI
      await root.send("job-update-current", job);

      // Process the job asynchronously
      await processJob(job);

      // Remove the job from inProgress and remove it from the UI
      const jobIndex = jobQueue.inProgress.indexOf(job);
      if (jobIndex !== -1) {
        jobQueue.inProgress.splice(jobIndex, 1);
        await root.send("job-complete-current", job);
      }
    }
    currentJob = 0;
    root.send("job-complete");
    // TODO check if there are jobs that failed and maybe don't send job complete to
    // close the panel
  }

  async function processJob(job) {
    const ffmpegProcess = spawn(job.pipe1[0], job.pipe1.slice(1));
    const hdrProcess = spawn(job.pipe2[0], job.pipe2.slice(1));
    // const duration = job.duration;
    const frameCount = job.frameCount;
    let complete = false;
    const currentJobTimeStamp = new Date()
      .toISOString()
      .replace(/:/g, "-")
      .replace(/\./g, "_")
      .replace(/T/g, " ")
      .replace(/Z/g, "_");

    // log path
    const logPath = path.join(
      root.logDirectory,
      `${currentJobTimeStamp}_${path.parse(job.fileName).name}.log`
    );

    // pipe hdr tool outputs to log
    hdrProcess.stderr.on("data", (data) => {
      const dataToString = data.toString();
      logProgress(logPath, "HDR Tool", dataToString);
    });
    hdrProcess.stdout.on("data", (data) => {
      const dataToString = data.toString();
      logProgress(logPath, "HDR Tool", dataToString);
    });

    // pipe ffmpeg to hdr tool
    ffmpegProcess.stdout.pipe(hdrProcess.stdin);

    // process ffmpeg output
    ffmpegProcess.stderr.on("data", (data) => {
      // const progress = convertFFmpegToPercent(data.toString(), duration);
      const dataToString = data.toString();
      logProgress(logPath, "FFMPEG", dataToString);
      const progress = convertFFmpegFrameCountToPercent(
        dataToString,
        frameCount
      );

      if (progress && progress < 99.9) {
        root.webContents.send("update-job-progress", progress);
      } else if (progress && parseInt(progress) == 100) {
        root.webContents.send("update-job-progress", progress);
        complete = true;
      }
    });

    // Wait for the hdrProcess to complete
    await new Promise((resolve) => {
      hdrProcess.on("close", (exitCode) => {
        if (complete) {
          checkValidOutput(job.outputPath, root);
          root.webContents.send("reset-job-progress");
        }
        resolve();
      });
    });

    // clean up log files
    cleanupOldLogFiles(root.logDirectory);
  }
};

ipcMain.handle("auto-start-job", async () => {
  return createConfigStore().get("autoStart");
});
