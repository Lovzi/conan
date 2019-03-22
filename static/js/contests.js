$(function () {
    // function(inputValue){
    //   if (inputValue === false) return false;
    //
    //   if (inputValue === "") {
    //     swal.showInputError("你需要输入一些话！");
    //     return false
    //   }
    //   swal("非常好！", "你输入了：" + inputValue,"success");
    // });
    $('.contest-dis').on('click', '.random-contest', function (event) {
        let url = '/contest/virtual_contest/random/'
        $.get(url, function (res) {
            if(res['status']){
                // swal("虚拟竞赛创建成功", "竞赛已经开始！","success")
                swal({
                    title: "虚拟竞赛创建成功？",
                    text: "竞赛已经开始！",
                    icon: "success",
                    button: "前往竞赛",
                }).then(() => {
                    let url = "/contest/virtual/" + res['contestName'] + "/"
                    window.location.href= url
                    });
            }else{
                swal("虚拟竞赛创建失败", "请稍后重试！","error")
            }
        })
    })
})