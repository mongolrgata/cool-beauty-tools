/**
 * Created by mongolrgata
 */

require.config({
    paths: {
        jquery: 'lib/jquery-2.1.4.min',
        doT: 'lib/doT.min',
        Layer: 'modules/Layer/Layer.module',
        BinaryFile: 'modules/BinaryFile/BinaryFile.module',
        PNA: 'modules/PNA/PNA.module'
    }
});

require(['jquery', 'doT', 'BinaryFile', 'PNA', 'text!../templates/layer.doT'], function ($, doT, BinaryFile, PNA, layerT) {
    var layerFn = doT.template(layerT);

    $(document).ready(function () {
        $('#PNA-file').change(function () {
            var file = this.files[0];
            var blob = file.slice(0, file.size);
            var reader = new FileReader();

            reader.onloadend = function () {
                var binaryString = reader.result;
                var binaryFile = new BinaryFile(binaryString);
                var pnaObject = new PNA(binaryFile);
                var layers = pnaObject.getLayers();

                var $images = $('#images').empty();
                var $layers = $('#layers').empty();

                var $background = $('<div/>').addClass('background').css({
                    width: pnaObject.getImageWidth(),
                    height: pnaObject.getImageHeight()
                });
                var $table = $('<table/>').addClass('layers-info');

                for (var i = 0, n = layers.length; i < n; ++i) {
                    var layer = layers[i];
                    var layerCSS = layer.getCSS();
                    var $img = $('<div/>').addClass('img').css(layerCSS).hide();
                    var $tr = $(layerFn(layerCSS));

                    $tr.find('.visible-check').change({linkedImage: $img}, function (event) {
                        event.data.linkedImage.toggle($(this).prop('checked'));
                    });

                    $background.append($img);
                    $table.append($tr);
                }

                $images.append($background);
                $layers.append($table);
            };

            reader.readAsBinaryString(blob);
        });
    });
});
