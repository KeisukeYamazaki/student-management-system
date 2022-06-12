$(function($){
    show()

    $('#ave_all, #late_all').on('click', function () {
        let id = $(this).attr('id');
        if(id.indexOf('ave') != -1) {
            $('#ave_all').addClass('act');
            $('#late_all').removeClass('act');
            for(let i = 1; i <= 3; i++) {
                averageSelect(i);
            }
        } else {
            $('#late_all').addClass('act');
            $('#ave_all').removeClass('act');
            for(let i = 1; i <= 3; i++) {
                lateSelect(i);
            }
        }
    });

    $('#ave1, #ave2, #ave3').click(function () {
        let number = $(this).attr('id').replace('ave', '');
        averageSelect(number)
    });

    $('#late1, #late2, #late3').click(function () {
        let number = $(this).attr('id').replace('late', '');
        lateSelect(number)
    });

    function show() {
        let recordTextSelector, scoreTextSelector, borderTextSelector;
        let recordValueSelector, scoreValueSelector, borderValueSelector;
        let recordNeedValue, scoreAverageValueSelector;
        for(let i = 1; i <= 3; i++) {
            // TextSelector: 表示させる部分のセレクタ
            recordTextSelector = '#record' + i;
            scoreTextSelector = '#score' + i;
            borderTextSelector = '#border' + i;
            if($('.act').attr('id').indexOf('ave') != -1) {
                // ValueSelector: 値を取得する部分のセレクタ
                recordValueSelector = '#record_ave' + i;
                scoreValueSelector = '#score_calc_ave' + i;
                borderValueSelector = '#border_calc_ave' + i;
                // NeedValueSelector: あとどれくらい成績が必要かを取得するセレクタ
                let recordNeedValueSelector = '#record_calc_ave' + i;
                if ($(recordNeedValueSelector).val() == '') {
                    recordNeedValue = ''
                } else if ($(recordNeedValueSelector).val() < 0){
                    recordNeedValue = '(あと ' + Math.abs($(recordNeedValueSelector).val()) + ' 必要)';
                } else {
                    recordNeedValue = '( ' + Math.abs($(recordNeedValueSelector).val()) + ' 上回る)';
                }

                // 合格者平均の点数を取得するセレクタ
                scoreAverageValueSelector = '#score_ave' + i;
            } else {
                // TextSelector: 表示させる部分のセレクタ
                recordValueSelector = '#record_late' + i;
                scoreValueSelector = '#score_calc_late' + i;
                borderValueSelector = '#border_calc_late' + i;
                // NeedValueSelector: あとどれくらい成績が必要かを取得するセレクタ
                let recordNeedValueSelector = '#record_calc_late' + i;
                if ($(recordNeedValueSelector).val() < 0){
                    recordNeedValue = 'あと ' + Math.abs($(recordNeedValueSelector).val()) + ' 必要';
                } else {
                    recordNeedValue = ' ' + Math.abs($(recordNeedValueSelector).val()) + ' 上回る'
                }
                // 合格者平均の点数を取得するセレクタ
                scoreAverageValueSelector = '#score_late' + i;
            }
            let scoreAverageValue;
            if ($(scoreAverageValueSelector).val() == '') {
                scoreAverageValue = ''
            } else {
                scoreAverageValue = '(県平均: ' + $(scoreAverageValueSelector).val() + ')';
            }
            $(recordTextSelector).html($(recordValueSelector).val() + '<br>' + recordNeedValue);
            $(scoreTextSelector).html($(scoreValueSelector).val() + '<br>' + scoreAverageValue);
            $(borderTextSelector).text($(borderValueSelector).val());
        }

    }

    function averageSelect(number) {
        let buttonAddSelector = '#ave' + number;
        // TextSelector: 表示させる部分のセレクタ
        let recordTextSelector = '#record' + number;
        let scoreTextSelector = '#score' + number;
        let borderTextSelector = '#border' + number;
        // ValueSelector: 値を取得する部分のセレクタ
        let recordValueSelector = '#record_ave' + number;
        let scoreValueSelector = '#score_calc_ave' + number;
        let borderValueSelector = '#border_calc_ave' + number;
        // NeedValueSelector: あとどれくらい成績が必要かを取得するセレクタ
        let recordNeedValueSelector = '#record_calc_ave' + number;
        let recordNeedValue;
        if ($(recordNeedValueSelector).val() == '') {
            recordNeedValue = ''
        } else if ($(recordNeedValueSelector).val() < 0){
            recordNeedValue = '(あと ' + Math.abs($(recordNeedValueSelector).val()) + ' 必要)';
        } else {
            recordNeedValue = '( ' + Math.abs($(recordNeedValueSelector).val()) + ' 上回る)';
        }
        // 合格者平均の点数を取得するセレクタ
        let scoreAverageValueSelector = '#score_ave' + number;
        let scoreAverageValue;
        if ($(scoreAverageValueSelector).val() == '') {
            scoreAverageValue = ''
        } else {
            scoreAverageValue = '(県平均: ' + $(scoreAverageValueSelector).val() + ')';
        }
        $(buttonAddSelector).addClass('act');
        $(recordTextSelector).html($(recordValueSelector).val() + '<br>' + recordNeedValue);
        $(scoreTextSelector).html($(scoreValueSelector).val() + '<br>' + scoreAverageValue);
        $(borderTextSelector).text($(borderValueSelector).val());
        let buttonRemoveSelector = '#late' + number;
        $(buttonRemoveSelector).removeClass('act');
    }

    function lateSelect(number) {
        let buttonAddSelector = '#late' + number;
        // TextSelector: 表示させる部分のセレクタ
        let recordTextSelector = '#record' + number;
        let scoreTextSelector = '#score' + number;
        let borderTextSelector = '#border' + number;
        // ValueSelector: 値を取得する部分のセレクタ
        let recordValueSelector = '#record_late' + number;
        let scoreValueSelector = '#score_calc_late' + number;
        let borderValueSelector = '#border_calc_late' + number;
        // NeedValueSelector: あとどれくらい成績が必要かを取得するセレクタ
        let recordNeedValueSelector = '#record_calc_late' + number;
        let recordNeedValue;
        if ($(recordNeedValueSelector).val() == '') {
            recordNeedValue = ''
        } else if ($(recordNeedValueSelector).val() < 0){
            recordNeedValue = '(あと ' + Math.abs($(recordNeedValueSelector).val()) + ' 必要)';
        } else {
            recordNeedValue = '( ' + Math.abs($(recordNeedValueSelector).val()) + ' 上回る)';
        }
        // 合格者平均の点数を取得するセレクタ
        let scoreAverageValueSelector = '#score_late' + number;
        let scoreAverageValue;
        if($(scoreAverageValueSelector).val() == '') {
            scoreAverageValue = ''
        } else {
            scoreAverageValue = '(県平均: ' + $(scoreAverageValueSelector).val() + ')';
        }
        $(buttonAddSelector).addClass('act');
        $(recordTextSelector).html($(recordValueSelector).val() + '<br>' + recordNeedValue);
        $(scoreTextSelector).html($(scoreValueSelector).val() + '<br>' + scoreAverageValue);
        $(borderTextSelector).text($(borderValueSelector).val());
        let buttonRemoveSelector = '#ave' + number;
        $(buttonRemoveSelector).removeClass('act');
    }
});