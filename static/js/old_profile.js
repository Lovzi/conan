var cookie = {
    set:function(key,val,time){//设置cookie方法
        let date=new Date(); //获取当前时间
        let expiresDays=time;  //将date设置为n天以后的时间
        date.setTime(date.getTime() + expiresDays*24*3600*1000); //格式化为cookie识别的时间
        document.cookie=key + "=" + val +";expires="+date.toGMTString();  //设置cookie
    },
    get:function (Name) {
        var search = Name + "="//查询检索的值
        var returnvalue = "";//返回值
        if (document.cookie.length > 0) {
            sd = document.cookie.indexOf(search);
            if (sd!== -1) {
                sd += search.length;
                end = document.cookie.indexOf(";", sd);
                if (end === -1)
                    end = document.cookie.length;
                //unescape() 函数可对通过 escape() 编码的字符串进行解码。
                returnvalue=unescape(document.cookie.substring(sd, end))
            }}
       return returnvalue;
    },
    delete: function(key){ //删除cookie方法
        var date = new Date(); //获取当前时间
        date.setTime(date.getTime()-10000); //将date设置为过去的时间
        document.cookie = key + "=v; expires =" +date.toGMTString();//设置cookie
    }
};


$(function () {
    $('.profile-editor').click(function () {
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
        else if(field === 'birthday'){

        }
        else{
            var initValue = $(fieldClass).val();
            var html =
                '<form onsubmit="return false" class="profile-update-form">\n' +
                '  <div class="form-group profile-update-group" data-field='+ field +'>\n' +
                '    <input type="text" name="'+ field + '" class="form-control profile-text-input" data-initial="'+ initValue +'" placeholder="'+ initValue +'">\n' +
                '    <button type="submit" class="btn btn-primary profile-edit-submit" onclick="profileUpdate()">保存</button>' +
                '    <button class="btn btn-default edit-cancel" onclick="updateCancel()">取消</button>' +
                '  </div>' +
                '</form>'
        }
        $(fieldClass).html(html)
    });


});

function updateCancel() {
    alert('sdfdsf')
    let initValue = $('.profile-text-input').data('initial');
    let field = $('.profile-update-group').data('field');
    let fieldClass = '.td-profile-' + field;
    $(fieldClass).html(initValue)
}
function profileUpdate() {
    field = $('.profile-update-group').data('field');
    updateValue = $('.profile-text-input').val()
    $.post("/accounts/profile/"+ field + "/", {sdf: updateValue}, function (res) {
        let fieldClass = '.td-profile-' + field;
        let value = res;
        $(fieldClass).html(res)
    })
}




