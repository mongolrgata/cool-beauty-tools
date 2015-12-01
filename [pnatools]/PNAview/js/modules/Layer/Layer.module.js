/**
 * Created by mongolrgata
 */

define([], function () {
    /**
     * @constructor
     */
    var Layer = function Layer() {
    };

    /**
     * @param {number} zIndex
     */
    Layer.prototype.setZIndex = function setZIndex(zIndex) {
        //noinspection JSUnusedGlobalSymbols
        this.zIndex = zIndex;
    };

    /**
     * @param {number} left
     */
    Layer.prototype.setLeft = function setLeft(left) {
        this.left = left;
    };

    /**
     * @param {number} top
     */
    Layer.prototype.setTop = function setTop(top) {
        this.top = top;
    };

    /**
     * @param {number} width
     */
    Layer.prototype.setWidth = function setWidth(width) {
        this.width = width;
    };

    /**
     * @param {number} height
     */
    Layer.prototype.setHeight = function setHeight(height) {
        this.height = height;
    };

    /**
     * @param {string} backgroundImage
     */
    Layer.prototype.setBackgroundImage = function setBackgroundImage(backgroundImage) {
        //noinspection JSUnusedGlobalSymbols
        this.backgroundImage = backgroundImage;
    };

    /**
     * @returns {Object}
     */
    Layer.prototype.getCSS = function getCSS() {
        var result = {};

        for (var key in this) {
            if (this.hasOwnProperty(key)) {
                result[key] = this[key];
            }
        }

        return result;
    };

    return Layer;
});
