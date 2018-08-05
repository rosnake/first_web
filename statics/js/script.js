 function getCookie(name){
    var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return x ? x[1]:undefined;
}

function debugMessage(msg) {
    alert(msg);
    }

    
$(document).ready(function(){
    $("#login").click(function(){
        var user = $("#username").val();
        var pwd = $("#password").val();
        var verify_code = $("#verify_code").val();
        var pd = {"username":user, "password":pwd,"verify_code":verify_code, "_xsrf":getCookie("_xsrf")};
        $.ajax({
            type:"post",
            url:"/login",
            data:pd,
            cache:false,
            success:function(arg){
            console.log(arg);
            //arg是字符串
            var obj = JSON.parse(arg);
            if(obj.status){
                //注册成功---跳转（已登录状态--session实现）
                //alert("注册成功")
                window.location.href = "/home?user="+user;
            }else{
                alert(obj.error);
                window.location.href ="/login"
            }
            }
        });
    });
    
    $("#register").click(function(){
        //alert('register')
        var user = $("#username").val();
        var pwd = $("#password").val();
        var conf = $("#confirm").val();

        if (user == "") {
            $("#username").focus();
            debugMessage("用户名不能为空.");
            return false;
        }
        else
        {
            //debugMessage("用户名:"+user);    
        }
        //验证密码是否合理
        if(pwd.length < 6){            
            $("#password").focus();
            debugMessage("密码不能小于6位数."+pwd.length);
            return false;
        }
        
        if(pwd == ""){            
            $("#password").focus();
            debugMessage("密码不能为空");
            return false;
        }
        
        //验证密码与确认密码是否相等
        if(pwd != conf){            
            $("#password").focus();
            debugMessage("两次输入密码不一致"+"pwd:"+pwd+"conf:"+conf);
            return false;
        }
        
        //debugMessage("密码:"+pwd);
        //alert(user);
        var pd = {"username":user, "password":pwd,"confirm":conf, "_xsrf":getCookie("_xsrf")};
        
        $.ajax({
            type:"post",
            url:"/register",
            data:pd,
            cache:false,
            success:function(arg){
            console.log(arg);
            //arg是字符串
            var obj = JSON.parse(arg);
            if(obj.status){
                //注册成功---跳转（已登录状态--session实现）
                //alert("注册成功")
                window.location.href = "/home?user="+user;
            }else{
                alert(obj.error);
            }
            }
        });    

            
        
        });
});
