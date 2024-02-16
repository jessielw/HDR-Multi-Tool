const fs = require("fs");
const { getPathObject } = require("./fileUtils");

function processDvJson(
  inputPath,
  mode,
  cropTop,
  cropBottom,
  cropLeft,
  cropRight,
  fixNegativeCrops,
  logProgressFunction
) {
  try {
    // Read the JSON file
    const jsonData = fs.readFileSync(inputPath, "utf8");
    const rpu_dict = JSON.parse(jsonData);
    rpu_dict.crop = true;
    const json_dict = { active_area: rpu_dict, mode: mode };
    const outputJsonPath = `${getPathObject(inputPath).pathNoExt}_cropped.json`;

    // Check if "presets" key exists
    const presets = json_dict.active_area.presets || [];
    if (presets.length === 0) {
      throw new Error("No 'presets' found in the JSON file");
    }

    for (let preset of presets) {
      let left = (preset.left || 0) - cropLeft;
      let right = (preset.right || 0) - cropRight;
      let top = (preset.top || 0) - cropTop;
      let bottom = (preset.bottom || 0) - cropBottom;

      if (fixNegativeCrops) {
        // Log fixed negative crop values
        const fixedValues = [];
        if (left < 0) {
          fixedValues.push(`left=${left}`);
          left = Math.max(0, left);
        }
        if (right < 0) {
          fixedValues.push(`right=${right}`);
          right = Math.max(0, right);
        }
        if (top < 0) {
          fixedValues.push(`top=${top}`);
          top = Math.max(0, top);
        }
        if (bottom < 0) {
          fixedValues.push(`bottom=${bottom}`);
          bottom = Math.max(0, bottom);
        }

        if (fixedValues.length > 0) {
          logProgressFunction(
            `Negative crop values were detected for presets, but were fixed automatically: ${fixedValues.join(
              ", "
            )}`
          );
        }
      } else {
        // If fixNegativeCrops is disabled, check for negative crop values
        const negativeValues = [];
        if (left < 0) negativeValues.push(`left=${left}`);
        if (right < 0) negativeValues.push(`right=${right}`);
        if (top < 0) negativeValues.push(`top=${top}`);
        if (bottom < 0) negativeValues.push(`bottom=${bottom}`);

        // If any negative values are found, throw an error
        if (negativeValues.length > 0) {
          throw new Error(
            `Negative crop values are not allowed for presets: ${negativeValues.join(
              ", "
            )}`
          );
        }
      }

      // Update preset values
      preset.left = left;
      preset.right = right;
      preset.top = top;
      preset.bottom = bottom;
    }

    // Write the JSON to the output file
    fs.writeFileSync(
      outputJsonPath,
      JSON.stringify(json_dict, null, 2),
      "utf-8"
    );

    return outputJsonPath;
  } catch (error) {
    throw new Error(
      `Error processing JSON file '${inputPath}': ${error.message}`
    );
  }
}

module.exports = { processDvJson };
