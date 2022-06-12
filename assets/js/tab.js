$(function ($) {
    // パラメーターに現在のタブを表示する
    $('.nav-link').on("click", function () {
        let tab = $(this).attr('href').replace('#tab', '');
        history.replaceState('', '', tab);

        let tab_num = location.href.slice(-1);
        let selector = '#tab' + tab_num;
        $('.tab-pane').hide();
        $(selector).addClass('active in');
        $(selector).show();
    });

    $(window).on('load', function () {
        let tab_num = location.href.slice(-1);
        let selector = '#tab' + tab_num;
        $('.tab-pane').hide();
        $(selector).addClass('active in');
        $(selector).show();
    })
});