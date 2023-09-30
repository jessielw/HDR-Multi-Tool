const { app, BrowserWindow, dialog } = require("electron");
const path = require("path");
const { checkDependencies } = require("./app/main/detectFilePaths.js");
const createLogDir = require("./app/main/createDirectories.js");
const os = require("os");

// get the operating system [darwin, win32, linux]
const curPlatform = os.platform();

// keep a global variable for root
let root;

async function createWindow() {
  // Create the browser window.
  root = new BrowserWindow({
    width: 700,
    height: 380,
    webPreferences: {
      sandbox: true,
      contextIsolation: true,
      preload: path.join(__dirname, "/app/preload/preload.js"),
    },
    icon: path.join(__dirname, "/app/images/hdr.ico"),
    backgroundColor: "#2c313a",
  });

  // Event listeners on the window
  root.webContents.on("did-finish-load", async () => {
    root.show();
    root.focus();
    const dependenciesPresent = await checkDependencies();
    if (!dependenciesPresent.success) {
      dialog.showErrorBox("", dependenciesPresent.message);
      app.exit();
    }
  });

  const getLogDirectory = await createLogDir();

  // add vars to root object as needed
  root.logDirectory = getLogDirectory;

  // customize menu bar
  require("./app/main/customMenu.js")(root);

  // Load app
  root.loadFile(path.join(__dirname, "/app/renderer/index.html"));

  // Open the DevTools.
  if (!app.isPackaged) {
    root.webContents.openDevTools();
  }

  require("./app/main/ipc_handlers/ipcFileHandlers.js");
  require("./app/main/ipc_handlers/ipcHandlers.js");
  require("./app/main/ipc_handlers/ipcJobHandler.js")(root);
  if (app.isPackaged) {
    require("./app/main/ipc_handlers/ipcOverRideClose.js")(root);
  }
}

app.whenReady().then(() => {
  createWindow();
});
