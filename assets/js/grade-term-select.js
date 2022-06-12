$(function ($) {
    let now_url = location.href;
    let term_now_value = $('#term_name').val();
    $(window).on('load', function () {
        let list = ['j3', 'j2', 'j1', 'e6', 'e5', 'e4', 'e3'];
        for(let i = 0; i < list.length; i++) {
            now_url = now_url.replace('/' + list[i], '');
        }
    })

    $('#grade_select').change(function () {
        let clicked_url = location.href;
        let grade = $('#grade_select option:selected').val();
        if(term_now_value == undefined || term_now_value == '') {
            if(clicked_url.slice(-3).startsWith('j')) {
                window.location.href = clicked_url.slice(0, -3) + grade;
            } else {
                window.location.href = clicked_url + grade;
            }
        } else {
            let url = clicked_url.slice(0, -5);
            window.location.href =  url + grade;
        }
    });
});