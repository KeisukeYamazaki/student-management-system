$(function () {
    $('#meeting_sheet_grade').change(function () {
        let now_url = location.href;
        let grade = $('#meeting_sheet_grade').val();
        if(now_url.slice(-3).startsWith('j')) {
            window.location.href = now_url.slice(0, -3) + grade;
        } else {
            window.location.href = now_url + grade;
        }
    })
});
