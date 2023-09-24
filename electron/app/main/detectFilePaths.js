const fs = require("fs");
const which = require("which");
const curPlatform = require("os").platform();
const path = require("path");

// tool paths (attempt to detect on PATH)
let doviToolPath = {
  name: "dovi_tool",
  path: which.sync("dovi_tool", { nothrow: true }),
};
let hdrToolPath = {
  name: "hdr10plus_tool",
  path: which.sync("hdr10plus", { nothrow: true }),
};
let ffmpegToolPath = {
  name: "FFMPEG",
  path: which.sync("ffmpeg", { nothrow: true }),
};

if (curPlatform === "win32") {
  if (!doviToolPath.path) {
    doviToolPath.path = path.resolve("apps/dovi_tool.exe");
  }
  if (!hdrToolPath.path) {
    hdrToolPath.path = path.resolve("apps/hdr10plus_tool.exe");
  }
  if (!ffmpegToolPath.path) {
    ffmpegToolPath.path = path.resolve("apps/ffmpeg.exe");
  }
} else {
  if (!doviToolPath.path) {
    doviToolPath.path = path.resolve("apps/dovi_tool");
  }
  if (!hdrToolPath.path) {
    hdrToolPath.path = path.resolve("apps/hdr10plus_tool");
  }
  if (!ffmpegToolPath.path) {
    ffmpegToolPath.path = path.resolve("apps/ffmpeg");
  }
}

const toolPathObject = {
  doviToolPath: doviToolPath.path,
  hdrToolPath: hdrToolPath.path,
  ffmpegToolPath: ffmpegToolPath.path,
};

async function checkDependencies() {
  for (const toolPath of [doviToolPath, hdrToolPath, ffmpegToolPath]) {
    const detectFile = fs.existsSync(toolPath.path);
    if (!detectFile) {
      const fileName = toolPath.name;
      return {
        success: false,
        message: `"${fileName}" is not detected.\n\nWe will be unable to process files without having "${fileName}" installed.\n\nInstall "${fileName}" on your system path or in the "apps" folder and relaunch`,
      };
    }
  }
  return { success: true };
}

module.exports = { checkDependencies, toolPathObject };
