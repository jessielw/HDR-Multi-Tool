const infoArea = document.getElementById("info-area-span");
const openFileBtn = document.getElementById("open-file");
const hiddenOpenFileBtn = document.getElementById("hidden-open-file");
const inputTextBox = document.getElementById("open-file-text-box");
const hdr10PlusCheckBox = document.getElementById("hdr10plus-check-box");
const dVCheckBox = document.getElementById("dv-check-box");
const outputTextBox = document.getElementById("save-file-text-box");
const startJobButton = document.getElementById("start-job-button");

// detect and define default colors
const defaultDropColor = openFileBtn.style.backgroundColor;
const defaultInfoColor = infoArea.style.color;

let mediaInfoObject;
let dolbyVision;
let hdr10Plus;
let invalidHdrSelection = false;
let inputPath;
let outputExt;
let outputPath;

function resetGui() {
  mediaInfoObject = undefined;
  dolbyVision = undefined;
  hdr10Plus = undefined;
  invalidHdrSelection = false;
  inputPath = undefined;
  outputExt = undefined;
  outputPath = undefined;
  inputTextBox.value = '';
  outputTextBox.value = '';
}

async function acceptInputFile(filePath) {
  // Ensure colors are reset back to defaults
  infoArea.style.color = defaultInfoColor;
  openFileBtn.style.backgroundColor = defaultDropColor;
  inputTextBox.style.backgroundColor = defaultDropColor;

  resetGui();

  try {
    const inputFileObject = await ipcRenderer.invoke(
      "get-path-object",
      filePath
    );
    const { dirName, path, baseName, ext } = inputFileObject;

    const supportedExtensions = [".mkv", ".mp4", ".hevc", ".ts"];

    if (!supportedExtensions.includes(ext)) {
      infoArea.innerText = "Input type is not supported";
      return;
    }

    const mediaInfoObjectParsed = await ipcRenderer.invoke(
      "open-file",
      filePath
    );
    mediaInfoObject = mediaInfoObjectParsed;

    const videoTrackObject = findVideoTrack(mediaInfoObject.media.track);

    if (!videoTrackObject) {
      infoArea.innerText = "Input does not have a video track";
      infoArea.style.color = "#e1401d";
      return;
    }

    // Update input var
    inputPath = path;

    // Update text box with file's base name
    inputTextBox.value = baseName; 

    const hdrString = getHdrString(videoTrackObject);

    if (!hdrString) {
      infoArea.innerText =
        "Video track does not contain HDR/Dolby Vision metadata";
    } else {
      infoArea.innerText = hdrString;
      infoArea.style.color = "#c0cbd3";

      const combinedHdrStrings = hdrString.toLowerCase();

      checkHdrTypes(combinedHdrStrings);

      // If input is only HDR10 and not HDR10+/Dolby Vision, let the user know
      if (!dolbyVision && !hdr10Plus) {
        infoArea.innerText = "Input is only HDR10, no parsing needed";
      }
    }

    if (dolbyVision) {
      dvTab.click();
      hdr10PlusCheckBox.checked = false;
      dVCheckBox.checked = true;
      outputExt = ".bin";
    } else if (hdr10Plus) {
      hdr10Tab.click();
      dVCheckBox.checked = false;
      hdr10PlusCheckBox.checked = true;
      outputExt = '.json';
    } 
    
    enableDisableStart();

  } catch (error) {
    console.error(error);
  }
}


// enable and disable opposing checkbox's
hdr10PlusCheckBox.addEventListener("change", function() {
  if (this.checked) {
    dVCheckBox.checked = false;

    if (hdr10Plus) {
      invalidHdrSelection = false;
    } else {
      invalidHdrSelection = true;
    }
  }
  outputExt = ".json";
  enableDisableStart();
})

dVCheckBox.addEventListener("change", function() {
  if (this.checked) {
    hdr10PlusCheckBox.checked = false;

    if (dolbyVision) {
      invalidHdrSelection = false;
    } else {
      invalidHdrSelection = true;
    }    
  }
  outputExt = ".bin";
  enableDisableStart();
})


