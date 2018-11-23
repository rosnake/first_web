var popup_index = 0;

function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}

//判断当前选择时间是否小于是当前实际时间
function contrastTime(select_time) {
	var d = new Date();
	var str = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();//获取当前实际日期
	if (Date.parse(str) > Date.parse(select_time)) {//时间戳对比
	       return true;
	}
	return false;
}

$(document).ready(function () {
	//弹出一个iframe层
	//标签+属性选择所有<编辑>按钮
	$('#id_home_leave_apply').on('click', function () {
		var user = $('#id_span_home_user_name').val();
		var operation = "absent_apply";
		console.log("leave apply user_name:" + user);
		if (user == "") {
			layer.msg('用户名不能为空');
		} else {
			console.log(user);
			var index = layer.open({
					type: 2, //iframe 层
					title: '编辑',
					maxmin: true,
					shadeClose: true, //点击遮罩关闭层
					area: ['800px', '360px'],
					//content: '/layer?user='+user
					content: '/layer?user=' + user + '&operation=' + operation
				});
		}
	});

	$(".class_handle_detail",this).click(function(){
	    var id =$(this).attr("id");
	    if(id ==="id_home_point_detail")
        {
            var user_name = $(this).parents("tr").find("#id_home_user_name").html();
            console.log("user_name:"+user_name)
		    var operation = "detail_browse";

            if (user_name == "") {
			    layer.msg('用户名不能为空');
            } else {
                var index = layer.open({
                        type: 2, //iframe 层
                        title: '查看详细信息',
                        maxmin: true,
                        shadeClose: true, //点击遮罩关闭层
                        area: ['800px', '520px'],
                        content: '/layer?user=' + user_name + '&operation=' + operation
                    });
            }
        }
    });

	$('#popup').on('click', function () {
		var user = $("#user_name").val();
		if (user == "") {
			layer.msg('用户名不能为空');
		} else {
			var index = layer.open({
					type: 2, //iframe 层
					title: '编辑',
					maxmin: true,
					shadeClose: true, //点击遮罩关闭层
					area: ['800px', '520px'],
					content: '/layer?user=' + person
				});
		}
	});

	$('#id_popup_leave_apply_submit').on('click', function () {
		var temp = $("#id_popup_leave_apply_user_name").html();
		var words = temp.split(':');
		var user_name = words[1];
		var leave_reason = $('#id_popup_leave_apply_reason option:selected').text(); //选中的文本
		var leave_id = $('#id_popup_leave_apply_reason option:selected').val(); //选中的文本
		var leave_date = $('#id_popup_leave_apply_date').val(); //选中的文本
		console.log("user:" + user_name + " leave_reason:" + leave_reason + " leave_id: " + leave_id + " leave_date:" + leave_date);

		if ((typeof leave_date) === 'undefined') {
			layer.msg("请选择请假日期");
			console.log("current not select any date");
			return;
		}

		if (leave_date === "") {
			layer.msg("请选择请假日期");
			console.log("current not select any date");
			return;
		}

		if (contrastTime(leave_date) === true){
			$("#id_popup_leave_apply_date").focus();
			console.log("时间不能早于当前时间");
			layer.msg("时间不能早于当前时间");
			return;
		}
		var submit_data = {
			"operation": "absent_apply",
			"user_name": user_name,
			"leave_id": leave_id,
			"leave_date": leave_date,
			"_xsrf": getCookie("_xsrf")
		};

		console.log("operation:leave_apply,user_name:" + user_name + " leave_id:" + leave_id + " leave_date:" + leave_date);

		$.ajax({
			type: "post",
			url: "/home",
			data: submit_data,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					//注册成功---跳转（已登录状态--session实现）
					layer.msg("提交成功");
					console.log("user_name:" + user_name);
					window.location.reload();
				} else {
					layer.msg(obj.message);
				}
			},
			error: function (arg) {
				layer.msg("未知的错误");
			}
		});

		var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
		parent.layer.close(index); //再执行关闭
	});

	$('#popup_back').on('click', function () {
		var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
		parent.layer.close(index); //再执行关闭
	});
});
