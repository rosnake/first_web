$(document).ready(function () {
	$('#admin_member_add').on('click', function () {
		var member_id = prompt("请输入新的工号.");
		if (member_id === "" || member_id === null) {
			layer.msg("您未输入有效的工号，已为您取消操作。", {
				icon: 2
			});
			return;
		}
		var user_name = prompt("请输入姓名.");
		if (user_name === "" || user_name === null) {
			layer.msg("您未输入有效的姓名，已为您取消操作。", {
				icon: 2
			});
			return;
		}
		var user_role = prompt("请输入角色.");
		if ("admin" !== user_role || "organizer" !== user_role || "normal" !== user_role) {
			layer.msg("您角色输入，有误只能输入[admin、organizer、normal]，已为您取消操作。", {
				icon: 2
			});
			return;
		}
		console.log("member_id: " + member_id);
		console.log("user_name: " + user_name);
		console.log("user_role: " + user_role);
		ret = confirm("是否新增【" + user_name + "】?");
		if (ret === true) {
			alert("新增成功");
		} else {
			alert("取消新增");
		}
		window.location.reload();
	});

	$('#admin_member_del').on('click', function () {
		var member_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
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
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "user_id") {
				var user_id = $(this).text();
				console.log("user_id:" + user_id);
			}

			if ($(this).attr('id') === "user_name") {
				user_name = $(this).text();
				console.log("user_name:" + user_name);
			}

			if ($(this).attr('id') === "user_role") {
				var user_role = $(this).text();
				console.log("user_role:" + user_role);
			}
		});

		ret = confirm("是否删除【" + user_name + "】?");
		if (ret === true) {
			alert("删除成功");
		} else {
			alert("删除取消");
		}
		window.location.reload();
	});

	$('#admin_member_mod').on('click', function () {
		var member_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
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

		member_id = prompt("请输入新的工号,当前工号【" + user_id + "】");
		if (member_id === "" || member_id === null) {
			layer.msg("您未输入有效的工号，已为您取消操作。", {
				icon: 2
			});
			return;
		}
		user_name = prompt("请输入新的用户名,当前用户名【" + user_name + "】");
		if (user_name === "" || user_name === null) {
			layer.msg("您未输入有效的姓名，已为您取消操作。", {
				icon: 2
			});
			return;
		}
		user_role = prompt("请输入新的角色,当前角色【" + user_role + "】");
		if ("admin" !== user_role || "organizer" !== user_role || "normal" !== user_role) {
			layer.msg("您角色输入，有误只能输入[admin、organizer、normal]，已为您取消操作。", {
				icon: 2
			});
			return;
		}

		console.log("member_id: " + member_id);
		console.log("user_name: " + user_name);
		console.log("user_name: " + user_name);
		ret = confirm("是否修改【" + user_name + "】?");
		if (ret === true) {
			alert("修改成功");
		} else {
			alert("取消修改");
		}
		window.location.reload();
	});
});
