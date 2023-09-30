const electronStore = require("electron-store");
const path = require("path");
const baseDirectory = require("../../app/main/baseDirectory");

// set config default options
const defaultOptions = {
  autoStart: false,
};

// Define a function that initializes and returns the store instance
function createConfigStore() {
  return new electronStore({
    cwd: path.resolve(baseDirectory, "app_config"),
    defaults: defaultOptions,
  });
}

module.exports = createConfigStore;
