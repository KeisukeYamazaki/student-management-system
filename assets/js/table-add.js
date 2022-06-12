//最終行に追加する
jQuery(function($) {
    $("#btnAdd1").on("click", function() {
        // テーブルの最終行をクローンしてテーブルの最後に追加する
        $("#tblForm1 tbody tr:last-child").clone(true).appendTo("#tblForm1 tbody");

        // 追加した行の値をクリアする
        $("#tblForm1 tbody tr:last-child input").val("");
        $("#tblForm1 tbody tr:last-child .sum_five").text("0");
        $("#tblForm1 tbody tr:last-child .sum_all").text("0");
    });
});