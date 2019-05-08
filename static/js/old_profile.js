$(function () {
    $('.profile-panel').on('click', '.profile-editor', function () {
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

    $('.profile-panel').on('click', '.edit-cancel', function () {
        let initValue = $('.profile-text-input').data('initial');
        let field = $('.profile-update-group').data('field');
        let fieldClass = '.td-profile-' + field;
        $(fieldClass).html(initValue)
        $(fieldClass).next().children().toggleClass('profile-editor')
    });
    $('.profile-panel').on('click', '.profile-edit-submit', function () {
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



