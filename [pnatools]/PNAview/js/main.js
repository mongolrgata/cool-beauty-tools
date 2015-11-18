/**
 * Created by mongolrgata
 */

require.config({
    paths: {
        jquery: 'lib/jquery-2.1.4.min',
        Layer: 'modules/Layer/Layer.module',
        BinaryFile: 'modules/BinaryFile/BinaryFile.module',
        PNA: 'modules/PNA/PNA.module'
    }
});

require(['jquery'], function ($) {
    $(document).ready(function () {

    });
});
