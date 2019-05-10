$(function () {
    $('body').on('click', '.profile-nav', function (e) {
        let that = $(this)
        that.parent().children().removeClass('active')
        that.addClass('active')
        let module = $(this).data('m')
        let url = '/accounts/profile/modules/'
        $.post(url, {module: module}, function (res) {
            $('.profile-ctr').html(res)
        })
    })
})

$(function () {
    $('body').on('click', '.apply-group-btn', function (e) {
        swal({
            text: '请输入你想加入的队伍',
            content: "input",
            button: {
                text: "创建",
                closeModal: false,
            },
        }).then(name => {
            if (!name) throw null;
            let url = "/contest/apply_group/";
            $.post(url, {name: name}, function (res) {
                if (res.code === 10000) {
                    swal(res.message, res.detail, "success")
                }else{
                    swal(res.message, res.detail, "error")
                }
            })
        }).catch(err => {
          if (err) {
            swal("啊哦。。。", "服务器走丢了。。。", "error");
          } else {
            swal.stopLoading();
            swal.close();
          }
        });
    })
})

$(function () {
    $('.profile-ctr').on('click', '.profile-editor', function () {
        $(this).toggleClass('profile-editor')
        let field = $(this).data('field');
        let fieldClass = '.td-profile-' + field
        if(field === 'email'){
            let html = '<form>\n' +
                '  <div class="form-group">\n' +
                '    <label for="exampleInputEmail1">Email address</label>\n' +
                '    <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Email">\n' +
                '  </div>' +
                '</form>'


        }
        else if(field === 'password'){

        }
        else{
            // var initValue = $(fieldClass).val();
            let initValue = $(this).parent().prev().html()
            var html =
                '<form onsubmit="return false" class="profile-update-form">\n' +
                '  <div class="form-group profile-update-group" data-field='+ field +'>\n' +
                '    <input type="text" name="'+ field + '" class="form-control profile-text-input" data-initial="'+ initValue +'" placeholder="'+ initValue +'">\n' +
                '    <button type="submit" class="btn btn-primary profile-edit-submit" >保存</button>' +
                '    <button class="btn btn-default edit-cancel">取消</button>' +
                '  </div>' +
                '</form>'
        }
        $(fieldClass).html(html)
    });

    $('.mugshot-username').on('click', '.mugshot-img', function () {
        swal('')
    })

    $('.profile-ctr').on('click', '.edit-cancel', function () {
        let initValue = $('.profile-text-input').data('initial');
        let field = $('.profile-update-group').data('field');
        let fieldClass = '.td-profile-' + field;
        $(fieldClass).html(initValue)
        $(fieldClass).next().children().toggleClass('profile-editor')
    });
    $('.profile-ctr').on('click', '.profile-edit-submit', function () {
        let field = $('.profile-update-group').data('field');
        let updateValue = $('.profile-text-input').val();
        let fieldClass = '.td-profile-' + field;
        let initValue = $('.profile-text-input').data('initial');
        $.post("/accounts/profile/"+ field + "/", {field: field, data: updateValue}, function (res) {
            if(res['status']){
                $(fieldClass).html(res['data']);
                swal('修改成功', res['msg'], "success")
            }
            else{
                $(fieldClass).html(initValue)
                swal('修改失败', res['msg'], "error")
            }
        })
        $(fieldClass).next().children().toggleClass('profile-editor')
    })
});



