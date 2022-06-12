$(function ($) {
    now_grade_change();
    show_grade_change();

    let sent_grade = $('#sent_grade').val();
    let sent_grade_selector = '#show_grade option[value="' + sent_grade + '"]'
    $(sent_grade_selector).prop('selected',true);

    let sent_term = $('#sent_term').val();
    let sent_term_selector = '#term option[value="' + sent_term + '"]'
    $(sent_term_selector).prop('selected',true);

    $('.record_select').change(function () {
        let now = $('#now_grade').val();
        let grade = $('#show_grade').val();
        let term = $('#term').val();
        let param = '?now=' + now + '&grade=' + grade + '&term=' + term;
        history.replaceState('', '', param);

        let url = location.href;
        $('#record_grade_term_show').attr('href', url);
    });

    $('#now_grade').change(function () {
        now_grade_change();
    });

    $('#show_grade').change(function () {
        show_grade_change();
    });

    function now_grade_change() {
        let now = $('#now_grade').val();
        if (now == '') {
            $('#show_grade').children().remove();
            $('#show_grade').append("<option value=''>学年</option>");
            $('#show_grade').append("<option value='j3'>中３</option>")
            $('#show_grade').append("<option value='j2'>中２</option>")
            $('#show_grade').append("<option value='j1'>中１</option>")
        } else if (now == 'j3') {
            $('#show_grade').children().remove();
            $('#show_grade').append("<option value=''>学年</option>");
            $('#show_grade').append("<option value='j3'>中３</option>")
            $('#show_grade').append("<option value='j2'>中２</option>")
            $('#show_grade').append("<option value='j1'>中１</option>")
        } else if (now == 'j2') {
            $('#show_grade').children().remove();
            $('#show_grade').append("<option value=''>学年</option>");
            $('#show_grade').append("<option value='j2'>中２</option>")
            $('#show_grade').append("<option value='j1'>中１</option>")
        } else {
            $('#show_grade').children().remove();
            $('#show_grade').append("<option value=''>学年</option>");
            $('#show_grade').append("<option value='j1'>中１</option>")
        }
    }

    function show_grade_change() {
        let show_grade = $('#show_grade').val();
        if (show_grade == 'j3') {
            $('#term').children().remove();
            $('#term').append("<option value=''>学期</option>");
            $('#term').append("<option value=1>１学期・前期</option>");
            $('#term').append("<option value=4>２学期・後期</option>");
        } else {
            $('#term').children().remove();
            $('#term').append("<option value=''>学期</option>");
            $('#term').append("<option value=1>１学期・前期</option>");
            $('#term').append("<option value=2>２学期</option>");
            $('#term').append("<option value=3>３学期・後期</option>");
        }
    }
});