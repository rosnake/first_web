function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}

function debugMessage(msg) {
	alert(msg);
}

$(document).ready(function () {
	$("#login").click(function () {
		var user = $("#username").val();
		var pwd = $("#password").val();
		var verify_code = $("#verify_code").val();
		var nextname = $("#login").val();
		if(nextname ==="")
		{
			nextname = "/home";

		}

		console.log("nextname:"+nextname);
		var pd = {
			"username": user,
			"password": pwd,
			"next":nextname,
			"verify_code": verify_code,
			"_xsrf": getCookie("_xsrf")
		};
		$.ajax({
			type: "post",
			url: "/login",
			data: pd,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					//注册成功---跳转（已登录状态--session实现）
					alert("登陆成功");
					window.location.href = nextname+"?user=" + user;
				} else {
					alert(obj.message);
					window.location.href = "/login"
				}
			},
			error:function(arg) {
                alert("未知的错误");
                window.location.href = "/login"
            }
		});
	});

	$("#register").click(function () {
		//alert('register')
		var user = $("#username").val();
		var pwd = $("#password").val();
		var conf = $("#confirm").val();

		if (user == "") {
			$("#username").focus();
			debugMessage("用户名不能为空.");
			return false;
		} else {
			//debugMessage("用户名:"+user);
		}
		//验证密码是否合理
		if (pwd.length < 6) {
			$("#password").focus();
			debugMessage("密码不能小于6位数." + pwd.length);
			return false;
		}

		if (pwd == "") {
			$("#password").focus();
			debugMessage("密码不能为空");
			return false;
		}

		//验证密码与确认密码是否相等
		if (pwd != conf) {
			$("#password").focus();
			debugMessage("两次输入密码不一致" + "pwd:" + pwd + "conf:" + conf);
			return false;
		}

		//debugMessage("密码:"+pwd);
		//alert(user);
		var pd = {
			"username": user,
			"password": pwd,
			"confirm": conf,
			"_xsrf": getCookie("_xsrf")
		};

		$.ajax({
			type: "post",
			url: "/register",
			data: pd,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					//注册成功---跳转（已登录状态--session实现）
					alert("注册成功");
					console.log("username:"+user);
					window.location.href = "/user?user=" + user;
				} else {
					alert(obj.message);
				}
			},
			error:function(arg) {
                alert("未知的错误");
            }
		});
	});

	$("#modify_password").click(function () {
		//alert('register')
		var user = $("#username").val();
		var old_password = $("#old_password").val();
		var new_password = $("#new_password").val();
		var conf = $("#confirm").val();

		if (user == "") {
			$("#username").focus();
			debugMessage("用户名不能为空.");
			return false;
		} else {
			//debugMessage("用户名:"+user);
		}
		//验证密码是否合理
		if (old_password.length < 6) {
			$("#password").focus();
			debugMessage("密码不能小于6位数." + pwd.length);
			return false;
		}

		if (new_password.length < 6) {
			$("#new_password").focus();
			debugMessage("新密码不能小于6位数." + pwd.length);
			return false;
		}

		if (new_password == old_password) {
			$("#new_password").focus();
			debugMessage("新密码不能等于老密码.");
			return false;
		}

		if (new_password == "") {
			$("#new_password").focus();
			debugMessage("新密码不能为空");
			return false;
		}

		//验证密码与确认密码是否相等
		if (new_password != conf) {
			$("#new_password").focus();
			debugMessage("两次输入密码不一致" + "pwd:" + new_password + "conf:" + conf);
			return false;
		}

		//debugMessage("密码:"+pwd);
		//alert(user);
		var pd = {
			"username": user,
			"old_password": old_password,
			"new_password": new_password,
			"confirm": conf,
			"_xsrf": getCookie("_xsrf")
		};

		$.ajax({
			type: "post",
			url: "/modify_password",
			data: pd,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					//注册成功---跳转（已登录状态--session实现）
					alert("修改成功")
					window.location.href = "/home?user=" + user;
				} else {
					alert(obj.error);
				}
			}
		});
	});
	$("#id_points_exchange_user").click(function () {
		var selected = $("#id_points_exchange_select option:selected").text(); //获取选中的项
		layer.confirm("是否兑换【" + selected + "】?", {
			btn: ['兑换', '取消']//按钮
		}, function () {
			var pd = {
			"present": selected,
			"_xsrf": getCookie("_xsrf")
		};

		$.ajax({
			type: "post",
			url: "/statistics",
			data: pd,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					layer.msg("兑换成功", {
						icon: 1
					});
					setTimeout(function () {
						window.location.reload();
					}, 1000);
				} else {
					alert(obj.message);
				}
			}
		});


		}, function () {
			layer.msg("兑换【" + selected + "】操作已为您取消", {
				icon: 0
			});
		});
		console.log(selected);
	});

	$("#id_user_other_info_submit").click(function () {
		var user = $("#id_user_other_info_user").val();
		var email = $("#id_user_other_info_email").val();
		var nickname = $("#id_user_other_info_nickname").val();
		var department = $("#id_user_other_info_department").val();

		if (email == "") {
			$("#id_user_other_info_email").focus();
			debugMessage("Email不能为空.");
			return false;
		} else {
			//debugMessage("用户名:"+user);
		}

		if (nickname == "") {
			$("#id_user_other_info_nickname").focus();
			debugMessage("姓名不能为空");
			return false;
		}

		if (department == "") {
			$("#id_user_other_info_department").focus();
			debugMessage("部门不能为空");
			return false;
		}

		var pd = {
			"username": user,
			"email": email,
			"nickname": nickname,
			"department": department,
			"_xsrf": getCookie("_xsrf")
		};

		$.ajax({
			type: "post",
			url: "/user",
			data: pd,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					//注册成功---跳转（已登录状态--session实现）
					alert("提交成功")
					window.location.href = "/index?user=" + user;
				} else {
					alert(obj.error);
				}
			}
		});
    });


});
