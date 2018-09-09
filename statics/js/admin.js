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
	$('#id_admin_file_download').on('click', function () {
		window.location.href = "/file/download"
	});

	$('#id_admin_file_upload').on('click', function () {
		var fileObj = $("#id_admin_upload_file")[0].files[0]; //获取上传文件名称
		var form = new FormData(); //创建表单对象
		form.append("k1", "v1"); //向表单对象添加name和value
		form.append("file", fileObj); //向表单对象添加name和value,将上传文件名称添加到value
		form.append("_xsrf", getCookie("_xsrf"));
		$.ajax({ //jquery的ajax提交
			type: 'POST',
			url: '/file/upload',
			data: form, //提交数据为表单对象
			processData: false, //默认为 true，数据被处理为 URL 编码格式。如果为 false，则阻止将传入的数据处理为 URL 编码的格式。
			contentType: false, //指 定 请 求 内 容 的 类 型
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					//注册成功---跳转（已登录状态--session实现）
					alert("上传成功");

				} else {
					alert("上传失败");
				}
			}

		});
	});

	$('#id_admin_point_mod').on('click', function () {
		var user_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
		if ((typeof user_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		//console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var user_id = "";
		var user_name = "";
		var user_point = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */
			if ($(this).attr('id') === "user_id") {
				user_id = $(this).text();
				console.log("user_id:" + user_id);
			}

			if ($(this).attr('id') === "user_name") {
				user_name = $(this).text();
				console.log("user_name:" + user_name);
			}

			if ($(this).attr('id') === "user_point") {
				user_point = $(this).text();
				console.log("user_point:" + user_point);
			}
		});

		user_point = prompt("请输入【" + user_name + "】新的积分,当前积分【" + user_point + "】");
		if (user_point === "" || user_point === null) {
			layer.msg("您未输入有效的积分，已为您取消操作。", {
				icon: 2
			});
			return;
		}
		if (isDigitNumber(user_point) === false) {
			layer.msg("只能输入数字，不能输入其他字符！", {
				icon: 2
			});

			return;
		}
		console.log("user_id: " + user_id);
		console.log("user_name: " + user_name);
		console.log("user_point: " + user_point);

		var ret = confirm("是否修改【" + user_name + "】的积分到【" + user_point + "】?");
		if (ret === true) {
			var post_date = {
				"user_id": user_id,
				"user_name": user_name,
				"user_point": user_point,
				"_xsrf": getCookie("_xsrf"),
			};
			$.ajax({
				type: "POST",
				url: "/admin/point",
				data: post_date,
				success: function (arg) {
					console.log(arg);
					var obj = JSON.parse(arg);
					if (obj.status) {
						layer.msg(obj.message, {
							icon: 0
						});

						setTimeout(function () {
							window.location.reload();
						}, 500);
					} else {
						layer.msg(obj.message, {
							icon: 2
						});
					}
				}
			});
		}
	});

});
