$(function ($) {
    // 全県模試の登録・編集をする学年と校舎の選択をパラメータ表示させる
    $('#zenken_school, #zenken_grade').change(function () {
        let school = $('#zenken_school').val();
        let grade = $('#zenken_grade').val();
        let param = `?school=${school}&grade=${grade}`;
        history.replaceState('', '', param);

        let url = location.href;
        $('#zenken_select').attr('href', url);
    });

    // // それぞれのボタンにURLを設定する
    $(document).ready(function(){
        let now_url = location.href;
        let edit_url = now_url.replace('zenken/', 'zenken/edit/');
        let download_url = now_url.replace('zenken/', 'zenken/download/');
        // ボタンに設定
        $('#zenken_edit').attr('href', edit_url);
        $('#zenken_download').attr('href', download_url);
    });
});
