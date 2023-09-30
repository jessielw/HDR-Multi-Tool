const path = require("path");
const fsPromises = require("fs").promises;
const MediaInfoFactory = require("mediainfo.js").default;

const parseMediaInfo = async (fileInput) => {
  const file = path.normalize(fileInput);
  // Specify the desired format
  const format = "object";
  // Set to true if you want to extract cover data
  const coverData = false;
  // Set to true for full information display
  const full = true;

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
    results = result;
  } finally {
    if (fileHandle) await fileHandle.close();
    if (mediaInfo) mediaInfo.close();
  }
  return results;
};

module.exports = parseMediaInfo;
