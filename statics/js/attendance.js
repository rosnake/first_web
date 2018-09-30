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
	$('input[value="同意"]').click(function () {
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var numId = $('input[value="同意"]').index($(this)) + 1;
		console.log(numId);
		//选择表格中的所有tr 通过eq方法取得当前tr
		var ttr = $('table tr').eq(numId);
		console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var user = "";
		var operation = "leave_accept";
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
			if (id == "id_admin_attendance_user_name") {
				user = tdVal;
			}
		});

		console.log(user);
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

	});

	$('input[value="驳回"]').click(function () {
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var numId = $('input[value="驳回"]').index($(this)) + 1;
		console.log(numId);
		//选择表格中的所有tr 通过eq方法取得当前tr
		var ttr = $('table tr').eq(numId);
		console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var user = "";
		var operation = "leave_reject";
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
			if (id == "id_admin_attendance_user_name") {
				user = tdVal;
			}
		});

		console.log(user);
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

	});

	$('input[value="已到"]').click(function () {
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var numId = $('input[value="已到"]').index($(this)) + 2;
		console.log(numId);
		//选择表格中的所有tr 通过eq方法取得当前tr
		var ttr = $('table tr').eq(numId);
		console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var user = "";
		var operation = "sign";
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
			if (id == "id_admin_attendance_user_name") {
				user = tdVal;
			}
		});

		console.log(user);
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

	});

	$('input[value="缺席"]').click(function () {
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var numId = $('input[value="缺席"]').index($(this)) + 2;
		console.log(numId);
		//选择表格中的所有tr 通过eq方法取得当前tr
		var ttr = $('table tr').eq(numId);
		console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var user = "";
		var operation = "absent";
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

			if (id == "id_admin_attendance_user_name") {
				user = tdVal;
			}
		});

		console.log("absent:" + user);
		if (user == "") {
			layer.msg('用户名不能为空');
			return false;
		}
		$('#id_admin_attendance_popup_user_name').val(user);
		$('#id_admin_attendance_popup_user_name').attr("readonly", true);
		$('#id_admin_attendance_edit_popup_background').show();

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

});
