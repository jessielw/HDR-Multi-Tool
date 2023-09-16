const path = require("path");
const fsPromises = require("fs").promises
const MediaInfoFactory = require('mediainfo.js').default;

const parseMediaInfo = async (fileInput) => {
  const file = path.normalize(fileInput);
  console.log(file);
  //const file = "C:/Users/jlw_4/OneDrive/Desktop/testing/Revolutionary Road 2008 Hybrid 2160p WEB-DL TrueHD 5.1 DoVi HDR10plus HEVC.mkv"; // Replace with your file path
  const format = "object"; // Specify the desired format
  const coverData = true; // Set to true if you want to extract cover data
  const full = true; // Set to true for full information display

  let fileHandle;
  let fileSize;
  let mediaInfo;

  let results;

  const readChunk = async (size, offset) => {
    if (!fileHandle) throw new Error("File unavailable");
    const buffer = new Uint8Array(size);
    await fileHandle.read(buffer, 0, size, offset);
    return buffer;
  };

  try {
    fileHandle = await fsPromises.open(file, "r");
    fileSize = (await fileHandle.stat()).size;
    mediaInfo = await MediaInfoFactory({ format, coverData, full });

    if (!mediaInfo) {
      throw new Error("Failed to initialize MediaInfo");
    }

    const result = await mediaInfo.analyzeData(() => fileSize, readChunk);
    // console.log(result);
    // return result;
    results = result;
  } finally {
    if (fileHandle) await fileHandle.close();
    if (mediaInfo) mediaInfo.close();
  }
  // console.log(results);
  return results;
};

module.exports = parseMediaInfo;
