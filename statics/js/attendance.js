function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}
function isDigitNumber(inputData) {
	//isNaN(inputData)不能判断空串或一个空格
	//如果是一个空串或是一个空格，而isNaN是做为数字0进行处理的，而parseInt与parseFloat是返回一个错误消息，这个isNaN检查不严密而导致的。
	if (parseFloat(inputData).toString() == "NaN") {
		return false;
	} else {
		return true;
		　　
	}
}

$(document).ready(function () {
	$(".class_admin_context_table_button",this).click(function(){
	    var id =$(this).attr("id");
	    if(id ==="id_admin_attendance_submit") {
            var user = $(this).parents("tr").find("#id_admin_attendance_user_name").html();
		    var operation = "leave_accept";
            console.log("user name:"+ user + " operation:"+operation);

            if (user == "") {
                layer.msg('用户名不能为空');
                return false;
            }
            var submit_data = {
                "operation": operation,
                "user_name": user,
                "_xsrf": getCookie("_xsrf")
            };

            $.ajax({
                type: "post",
                url: "/admin/attendance",
                data: submit_data,
                cache: false,
                success: function (arg) {
                    console.log(arg);
                    //arg是字符串
                    var obj = JSON.parse(arg);
                    if (obj.status) {
                        layer.msg("提交成功");
                        console.log("user:" + user);
                        setTimeout(function () {
                            window.location.reload();
                        }, 1000);
                    } else {
                        layer.msg(obj.message);
                    }
                },
                error: function (arg) {
                    layer.msg("未知的错误");
                }
            });
	    }

	});

	$(".class_admin_context_table_button",this).click(function(){
	    var id =$(this).attr("id");
	    if(id ==="id_admin_attendance_cancel") {
            var user = $(this).parents("tr").find("#id_admin_attendance_user_name").html();
            var operation = "leave_reject";
            console.log("user name:"+ user + " operation:"+operation);

            if (user == "") {
			layer.msg('用户名不能为空');
			return false;
            }
            var submit_data = {
                "operation": operation,
                "user_name": user,
                "_xsrf": getCookie("_xsrf")
            };

            $.ajax({
                type: "post",
                url: "/admin/attendance",
                data: submit_data,
                cache: false,
                success: function (arg) {
                    console.log(arg);
                    //arg是字符串
                    var obj = JSON.parse(arg);
                    if (obj.status) {
                        layer.msg("提交成功");
                        console.log("user:" + user);
                        setTimeout(function () {
                            window.location.reload();
                        }, 1000);
                    } else {
                        layer.msg(obj.message);
                    }
                },
                error: function (arg) {
                    layer.msg("未知的错误");
                }
            });
        }

	});

	$(".class_admin_context_table_button",this).click(function(){
	    var id =$(this).attr("id");
	    if(id ==="id_admin_attendance_sign_in")
        {
            var user = $(this).parents("tr").find("#id_admin_attendance_user_name").html();
            var operation = "sign";
            console.log("user name:"+ user + " operation:"+operation);

            if (user == "") {
                layer.msg('用户名不能为空');
                return false;
		    }

            var submit_data = {
                "operation": operation,
                "user_name": user,
                "_xsrf": getCookie("_xsrf")
            };

            $.ajax({
                type: "post",
                url: "/admin/attendance",
                data: submit_data,
                cache: false,
                success: function (arg) {
                    console.log(arg);
                    //arg是字符串
                    var obj = JSON.parse(arg);
                    if (obj.status) {
                        layer.msg("签到成功");
                        console.log("user:" + user);
                        setTimeout(function () {
                            window.location.reload();
                        }, 1000);
                    } else {
                        layer.msg(obj.message);
                    }
                },
                error: function (arg) {
                    layer.msg("未知的错误");
                }
            });
        }
    });

	$(".class_admin_context_table_button",this).click(function(){
	    var id =$(this).attr("id");
	    if(id ==="id_admin_attendance_absence")
        {
            var user = $(this).parents("tr").find("#id_admin_attendance_user_name").html();

            console.log("absent:" + user);
            if (user == "") {
                layer.msg('用户名不能为空');
                return false;
            }
            $('#id_admin_attendance_popup_user_name').val(user);
            $('#id_admin_attendance_popup_user_name').attr("readonly", true);
            $('#id_admin_attendance_edit_popup_background').show();
        }
	});

	$('#id_admin_attendance_edit_submit').on('click', function () {

		var absent_id = $('#id_admin_popup_absent_reason').val();
		var user_name = $('#id_admin_attendance_popup_user_name').val();

		console.log("user_name:" + user_name + " absent_id:" + absent_id);
		var submit_data = {
			"operation": "absent",
			"absent_id": absent_id,
			"user_name": user_name,
			"_xsrf": getCookie("_xsrf")
		};

		$.ajax({
			type: "post",
			url: "/admin/attendance",
			data: submit_data,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					layer.msg("缺席提交成功");
					console.log("user:" + user_name);
					setTimeout(function () {
						window.location.reload();
					}, 1000);
				} else {
					layer.msg(obj.message);
				}
			},
			error: function (arg) {
				layer.msg("未知的错误");
			}
		});

		$("#id_admin_attendance_edit_operation").val("");
		$("#id_admin_attendance_edit_sub_title").text("");
		$('#id_admin_attendance_edit_popup_background').hide();
	});

	/*select popup*/
	$('#id_admin_attendance_edit_cancel').on('click', function () {
		$("#id_admin_attendance_edit_operation").val("");
		$("#id_admin_attendance_edit_sub_title").text("");
		$('#id_admin_attendance_edit_popup_background').hide();
	});

	$('#id_admin_attendance_start_sign').on('click', function () {
		console.log("id_admin_attendance_start_sign");

		var submit_data = {
			"operation": "start_sign",
			"_xsrf": getCookie("_xsrf")
		};

		$.ajax({
			type: "post",
			url: "/admin/attendance",
			data: submit_data,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					layer.msg("启动签到成功");
					setTimeout(function () {
						window.location.reload();
					}, 1000);
				} else {
					layer.msg(obj.message);
				}
			},
			error: function (arg) {
				layer.msg("未知的错误");
			}
		});
    });

	$('#id_admin_attendance_reset_sign_table').on('click', function () {
		console.log("id_admin_attendance_reset_sign_table");

		layer.confirm("是否复位签到表?", {
			btn: ['复位', '取消']//按钮
		}, function () {
            var submit_data = {
                "operation": "reset_sign_table",
                "_xsrf": getCookie("_xsrf")
            };

            $.ajax({
                type: "post",
                url: "/admin/attendance",
                data: submit_data,
                cache: false,
                success: function (arg) {
                    console.log(arg);
                    //arg是字符串
                    var obj = JSON.parse(arg);
                    if (obj.status) {
                        layer.msg("复位签到表成功");
                        setTimeout(function () {
                            window.location.reload();
                        }, 1000);
                    } else {
                        layer.msg(obj.message);
                    }
                },
                error: function (arg) {
                    layer.msg("未知的错误");
                }
            });

		}, function () {
			layer.msg("复位签到表操作已为您取消", {
				icon: 0
			});
		});

    }); //end of sign table


});
