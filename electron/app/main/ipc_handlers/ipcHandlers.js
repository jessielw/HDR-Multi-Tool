const { ipcMain, dialog } = require("electron");
const parseMediaInfo = require("../../../app/main/mediaInfoParser.js");
const { toolPathObject } = require("../../../app/main/detectFilePaths.js");
const {
  getPathObject,
  changeFileExtension,
} = require("../../../app/main/fileUtils.js");

ipcMain.handle("open-file", async (_, filePath) => {
  try {
    const parsedMediaInfo = await parseMediaInfo(filePath);
    return parsedMediaInfo;
  } catch (error) {
    throw error.message;
  }
});

ipcMain.on("show-save-dialog", (event, args) => {
  let saveFilters = [{ name: "HDR", extensions: args.outputExtension }];
  if (args.allFiles) {
    saveFilters.push({ name: "All Files", extensions: ["*"] });
  }

  const setSavePath = getPathObject(args.defaultPath);
  const options = {
    defaultPath: setSavePath.baseNameNoExt,
    filters: saveFilters,
  };

  dialog
    .showSaveDialog(options)
    .then((result) => {
      if (!result.canceled) {
        event.reply("save-dialog-success", {
          filePath: getPathObject(result.filePath),
        });
      } else {
        event.reply("save-dialog-cancel");
      }
    })
    .catch((err) => {
      console.error(err);
      event.reply("save-dialog-error", err.message);
    });
});

// get file object
ipcMain.handle("get-path-object", async (_, fileInput) => {
  const pathObject = getPathObject(fileInput);
  return pathObject;
});

// change file extension
ipcMain.handle("change-extension", async (_, fileInput, ext) => {
  const newPathObject = changeFileExtension(fileInput, ext);
  return newPathObject;
});

ipcMain.handle("get-tool-paths", () => {
  return toolPathObject;
});

ipcMain.on("show-message-prompt", (event, args) => {
  dialog
    .showMessageBox({
      title: args[0],
      message: args[1],
      // You can add other options here if needed
    })
    .then((response) => {
      event.reply("message-box-response", response);
    });
});

function showMessagePrompt(args, event) {
  dialog
    .showMessageBox({
      title: args[0],
      message: args[1],
    })
    .then((response) => {
      if (event) {
        event.reply("message-box-response", response);
      }
    })
    .catch((error) => {
      console.error("Error showing message box:", error);
    });
}

ipcMain.on("show-message-prompt", (event, args) => {
  showMessagePrompt(args, event);
});

module.exports = { showMessagePrompt };
