const fs = require("fs");
const path = require("path");

// TODO maybe allow user customizations later?
const maxLogs = 50;

// Function to log progress to the file
function logProgress(logFilePath, prefix, logData) {
  // Create a timestamp for the log entry
  const timestamp = new Date().toISOString();

  // Create the log entry with a timestamp and logData information
  const logEntry = `${prefix} ${timestamp}: ${logData}\n`;

  // Append the log entry to the log file
  fs.appendFile(logFilePath, logEntry, (err) => {
    if (err) {
      console.error(`Error writing to log file: ${err}`);
    }
  });
}

// Function to clean up older log files, keeping only the most recent `maxLogs` files
function cleanupOldLogFiles(logDirectory) {
  fs.readdir(logDirectory, (err, files) => {
    if (err) {
      console.error(`Error reading log directory: ${err}`);
      return;
    }

    // Sort files by modification time (oldest first)
    files = files
      .filter((file) => file.endsWith(".log")) // Filter only log files
      .map((file) => ({
        name: file,
        time: fs.statSync(path.join(logDirectory, file)).mtime,
      }))
      .sort((a, b) => a.time - b.time);

    // Delete older log files, keeping only the most recent `maxLogs` files
    const filesToDelete = files.slice(0, Math.max(files.length - maxLogs, 0));
    filesToDelete.forEach((file) => {
      const filePath = path.join(logDirectory, file.name);
      fs.unlinkSync(filePath);
      // console.log(`Deleted log file: ${filePath}`);
    });
  });
}

module.exports = { logProgress, cleanupOldLogFiles };
