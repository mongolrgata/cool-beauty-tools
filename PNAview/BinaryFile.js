/**
 * Created by mongolrgata
 */

/**
 * @param {string} binaryString
 * @constructor
 */
function BinaryFile(binaryString) {
    this._currentPosition = 0;
    this._data = binaryString;
}

/**
 * @param {number} offset
 */
BinaryFile.prototype.seekCur = function seekCur(offset) {
    this._currentPosition += offset;
};

/**
 * @param {number} length
 * @returns {string}
 */
BinaryFile.prototype.read = function read(length) {
    var result = this._data.slice(this._currentPosition, this._currentPosition + length);

    this._currentPosition += length;

    return result;
};

/**
 * @returns {number}
 */
BinaryFile.prototype.readUnsignedInt32 = function readUnsignedInt32() {
    var dWord = this.read(4);
    var result = 0;

    for (var i = 0, shift = 0; i < 4; ++i, shift += 8) {
        result += dWord.charCodeAt(i) << shift;
    }

    return result >>> 0;
};
