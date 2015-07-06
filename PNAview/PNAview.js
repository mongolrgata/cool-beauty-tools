/**
 * Created by mongolrgata
 */

$(document).ready(function () {
    var $layerInfoTemplate = $([
        '<tr class="layer-info">                             ',
        '   <td><input type="checkbox"></td>                 ',
        '   <td><div class="preview"></div></td>             ',
        '   <td align="right"><span class="layer-width"></td>',
        '   <td>&#x2715;</td>                                ',
        '   <td align="left"><span class="layer-height"></td>',
        '   <td><span class="offset-left"></td>              ',
        '   <td><span class="offset-top"></td>               ',
        '</tr>                                               '
    ].join('\n'));

    $('#PNA-file').change(function () {
        var binaryFile = this.files[0];
        var blob = binaryFile.slice(0, binaryFile.size);
        var reader = new FileReader();

        reader.onloadend = function () {
            var binaryString = reader.result;
            var binaryFile = new BinaryFile(binaryString);
            var pnaObject = new PNA(binaryFile);

            var $layers = $('#layers').empty();
            var $table = $('<table style="border-collapse: collapse;"/>');

            for (var i = 0, n = pnaObject.layers.length; i < n; ++i) {
                var $layerInfo = $layerInfoTemplate.clone();
                var layer = pnaObject.layers[i];

                $layerInfo.find('.preview').css({
                    backgroundImage: ['url(', layer.pngDataUrl, ')'].join('')
                });
                $layerInfo.find('.layer-width').text(layer.layerWidth);
                $layerInfo.find('.layer-height').text(layer.layerHeight);
                $layerInfo.find('.offset-left').text('\u0394X:' + layer.offsetLeft);
                $layerInfo.find('.offset-top').text('\u0394Y:' + layer.offsetTop);

                $table.append($layerInfo);
            }

            $layers.append($table);
        };

        reader.readAsBinaryString(blob);
    });
});
