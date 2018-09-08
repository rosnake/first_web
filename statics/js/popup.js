var popup_index = 0;

function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}

$(document).ready(function () {
	//弹出一个iframe层
	//标签+属性选择所有<编辑>按钮
	$('#id_home_leave_apply').on('click', function () {
		var user = $('#id_span_home_user_name').val();
		var operation = "apply";
		console.log("leave apply username:"+user);
		if (user == "") {
			layer.msg('用户名不能为空');
		} else {
			console.log(user);
			var index = layer.open({
					type: 2, //iframe 层
					title: '编辑',
					maxmin: true,
					shadeClose: true, //点击遮罩关闭层
					area: ['800px', '520px'],
					//content: '/layer?user='+user
					content: '/layer?user=' + user + '&operation=' + operation
				});
		}
	});

	$('input[value="详细信息"]').click(function () {
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var numId = $('input[value="详细信息"]').index($(this)) + 2;
		console.log(numId);
		//选择表格中的所有tr 通过eq方法取得当前tr
		var ttr = $('table tr').eq(numId);
		console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var user = "";
		var operation = "browse";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */
			if ($(this).children("input[type='checkbox']").length > 0) {
				return;
			}
			if ($(this).children("input[type='button']").length > 0) {
				return;
			}
			if ($(this).children("input[type='text']").length > 0) {
				return;
			}

			var id = $(this).attr('id');
			var tdVal = $(this).html();
			//console.log(id);
			//console.log(tdVal);
			if (id == "id_home_user_name") {
				user = tdVal;
			}
		});

		console.log(user);
		if (user == "") {
			layer.msg('用户名不能为空');
		} else {
			console.log(user);
			var index = layer.open({
					type: 2, //iframe 层
					title: '查看详细信息',
					maxmin: true,
					shadeClose: true, //点击遮罩关闭层
					area: ['800px', '520px'],
					content: '/layer?user=' + user + '&operation=' + operation
				});
		}
	});

	$('#popup').on('click', function () {
		var user = $("#username").val();
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
		var username = words[1];
		var leave_reason = $('#id_popup_leave_apply_reason option:selected').text(); //选中的文本
		var leave_id = $('#id_popup_leave_apply_reason option:selected').val(); //选中的文本
		var leave_date = $('#id_popup_leave_apply_date').val(); //选中的文本
		console.log("user:" + username+" leave_reason:" + leave_reason+" leave_id: " + leave_id+" leave_date:"+ leave_date);

		if ((typeof leave_date) === 'undefined') {
			layer.msg("请选择请假日期");
			console.log("current not select any date");
			return;
		}

		if(leave_date ==="")
		{
			layer.msg("请选择请假日期");
			console.log("current not select any date");
			return;
		}

		var submit_data = {
			"operation": "leave_apply",
			"username": username,
			"leave_id": leave_id,
			"leave_date":leave_date,
			"_xsrf": getCookie("_xsrf")
			};

			console.log("operation:leave_apply,username:"+username+" leave_id:"+leave_id+" leave_date:"+leave_date);

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
						alert("提交成功");
						console.log("username:"+ username);
						window.location.reload();
					} else {
						alert(obj.message);
					}
				},
				error:function(arg) {
					alert("未知的错误");
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
