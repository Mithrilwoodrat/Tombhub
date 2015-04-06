function login(){
  username = $('#username').val();
  passwd = $('#passwd').val();
  if (!(username&&passwd)){
    alert("请输入帐号密码");
    return false;
  }
  $.post(
  '/login',
  {
  username : username,
  passwd : passwd}, 
  function(data) {
    if (data.status == 'login success'){
      location.href = '/';
    }
    else{
      alert("登录失败");
      location.href = '/login';
    }
  });
}