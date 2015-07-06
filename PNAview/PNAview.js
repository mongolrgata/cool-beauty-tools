/**
 * Created by mongolrgata
 */

$(document).ready(function () {
    var $layerInfoTemplate = $([
        '<tr class="layer-info">                                  ',
        '   <td><input class="visible-check" type="checkbox"></td>',
        '   <td><div class="preview"></div></td>                  ',
        '   <td align="right"><span class="layer-width"></td>     ',
        '   <td>&#x2715;</td>                                     ',
        '   <td align="left"><span class="layer-height"></td>     ',
        '   <td>&#x394;X:</td>                                    ',
        '   <td align="right"><span class="offset-left"></td>     ',
        '   <td>&#x394;Y:</td>                                    ',
        '   <td align="right"><span class="offset-top"></td>      ',
        '</tr>                                                    '
    ].join('\n'));

    $('#PNA-file').change(function () {
        var binaryFile = this.files[0];
        var blob = binaryFile.slice(0, binaryFile.size);
        var reader = new FileReader();

        reader.onloadend = function () {
            var binaryString = reader.result;
            var binaryFile = new BinaryFile(binaryString);
            var pnaObject = new PNA(binaryFile);

            var $images = $('#images').empty();
            var $background = $('<div/>').css({
                position: 'relative',
                width: pnaObject.imageWidth,
                height: pnaObject.imageHeight,
                background: '' +
                'linear-gradient(135deg, transparent 75%, lightgray 0%) 0 0,    ' +
                'linear-gradient(-45deg, transparent 75%, lightgray 0%) 8px 8px,' +
                'linear-gradient(135deg, transparent 75%, lightgray 0%) 8px 8px,' +
                'linear-gradient(-45deg, transparent 75%, lightgray 0%) 0 0     ',
                backgroundSize: '16px 16px'
            });

            var $layers = $('#layers').empty();
            var $table = $('<table/>').css({
                borderCollapse: 'collapse'
            });

            for (var i = 0, n = pnaObject.layers.length; i < n; ++i) {
                var layer = pnaObject.layers[i];

                var $img = $('<img>').prop({
                    src: layer.pngDataUrl
                }).css({
                    position: 'absolute',
                    left: layer.offsetLeft,
                    top: layer.offsetTop,
                    zIndex: layer.zIndex
                }).hide();

                var $layerInfo = $layerInfoTemplate.clone();

                $layerInfo.find('.visible-check').change({linkedImage: $img}, function (event) {
                    event.data.linkedImage.toggle($(this).prop('checked'));
                });
                $layerInfo.find('.preview').css({
                    backgroundImage: ['url(', layer.pngDataUrl, ')'].join('')
                });
                $layerInfo.find('.layer-width').text(layer.layerWidth);
                $layerInfo.find('.layer-height').text(layer.layerHeight);
                $layerInfo.find('.offset-left').text(layer.offsetLeft);
                $layerInfo.find('.offset-top').text(layer.offsetTop);

                $background.append($img);
                $table.append($layerInfo);
            }

            $images.append($background);
            $layers.append($table);
        };

        reader.readAsBinaryString(blob);
    });
});
