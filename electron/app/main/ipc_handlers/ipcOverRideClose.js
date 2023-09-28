const { dialog, ipcMain } = require("electron");

let allowedClose = false;

module.exports = (root) => {
  root.on("close", async (event) => {
    if (!allowedClose) {
      event.preventDefault();
      root.send("safe-to-close-app");
    }
  });

  ipcMain.on("respond:safe-to-close-app", (_, safeToClose) => {
    if (!safeToClose) {
      dialog
        .showMessageBox(root, {
          type: "question",
          buttons: ["Yes", "No"],
          title: "Exit",
          message:
            "Are you sure you want to quit while jobs are currently processing?",
        })
        .then((choice) => {
          if (choice.response === 0) {
            allowedClose = true;
            root.close();
          }
        })
        .catch((error) => {
          console.error(error);
        });
    } else {
      allowedClose = true;
      root.close();
    }
  });
};