async function enableDisableStart() {
  if (invalidHdrSelection) {
    infoArea.innerText =
      "Invalid HDR Selection for Input";    
    infoArea.style.color = "#e1401d";
  } else {
    
    if (outputExt) {
    try {
      const newOutput = await ipcRenderer.invoke(
        "change-extension",
        inputPath,
        outputExt
      );
      outputTextBox.value = newOutput.baseName;
      outputPath = newOutput.path;   
    } catch (error) {
      console.log(error);
    }
  }};

  if (inputPath && (hdr10PlusCheckBox.checked || dVCheckBox.checked) && !invalidHdrSelection && outputPath) {
    startJobButton.classList.remove("button-out-disabled");
  } else {
    startJobButton.classList.add("button-out-disabled");
  };
};

// loop to enable/disable start button as needed
// setInterval(function () {
//   if (inputPath && (hdr10PlusCheckBox.checked || dVCheckBox.checked) && !invalidHdrSelection) {
//     startJobButton.classList.remove("button-out-disabled");
//   } else {
//     startJobButton.classList.add("button-out-disabled");
//   }

//   if (invalidHdrSelection) {
//     infoArea.innerText =
//       "Invalid HDR Selection for Input";    
//     infoArea.style.color = "#e1401d";
//   }
// }, 100);

function findVideoTrack(trackArray) {
  return trackArray.find((track) => track["@type"] === "Video");
}

function getHdrString(videoTrackObject) {
  const hdrFormat = videoTrackObject.HDR_Format;
  const hdrFormatCommercial = videoTrackObject.HDR_Format_Commercial;

  if (hdrFormat || hdrFormatCommercial) {
    const separator = hdrFormat && hdrFormatCommercial ? " / " : "";
    return `${hdrFormat}${separator}${hdrFormatCommercial}`;
  }

  return null;
}

function checkHdrTypes(hdrString) {
  if (hdrString.includes("vision")) {
    dolbyVision = true;
  }
  if (hdrString.includes("hdr10+")) {
    hdr10Plus = true;
  }
}

openFileBtn.addEventListener("click", function () {
  hiddenOpenFileBtn.click();
});

hiddenOpenFileBtn.addEventListener("change", async function (event) {
  var filePath = event.target.files[0]["path"];
  acceptInputFile(filePath);
});

[openFileBtn, inputTextBox].forEach((dropArea) => {
  dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.backgroundColor = "#ccc";
  });

  // Handle the file drop event
  dropArea.addEventListener("drop", (e) => {
    e.preventDefault();

    const files = e.dataTransfer.files;

    if (files.length > 0) {
      const file = files[0].path;
      acceptInputFile(file);
    }
  });
});

// function updateOutputName(baseName, outputExt, dirName) {


//   let outPutPathName = baseName.slice(0, -4) + outputExt;
//   outputTextBox.value = outPutPathName;
//   outputPath = dirName + outPutPathName;  
//   console.log(outputPath);
// }

// notebook tabs
const notebookArea = document.getElementById("notebook-area");
const hdr10Tab = document.getElementById("hdr10-plus-tab");
const dvTab = document.getElementById("dv-tab");

const hdr10TabContent = document.getElementById("hdr10-plus-tab-content");
const dvTabContent = document.getElementById("dv-tab-content");


// var currentTab = hdr10Tab.id;


hdr10Tab.addEventListener("click", function () {
  dvTabContent.style.display = "none";
  dvTab.classList.remove("tab-swap");
  hdr10TabContent.style.display = "grid";
  hdr10Tab.classList.add("tab-swap");
  // currentTab = this.id;
});

dvTab.addEventListener("click", function () {
  hdr10TabContent.style.display = "none";
  hdr10Tab.classList.remove("tab-swap");
  dvTabContent.style.display = "grid";
  dvTab.classList.add("tab-swap");
  // currentTab = this.id;
});

