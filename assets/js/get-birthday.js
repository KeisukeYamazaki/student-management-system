$(function ($) {
    /*
      誕生日の日付データを変数birthdayに格納
     */
    let birth_year, birth_month, birth_day, default_dom;
    let birthday = $('#bd').val();
    if (birthday != undefined && birthday != 'None') {
        let date = birthday.split('-');
        birth_year = date[0];
        birth_month = date[1];
        birth_day = date[2];
        default_dom = '<input type="hidden" id="id_birthday" name="birthday" value=' + birthday + '>'
    } else {
        default_dom = '<input type="hidden" id="id_birthday" name="birthday" value="">'
    }
    $('#bd').after(default_dom);

    $('.change').change(function () {
        $('#id_birthday').remove();
        let year = $('#id_year option:selected').text();
        let month = $('#id_month option:selected').text();
        if (month.length == 1) {
            month = 0 + month;
        }
        let day = $('#id_day option:selected').text();
        if (day.length == 1) {
            day = '0' + day;
        }
        let birthday = year + '-' + month + '-' + day;
        let dom = '<input type="hidden" id="id_birthday" name="birthday" value=' + birthday + '>';
        $('#bd').after(dom);
    });


    /*
      ループ処理（スタート数字、終了数字、表示id名、デフォルト数字、年月日の種類）
     */
    function optionLoop(start, end, id, birth, kind) {
        let i, opt;
        opt = "<option value='" + "'>" + "---" + "</option>";
        for (i = start; i <= end; i++) {
            if (i == birth) {
                opt += "<option value='" + i + "' selected>" + i + "</option>";
            } else {
                opt += "<option value='" + i + "'>" + i + "</option>";
            }
        }
        return document.getElementById(id).innerHTML = opt;
    };

    /*
      関数設定（スタート数字[必須]、終了数字[必須]、表示id名[省略可能]、デフォルト数字[省略可能]）
     */
    let now = new Date();
    let this_year = now.getFullYear();
    optionLoop(2000, this_year, 'id_year', birth_year, 'year');
    optionLoop(1, 12, 'id_month', birth_month, 'month');
    optionLoop(1, 31, 'id_day', birth_day, 'day');
});