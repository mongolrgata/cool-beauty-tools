/**
 * Created by mongolrgata
 */

/**
 * @param {BinaryFile} binaryFile
 * @constructor
 */
function PNA(binaryFile) {
    binaryFile.seekCur(4); // [50 4E 41 50]
    binaryFile.seekCur(4); // [XX XX XX XX]

    this.imageWidth = binaryFile.readUnsignedInt32();
    this.imageHeight = binaryFile.readUnsignedInt32();
    this.layers = new Array(binaryFile.readUnsignedInt32());

    for (var i = 0, n = this.layers.length; i < n; ++i) {
        var layer = this.layers[i] = {};

        binaryFile.seekCur(4); // [00 00 00 00]

        layer.zIndex = binaryFile.readUnsignedInt32();
        layer.offsetLeft = binaryFile.readUnsignedInt32();
        layer.offsetTop = binaryFile.readUnsignedInt32();
        layer.layerWidth = binaryFile.readUnsignedInt32();
        layer.layerHeight = binaryFile.readUnsignedInt32();

        binaryFile.seekCur(4); // [00 00 00 00]
        binaryFile.seekCur(4); // [00 00 00 00]
        binaryFile.seekCur(4); // [00 00 F0 3F]

        layer.size = binaryFile.readUnsignedInt32();
    }

    this.layers.forEach(function (layer) {
        layer.pngData = binaryFile.read(layer.size);
    });
}

/**
 * @returns {Number}
 */
PNA.prototype.layersCount = function layersCount() {
    return this.layers.length;
};

/**
 * @param {Number} index
 * @returns {string}
 */
PNA.prototype.getSrcProperty = function getSrcProperty(index) {
    return 'data:image/png;base64,' + btoa(this.layers[index].pngData);
};
