/**
 * Created by mongolrgata
 */

$(document).ready(function () {
    $('#PNA-file').change(function () {
        var binaryFile = this.files[0];
        var blob = binaryFile.slice(0, binaryFile.size);
        var reader = new FileReader();

        reader.onloadend = function () {
            var binaryString = reader.result;
            var binaryFile = new BinaryFile(binaryString);
            var pnaObject = new PNA(binaryFile);

            // TODO
        };

        reader.readAsBinaryString(blob);
    });
});
