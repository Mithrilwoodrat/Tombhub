function register(){
    username = $('#username').val();
    passwd = $('#passwd').val();
    rpt_passwd = $('#rpt_passwd').val();
    if (!(username&&passwd)){
        alert("请输入帐号密码");
        return false;
    }
    else if (passwd != rpt_passwd)
    {
        alert("输入密码不一致");
        return false;
    }
    $.post(
            '/register',
            {
                username : username,
                passwd : passwd},
            function(data) {
                if (data.status == 'SUCCESS'){
                    location.href = '/login';
                }
                else{
                    alert("注册失败"+data.error);
                    location.href = '/register';
                }
            });
}
