const path = require("path");

const getPathObject = function (file) {
  return {
    dirName: path.normalize(path.dirname(file)),
    path: path.normalize(path.resolve(file)),
    baseName: path.basename(file),
    ext: path.extname(file),
  };
};

const changeFileExtension = function (filePath, ext) {
  const basename = path.basename(filePath, path.extname(filePath));
  const modifiedPath = path.join(path.dirname(filePath), basename + ext);
  return {
    dirName: path.normalize(path.dirname(modifiedPath)),
    path: path.normalize(path.resolve(modifiedPath)),
    baseName: path.basename(modifiedPath),
    ext: path.extname(modifiedPath),
  };
};

module.exports = { getPathObject, changeFileExtension };
