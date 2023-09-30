const path = require("path");
const { app } = require("electron");

let rootDir;

// determine root directory (where main.js would be)
if (app.isPackaged) {
  // bundled app
  rootDir = path.dirname(process.execPath);
} else {
  // development
  rootDir = path.resolve(__dirname, "../../");
}

module.exports = rootDir;
