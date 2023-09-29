const path = require("path");
const fs = require("fs").promises;
const { dialog } = require("electron");

async function createLogDir(baseDir) {
  const logDirectory = path.join(baseDir, "logs");

  try {
    await fs.mkdir(logDirectory, { recursive: true });
    return logDirectory;
  } catch (error) {
    if (error.code === "EEXIST") {
      return logDirectory;
    } else {
      // Only show an error dialog for unexpected errors
      if (error.code !== "ENOENT") {
        dialog.showErrorBox(
          "Error Creating Directory",
          `Error creating directory: ${error.message}`
        );
      }
      return null;
    }
  }
}

module.exports = createLogDir;
