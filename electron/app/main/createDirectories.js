const path = require("path");
const fs = require("fs").promises;
const { dialog } = require("electron");

async function createLogDir(baseDir) {
  // create logging directory
  const logDirectory = path.join(baseDir, "/logs");
  fs.mkdir(logDirectory)
    .then(() => {
      // console.log(`Directory ${logDirectory} created successfully`);
    })
    .catch((error) => {
      if (error.code === "EEXIST") {
        // console.log(`Directory ${logDirectory} already exists`);
      } else {
        dialog.showMessageBox({
          title: "Error",
          message: "Error creating directory: ${error.message}",
        });
      }
    });
  return logDirectory;
}

module.exports = createLogDir;
