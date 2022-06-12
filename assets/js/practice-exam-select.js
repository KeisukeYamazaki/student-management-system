$(function($){
    // URLによってチェックボックスを変える
    let now_url = location.href;
    let radio_id_list = [];
    $('input[name="practice_select"]').each(function(){ radio_id_list.push($(this).attr('id'))});
    $(window).on('load', function () {
        for (let i = 0; i < radio_id_list.length; i++) {
            if (now_url.indexOf(radio_id_list[i]) != -1) {
                // URLの中に、いずれかのidの値があった場合
                let selector = '#' + radio_id_list[i];
                $(selector).prop('checked', true);
            }
        }
    });

    // チェックが入ったときにURLを変える
    $('[name="practice_select"]').change(function () {
        let clean_url;
        let radio_id_list = [];
        // 'input[name="practice_select"]' の idの値をリストで取得する
        $('input[name="practice_select"]').each(function(){ radio_id_list.push($(this).attr('id'))});
        let clicked_url = location.href;
        let practice_select = $('input[name="practice_select"]:checked').attr('id');

        for (let i = 0; i < radio_id_list.length; i++) {
            if (radio_id_list[i] != practice_select) {
                // クリックされたもの以外のidの値は、replaceで削除
                clean_url = clicked_url.replace(radio_id_list[i] + '/', '');
            }
        }
        window.location.href = clean_url + practice_select;
    });

    // パラメータを変える
    $('.practice_select').change(function () {
        let birth_year = $('#birth_year').val();
        let month = $('#month').val();
        let school = $('#school').val();
        let param = '?birth_year=' + birth_year + '&month=' + month + '&school=' + school;
        history.replaceState('', '', param);

        let url = location.href.replace;
        $('#record_grade_term_show').attr('href', '');
        $('#record_grade_term_show').attr('href', url);
    });

    $('#get_practice_data').click(function () {
        let elements = [$('#birth_year').val(), $('#month').val(), $('#school').val()];
        for (let i = 0; i < elements.length; i++) {
            if (elements[i] == '') {
                $('#error').css('display', 'block')
                return false;
            }
        }
    })
});