/**
 * Created by mongolrgata
 */

/**
 * @param {string|*} binaryString
 * @constructor
 */
function BinaryFile(binaryString) {
    this._currentPosition = 0;
    this._data = binaryString;
}

/**
 * @param {Number} offset
 */
BinaryFile.prototype.seekCur = function seekCur(offset) {
    this._currentPosition += offset;
};

/**
 * @param {Number} size
 * @returns {string}
 */
BinaryFile.prototype.read = function read(size) {
    var result = this._data.slice(this._currentPosition, this._currentPosition + size);

    this._currentPosition += size;

    return result;
};

/**
 * @returns {Number}
 */
BinaryFile.prototype.readUnsignedInt32 = function readUnsignedInt32() {
    var dWord = this.read(4);
    var result = 0;

    for (var i = 0, shift = 0; i < 4; ++i, shift += 8) {
        result += dWord.charCodeAt(i) << shift;
    }

    return result >>> 0;
};
