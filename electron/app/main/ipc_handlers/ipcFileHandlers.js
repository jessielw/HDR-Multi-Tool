const { ipcMain, dialog } = require("electron");

// Handle the "show-open-dialog" event from the renderer process
ipcMain.on("show-open-dialog", async (event) => {
  const result = await showOpenDialog(event.sender);
  event.sender.send("return-open-dialog", result.filePaths);
});

// Function to show the open dialog
async function showOpenDialog(window) {
  const result = await dialog.showOpenDialog(window, {
    properties: ["openFile"],
    filters: [
      { name: "Media Files", extensions: ["mp4", "mkv", "hevc", "ts"] },
    ],
  });
  return result;
}

// Export the showOpenDialog function for use in other modules
module.exports = { showOpenDialog };
