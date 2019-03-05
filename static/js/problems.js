$().ready(function () {
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