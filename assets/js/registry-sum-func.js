$(function ($) {
    // ページが開かれて最初に行われる
    for (let i = 0; i < $('.counter').length; i++) {
        record_sum(i);
    }

    // 値が変わったときに行われる
    $('.sum').on('input', function () {
        let num = Math.floor($('.sum').index(this) / 9);
        record_sum(num)
    });

    function record_sum(number) {
        let selector_five = '.five' + number;
        let selector_all = '.all' + number;

        let sum_five = get_sum(selector_five);
        let sum_all = get_sum(selector_all) + sum_five;

        let id_five = '#sum_five' + number;
        $(id_five).prop('value', sum_five);
        let id_all = '#sum_all' + number;
        $(id_all).prop('value', sum_all);
    }

    function get_sum(selector) {
        let sum = 0;
        for(let i = 0; i < $(selector).length; i++) {
            if($(selector).eq(i).val() != '') {
                sum = sum + parseInt($(selector).eq(i).val(), 10);
            }
        }
        if(sum == 0) {
            return '';
        }
        return sum;
    }
});