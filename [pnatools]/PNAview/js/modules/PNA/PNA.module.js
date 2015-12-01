/**
 * Created by mongolrgata
 */

define(['Layer'], function (Layer) {
    /**
     * @param {BinaryFile} binaryFile
     * @constructor
     */
    var PNA = function PNA(binaryFile) {
        binaryFile.seekCur(4); // [50 4E 41 50]
        binaryFile.seekCur(4); // [XX XX XX XX]

        this._imageWidth = binaryFile.readUnsignedInt32();
        this._imageHeight = binaryFile.readUnsignedInt32();
        this._layers = [];

        var layerCount = binaryFile.readUnsignedInt32();
        var sizes = [];

        for (var i = 0; i < layerCount; ++i) {
            binaryFile.seekCur(4); // [00 00 00 00]

            this._layers[i] = new Layer();
            this._layers[i].setZIndex(binaryFile.readUnsignedInt32());
            this._layers[i].setLeft(binaryFile.readUnsignedInt32());
            this._layers[i].setTop(binaryFile.readUnsignedInt32());
            this._layers[i].setWidth(binaryFile.readUnsignedInt32());
            this._layers[i].setHeight(binaryFile.readUnsignedInt32());

            binaryFile.seekCur(4); // [00 00 00 00]
            binaryFile.seekCur(4); // [00 00 00 00]
            binaryFile.seekCur(4); // [00 00 F0 3F]

            sizes.push(binaryFile.readUnsignedInt32());
        }

        for (i = 0; i < layerCount; ++i) {
            this._layers[i].setBackgroundImage(['url(data:image/png;base64,', btoa(binaryFile.read(sizes[i])), ')'].join(''));
        }
    };

    PNA.prototype.getImageWidth = function getImageWidth() {
        return this._imageWidth;
    };

    PNA.prototype.getImageHeight = function getImageHeight() {
        return this._imageHeight;
    };

    PNA.prototype.getLayers = function getLayers() {
        return this._layers;
    };

    return PNA;
});
