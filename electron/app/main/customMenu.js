const { app, Menu } = require("electron");
const {
  showOpenDialog,
} = require("../../app/main/ipc_handlers/ipcFileHandlers");

module.exports = (root) => {
  const template = [
    {
      label: "File",
      submenu: [
        {
          label: "Open",
          accelerator: "CmdOrCtrl+O",
          click: async () => {
            const fileInput = await showOpenDialog(root);
            root.webContents.send("return-open-dialog", fileInput.filePaths);
          },
        },
        {
          type: "separator",
        },
        {
          label: "Quit",
          accelerator: "CmdOrCtrl+Q",
          click: () => {
            app.quit();
          },
        },
      ],
    },
    // Add more menu items and submenus as needed
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
};
