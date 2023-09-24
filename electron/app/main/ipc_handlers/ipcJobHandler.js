const { app, BrowserWindow, ipcMain, dialog } = require("electron");
const curPlatform = require("os").platform();
const { spawn } = require("child_process");

module.exports = (root) => {
  // job control
  let currentJob = 0;
  const jobQueue = { uncompleted: [], failed: [], inProgress: [] };

  function combinedPipes(data) {
    console.log(data);
  }

  ipcMain.handle("add-job", async (_, args) => {
    // TODO handle linux

    // update current job
    currentJob++;

    if (curPlatform === "win32") {
      args.command.unshift("/c");
      const modifiedJobCommand = {
        currentJob: currentJob,
        fileName: args.fileName,
        osShell: "cmd",
        command: args.command,
      };
      jobQueue.uncompleted.push(modifiedJobCommand);
    }

    return { currentJob: currentJob, jobName: args.fileName };
  });

  ipcMain.on("start-queue", async () => {
    await processJobs();
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

  async function processJobs() {
    while (jobQueue.uncompleted.length > 0) {
      const job = jobQueue.uncompleted.shift(); // Get the next job
      jobQueue.inProgress.push(job); // Move it to inProgress

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

    // TODO: Send a signal to the renderer to re-enable buttons or perform other actions
  }

  async function processJob(job) {
    // console.log(job);
    const childProcess = spawn(job.osShell, job.command);

    childProcess.stdout.setEncoding("utf-8");
    childProcess.stdout.on("data", (data) => {
      combinedPipes(data);
    });

    childProcess.stderr.setEncoding("utf-8");
    childProcess.stderr.on("data", (data) => {
      combinedPipes(data);
    });

    // Wait for the child process to complete
    // TODO check if code was 0 or something else!
    await new Promise((resolve) => {
      childProcess.on("close", (code) => {
        console.log(`Child process exited with code ${code}`);
        resolve();
      });
    });
  }
};
