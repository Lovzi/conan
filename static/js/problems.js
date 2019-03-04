$().ready(function () {
    $('.code-submit').click(function () {
        let editor = $('.code-editor');
        let problemId = $('.data-problem-id').data('problem-id');
        let code = editor.val()
        alert(problemId)
        let url = "/problems/answer/g++/"
        $.post(url, {'code': code, 'problem_id': problemId, 'user_id':'1'}, function(res) {
            alert(res)
        });
    });

    $('.page-index').click(function () {
        let index = this.val() - 1
        let offset = index * 50
        $.ajax({
            type: "POST",
            url: "/problems/answer/",
            traditional: true,
            data: {'code': code, 'problem_id': problemId, 'user_id': '1'},
            success: function (res) {
                alert(res)
            }

        })
    })
})