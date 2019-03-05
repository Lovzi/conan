// function submitProblemComments(classId) {
//     alert(classId)
//     let that = $('.comment-editor-' + classId);
//     let problemId = that.data('problem-id');
//     let userId = $('.user-id').data('user-id');
//     let repliedId = that.data('replied-id');
//     let parentCommentId = that.data('parent-comment-id')
//     alert(parentCommentId)
//     alert(problemId)
//     //alert(document.cookie)
//     //if(document.cookie.indexOf('sessionid') !== -1)
//     if(userId !== 'None'){
//         let comment = that.val();
//         if(comment === ""){
//             alert('评论不能为空')
//         }
//         else{
//             $.ajax({
//                 type: 'POST',
//                 url: '/problems/'+ problemId + '/comments/',
//                 traditional:true,
//                 data: {'comment': comment , 'problem_id': problemId, 'user_id': userId, 'replied_id':　repliedId, 'parent_comment_id': parentCommentId},
//                 success: function(res) {
//                     $('.problem-container').html(res['content'])
//                 }
//             })
//         }
//     }else{
//         alert('请先登录')
//     }
// }
//
// function getProblemComments() {
//
// }


$().off().ready(function () {
    $('.problem-submissions-et').click(function () {
        let problemId = $('.data-problem-id').data('problem-id');
        url = '/problems/' + problemId + '/submissions/'
        $.get(url, {}, function (res) {
             $('.problem-container').html(res['content'])
        })
        $('.active').toggleClass('active')
        $('.problem-submissions-li').toggleClass('active')
    });
    $('.problem-solution-et').click(function () {
        let problemId = $('.data-problem-id').data('problem-id');
        url = '/problems/' + problemId + '/solution/'
        $.get(url, {}, function (res) {
             $('.problem-container').html(res['content'])
        })
        $('.active').toggleClass('active')
        $('.problem-solution-   li').toggleClass('active')
    });
    $('.problem-comments-et').click(function () {
        let problemId = $('.data-problem-id').data('problem-id');
        url = '/problems/' + problemId + '/comments/'
        $.get(url, {}, function (res) {
             $('.problem-container').html(res['content'])
        });
        $('.active').toggleClass('active')
        $('.problem-comments-li').toggleClass('active')
    });
    $('.problem-container').on('click', '.submit-comment', function (event) {
        let target = event.target || window.event
        let obj = $(target)
        if(obj.data('type') !== 'master'){
            let commentObj = obj.parents('.singer-comment-container');
            var repliedId = commentObj.data('replied-id')
            var parentCommentId = commentObj.data('parent-comment-id');
        }
        let textArea = obj.prev();
        //alert(document.cookie)
        //if(document.cookie.indexOf('sessionid') !== -1)
        let problemId = $('.data-problem-id').data('problem-id');
        let userId = $('.user-id').data('user-id');
        if(userId !== 'None'){
            let commentComtent = textArea.val();
            if(commentComtent === ""){
                alert('评论不能为空')
            }
            else{
                url = '/problems/' + problemId + '/comments/'
                $.post(
                    url,
                    {'comment': commentComtent , 'problem_id': problemId, 'user_id': userId, 'replied_id':　repliedId, 'parent_comment_id': parentCommentId},
                    function(res) {
                        $('.problem-container').html(res['content'])
                })
            }
        }else{
            alert('请先登录')
        }
    });
    // $('.problem-container').on('click', 'submit-comment', function (event) {
    //
    // });

    $('.problem-container').on('click', '.code-submit', function () {
        let editor = $('.code-editor');
        let problemId = $('.data-problem-id').data('problem-id');
        let code = editor.val()
        alert(problemId)
        let url = "/problems/answer/g++/"
        $.post(url, {'code': code, 'problem_id': problemId, 'user_id':'1'}, function(res) {
            alert(res)
        });
    });


    $('.problem-container').on('click', '.reply-cls-btn', function (event) {
        let target = event.target
        let obj = $(target)
        let commentObj = obj.parents('.singer-comment-container')
        let commentId = commentObj.attr('id')
        let html = '<div class="panel-body">\n' +
        '    <form role="form" class="comment-form" action="">' +
        '      <div class="form-group">\n' +
        '        <textarea class="form-control comment-editor" rows="5"></textarea>\n' +
        '        <button class="btn btn-primary submit-comment" type="button">评论</button>\n' +
        '    </div>\n' +
        '    </form>\n' +
        '</div>';
        let replyContainer = $('.reply-input-container-' + commentId)
        replyContainer.html(html)
    })

    $('.problem-container').on('click', '.problem-comment-star', function (event) {
        let obj = event.target || window.event.target
        let problemId = $('.data-problem-id').data('problem-id');
        let commentId = $(obj).parents('.singer-comment-container').attr('id')
        alert(commentId)
        let url = '/problems/' + problemId + '/comments/';
        $.put(url, {'id': commentId}, function (res) {
            $(obj).html(res['content'])
        })
    })
});
