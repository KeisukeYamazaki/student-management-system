$(function ($) {
    // 選択によってurlを動的に変更する
    $('#personal_grade').change(function () {
        let now_url = location.href;
        let grade = $('#personal_grade').val();
        let url_block = now_url.split('/');
        if (now_url.slice(-3).startsWith('j')) {
            window.location.href = now_url.slice(0, -3) + grade;
        } else if (url_block.length == 9 || url_block.length == 8) {
            // 学年/ID/kindまである or 学年/ID まである場合
            // personal まで取得
            url_block = url_block.splice(0, 5);
            // http:// の / を１つ追加
            url_block.splice(1, 0, '/');
            // url を / で区切った配列を再び / で結合し、 gradeを加える
            window.location.href = url_block.join('/') + '/' + grade;
        } else {
            window.location.href = now_url + grade;
        }
    });

    // 個人選択で何を登録するかの選択
    $('input[name="radio_name"]').change(function () {
        let now_url = location.href;
        let kind = $('input[name="radio_name"]:checked').val();
        let kinds = ['school_record', 'regular_exam', 'practice_exam'];
        if (now_url.indexOf(kinds[0]) != -1 || now_url.indexOf(kinds[1]) != -1 || now_url.indexOf(kinds[2]) != -1) {
            for (let i = 0; i < kinds.length; i++) {
                now_url = now_url.replace('/' + kinds[i], "");
            }
            window.location.href = now_url + kind + '/';
        } else {
            window.location.href = now_url + kind + '/';
        }
    });

    // 個人登録の際に科目の合計を表示するメソッド
    // $(document) とすると、追加された行の要素もイベントの対象として認識される
    $(document).on('input', '.personal', function () {
        let subjects_five = ['english', 'math', 'japanese', 'science', 'social_studies'];
        let not_five_subjects = ['music', 'art', 'pe', 'tech_home'];
        // 入力したテキストボックスのname(=subject)を取得
        let subject = $(this).attr('name');
        // index でクリックした科目が何番目かを取得する
        let index = $('input[name="' + subject + '"]').index(this);
        let sum_five = 0;
        // ５科目でループを回す
        for (let i = 0; i < subjects_five.length; i++) {
            if (parseInt($('input[name=' + [subjects_five[i]] + ']').eq(index).val(), 10)) {
                // parseIntできれば、sum_fiveに加える
                sum_five = sum_five + parseInt($('input[name=' + [subjects_five[i]] + ']').eq(index).val(), 10);
            }
        }
        // 9科目の場合も同様
        let sum_all = sum_five;
        for (let i = 0; i < not_five_subjects.length; i++) {
            if (parseInt($('input[name=' + [not_five_subjects[i]] + ']').eq(index).val(), 10)) {
                sum_all = sum_all + parseInt($('input[name=' + [not_five_subjects[i]] + ']').eq(index).val(), 10);
            }
        }
        // 模試用の３科目(5科目の配列を使い、3回ループを回す)
        let sum_three = 0;
        for (let i = 0; i < 3; i++) {
            if (parseInt($('input[name=' + [subjects_five[i]] + ']').eq(index).val(), 10)) {
                sum_three = sum_three + parseInt($('input[name=' + [subjects_five[i]] + ']').eq(index).val(), 10);
            }
        }
        // valueとtextに合計をセットする
        $('input[name="sum_five"]').eq(index).attr('value', sum_five);
        $('.sum_five').eq(index).text(sum_five);
        $('input[name="sum_all"]').eq(index).attr('value', sum_all);
        $('.sum_all').eq(index).text(sum_all);
        $('input[name="sum_three"]').eq(index).attr('value', sum_three);
        $('.sum_three').eq(index).text(sum_three);

        // １つでも点数・成績が入力されている場合、学年、実施年度、時期など必要な項目が入力されているかをチェック
        $('.personal_registry').click(function () {
            let subjects_five = ['english', 'math', 'japanese', 'science', 'social_studies'];
            let record_checks = ['grade', 'record_year', 'term_name'];
            let regular_checks = ['grade', 'exam_year', 'regular_id'];
            let practice_checks = ['grade', 'exam_year', 'month_id'];
            // 展開されている行の数(gradeの数)を取得
            let count = $('[name="grade"]').length;
            // 押されたボタンが school_record か regular_exam か practice_exam かを取得
            let kind = $(this).val();
            let check_list = kind == 'school_record' ? record_checks :
                             kind == 'regular_exam' ? regular_checks : practice_checks;
            for (let row = 0; row < count; row++) {
                // 各行の数値の入力状況を確認
                for (let sub = 0; sub < subjects_five.length; sub++) {
                    if ($('input[name="' + subjects_five[sub] + '"]').eq(row).val() != '') {
                        // １つでも入力されている場合は、学年、実施年度、時期などが入力されているかを確認
                        for(let check = 0; check < check_list.length; check++) {
                            if ($('[name="' + check_list[check] + '"]').eq(row).val() == ''){
                                // check_listのいずれかが''ならfalseを返し、処理しない
                                $('.error').css('display', 'inline');
                                return false;
                            }
                        }
                    }
                }
            }
        });
    });
});
