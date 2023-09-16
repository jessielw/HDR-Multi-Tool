const {
    app,
    BrowserWindow,
    ipcMain
  } = require("electron");
const path = require("path");
  // const fsPromises = require("fs").promises
  // const MediaInfoFactory = require('mediainfo.js').default;
const parseMediaInfo = require("./app/main/mediaInfoParser.js");
const { getPathObject, changeFileExtension } = require("./app/main/fileUtils.js");

  const devMode = true;
  
  // Keep a global reference of the window object, if you don't, the window will
  // be closed automatically when the JavaScript object is garbage collected.
  let root;
  
  async function createWindow() {

  let rootWidth = 675
  if (devMode) {
    rootWidth = rootWidth + 300
  }
  
    // Create the browser window.
    root = new BrowserWindow({
      width: rootWidth,
      height: 350,
      webPreferences: {
        sandbox: true,
        contextIsolation: true,
        preload: path.join(__dirname, '/app/preload/preload.js'),
      }      
    });
  
    // Load app
    root.loadFile(path.join(__dirname, "/app/renderer/index.html"));

    // Open the DevTools.
    if (devMode) {root.webContents.openDevTools()} 
  
    // rest of code..
    ipcMain.handle('open-file', async (event, filePath) => {
      console.log('triggered event');
      // console.log(event);
      // console.log(filePath);
      try {
        let test = await parseMediaInfo(filePath);
        console.log(typeof(test));
        return test;

      // Send the 'test' result back to the renderer process
      root.webContents.send('media-analysis-result', test);   

      } catch (error) {
        throw error.message;
      }
    });  
    
    // get file object
    ipcMain.handle('get-path-object', async (event, fileInput) => {
      const pathObject = getPathObject(fileInput);
      return pathObject;
    });

    // change file extension
    ipcMain.handle('change-extension', async (event, fileInput, ext) => {
      const newPathObject = changeFileExtension(fileInput, ext);
      return newPathObject;
    });    
  }
  
  app.on("ready", createWindow);
  

// const analyzeMedia = async (fileInput) => {
//   const file = path.normalize(fileInput);
//   console.log(file);
//   //const file = "C:/Users/jlw_4/OneDrive/Desktop/testing/Revolutionary Road 2008 Hybrid 2160p WEB-DL TrueHD 5.1 DoVi HDR10plus HEVC.mkv"; // Replace with your file path
//   const format = 'JSON'; // Specify the desired format
//   const coverData = true; // Set to true if you want to extract cover data
//   const full = true; // Set to true for full information display

//   let fileHandle;
//   let fileSize;
//   let mediainfo;

//   let results;

//   const readChunk = async (size, offset) => {
//     if (!fileHandle) throw new Error('File unavailable');
//     const buffer = new Uint8Array(size);
//     await fileHandle.read(buffer, 0, size, offset);
//     return buffer;
//   };

//   try {
//     fileHandle = await fsPromises.open(file, 'r');
//     fileSize = (await fileHandle.stat()).size;
//     mediainfo = await MediaInfoFactory({ format, coverData, full });

//     if (!mediainfo) {
//       throw new Error('Failed to initialize MediaInfo');
//     }

//     const result = await mediainfo.analyzeData(() => fileSize, readChunk);
//     // console.log(result);
//     // return result;
//     results = result;
//   } finally {
//     if (fileHandle) await fileHandle.close();
//     if (mediainfo) mediainfo.close();
//   }
//   // console.log(results);
//   return results;
// };


//   // Create an listener for the event "A"
//   ipcMain.on("A", (event, args) => {
      
//     // Send result back to renderer process
//     root.webContents.send("D", {success: true});
//   });
