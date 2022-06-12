$(function() {
    // 1. 「全選択」する
    $('#all').on('click', function() {
        $("input[name='class_name']").prop('checked', this.checked);
    });
    // 2. 「全選択」以外のチェックボックスがクリックされたら、
    $("input[name='class_name']").on('click', function() {
        if ($('.checkbox :checked').length == $('.checkbox :input').length) {
            // 全てのチェックボックスにチェックが入っていたら、「全選択」 = checked
            $('#all').prop('checked', true);
        } else {
            // 1つでもチェックが入っていたら、「全選択」 = checked
            $('#all').prop('checked', false);
        }
    });
});