$(document).ready(function () {
	$('#id_admin_member_add').on('click', function () {
		$('#id_admin_member_edit_user_id').val("0");
		$('#id_admin_member_edit_operation').val("add");
		$('#id_admin_member_edit_popup_background').show();
		$("#id_admin_member_edit_sub_title").text("增加用户");
	});

	$('#id_admin_member_del').on('click', function () {
		var member_id = $('#id_admin_member_table_body input[name="select_id"]:checked ').val();
		if ((typeof member_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("member_id: " + member_id);
		console.log("click admin member delete");
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		//console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var user_name = "";
		var user_role = "";
		var user_id = "";
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

			if ($(this).attr('id') === "user_role") {
				user_role = $(this).text();
				console.log("user_role:" + user_role);
			}
		});

		ret = confirm("是否删除【" + user_name + "】?");
		if (ret === true) {
			var submit_data = {
				"operation": "delete",
				"username": user_name,
				"role": user_role,
				"id": user_id,
				"_xsrf": getCookie("_xsrf")
			};

			console.log("operation:delete,username:" + user_name + " role:" + user_role + " id:" + user_id);

			$.ajax({
				type: "post",
				url: "/admin/member",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						//注册成功---跳转（已登录状态--session实现）
						alert("删除成功");
						console.log("username:" + user_name);
						window.location.reload();
					} else {
						alert(obj.message);
					}
				},
				error: function (arg) {
					alert("未知的错误");
				}
			});

		} else {
			alert("删除取消");
		}
		window.location.reload();
	});

	$('#id_admin_member_mod').on('click', function () {
		var member_id = $('#id_admin_member_table_body input[name="select_id"]:checked ').val();
		if ((typeof member_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("member_id: " + member_id);
		console.log("click admin member delete");
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		//console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var user_name = "";
		var user_id = "";
		var user_role = "";
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

			if ($(this).attr('id') === "user_role") {
				user_role = $(this).text();
				console.log("user_role:" + user_role);
			}
		});

		console.log("user_name: " + user_name);
		console.log("user_role: " + user_role);

		$('#id_admin_member_edit_user_id').val(user_id);
		$('#id_admin_member_edit_operation').val("modify");
		$('#id_admin_member_edit_username').val(user_name);
		$('#id_admin_member_edit_role').val(user_role);
		$("#id_admin_member_edit_username").attr("readonly", true);
		$('#id_admin_member_edit_popup_background').show();
		$("#id_admin_member_edit_sub_title").text("修改用户信息");
		console.log("operation:modify,username:" + user_name + " role:" + user_role + " id:" + user_id);
	});

	$('#id_admin_member_edit_submit').on('click', function () {
		var operation = $("#id_admin_member_edit_operation").val();
		var user_id = $("#id_admin_member_edit_user_id").val();
		var user_name = $("#id_admin_member_edit_username").val();
		var user_role = $("#id_admin_member_edit_role").val();

		if (user_name == "") {
			$("#id_admin_member_edit_username").focus();
			layer.msg("用户名不能为空.");
			return false;
		}

		if (user_name.length < 4) {
			$("#password").focus();
			layer.msg("用户名ID不能小于4个字符");
			return false;
		}
		if (user_role == "") {
			$("#id_admin_member_edit_username").focus();
			layer.msg("用户角色信息不能为空.");
			return false;
		}
		var submit_data = {
			"operation": operation,
			"username": user_name,
			"role": user_role,
			"id": user_id,
			"_xsrf": getCookie("_xsrf")
		};

		console.log("operation:" + operation + " username:" + user_name + " role:" + user_role + " id:" + user_id);
		$.ajax({
			type: "post",
			url: "/admin/member",
			data: submit_data,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					//注册成功---跳转（已登录状态--session实现）
					// alert("修改成功");
					layer.alert("提交成功", {
						skin: 'layui-layer-molv',
						closeBtn: 0
					}, function () {
						window.location.reload();
					});
					console.log("username:" + user_name);

				} else {
					layer.alert(obj.message, {
						skin: 'layui-layer-molv',
						closeBtn: 0
					}, function () {
						window.location.reload();
					});
					//alert(obj.message);
				}
			},
			error: function (arg) {
				alert("未知的错误");
			}
		});

		$("#id_admin_member_edit_user_id").val("");
		$("#id_admin_member_edit_username").val("");
		$('#id_admin_member_edit_operation').val("");
		$('#id_admin_member_edit_popup_background').hide();
		//window.location.reload();

	});

	$('#id_admin_member_show_password').on('click', function () {
		var member_id = $('#id_admin_member_table_body input[name="select_id"]:checked ').val();
		if ((typeof member_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("member_id: " + member_id);
		console.log("click admin member delete");
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		//console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var user_name = "";
		var user_id = "";
		var user_role = "";
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

			if ($(this).attr('id') === "user_role") {
				user_role = $(this).text();
				console.log("user_role:" + user_role);
			}
		});

		var submit_data = {
			"operation": "show_pwd",
			"username": user_name,
			"role": user_role,
			"id": user_id,
			"_xsrf": getCookie("_xsrf")
		};

		console.log("operation:show,username:" + user_name + " role:" + user_role + " id:" + user_id);

		$.ajax({
			type: "post",
			url: "/admin/member",
			data: submit_data,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					//注册成功---跳转（已登录状态--session实现）
					$("#id_admin_member_user_name").val(user_name);
					$("#id_admin_member_pass_word").val(obj.message);
					$('#id_admin_popup_background').show();
					console.log("username:" + user_name);
				} else {
					alert(obj.message);
				}
			},
			error: function (arg) {
				alert("未知的错误");
			}
		});
	});

	$('#id_admin_member_show_close').on('click', function () {
		$("#id_admin_member_user_name").val("");
		$("#id_admin_member_pass_word").val("");
		$('#admin_popup_background').hide();
		window.location.reload();
	});

	$('#id_admin_member_edit_cancel').on('click', function () {
		$("#id_admin_member_edit_user_id").val("");
		$("#id_admin_member_edit_username").val("");
		$('#id_admin_member_edit_operation').val("");
		$('#id_admin_member_edit_popup_background').hide();
		window.location.reload();
	});

});
