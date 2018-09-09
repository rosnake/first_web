function isRealNum(val) {
	// isNaN()函数 把空串 空格 以及NUll 按照0来处理 所以先去除
	if (val === "" || val == null) {
		return false;
	}
	if (!isNaN(val)) {
		return true;
	} else {
		return false;
	}
}

$(document).ready(function () {
	/*admin_exchange_confirm start*/
	$('#admin_exchange_confirm').on('click', function () {
		var exchange_id = $('#admin_user_exchange_table_body input[name="select_id"]:checked ').val();
		if ((typeof exchange_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		var user_name = "";
		var exchange_item = "";
		var exchange_id = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "exchange_id") {
				exchange_id = $(this).text();
				console.log("exchange_id:" + exchange_id);
			}

			if ($(this).attr('id') === "exchange_item") {
				exchange_item = $(this).text();
				console.log("exchange_item:" + exchange_item);
			}

			if ($(this).attr('id') === "user_name") {
				user_name = $(this).text();
				console.log("user_name:" + user_name);
			}
		});

		layer.confirm("是否允许【" + user_name + "】兑换【" + exchange_item + "】?", {
			btn: ['确认', '取消']//按钮
		}, function () {
			//这里放兑换提交
			var submit_data = {
				"operation": "exchange_confirm",
				"exchange_id": exchange_id,
				"user_name": user_name,
				"_xsrf": getCookie("_xsrf")
			};
			console.log("operation: exchange_confirm" + " exchange_id:" + exchange_id + " user_name:" + user_name);
			$.ajax({
				type: "post",
				url: "/admin/exchange",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						layer.msg("提交成功");
						console.log("exchange_item:" + exchange_item);
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
			}); /*end of ajax submit*/

		}, function () {
			layer.msg("兑换【" + exchange_item + "】操作已为您取消", {
				icon: 0
			});
		}); /*end of confirm function*/

	}); /*end of admin_exchange_confirm click*/
	/*admin_exchange_confirm end*/

	/* admin_exchange_cancel start*/
	$('#admin_exchange_cancel').on('click', function () {
		var exchange_id = $('#admin_user_exchange_table_body input[name="select_id"]:checked ').val();
		if ((typeof exchange_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("user_id: " + exchange_id);
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		var user_name = "";
		var exchange_item = "";
		var exchange_id = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "exchange_id") {
				exchange_id = $(this).text();
				console.log("exchange_id:" + exchange_id);
			}

			if ($(this).attr('id') === "exchange_item") {
				exchange_item = $(this).text();
				console.log("exchange_item:" + exchange_item);
			}

			if ($(this).attr('id') === "user_name") {
				user_name = $(this).text();
				console.log("user_name:" + user_name);
			}
		});

		layer.confirm("是否驳回【" + user_name + "】兑换【" + exchange_item + "】的申请?", {
			btn: ['确认', '取消']//按钮
		}, function () {
			//这里放驳回提交
			var submit_data = {
				"operation": "exchange_reject",
				"exchange_id": exchange_id,
				"user_name": user_name,
				"_xsrf": getCookie("_xsrf")
			};

			console.log("operation: exchange_reject" + " exchange_id:" + exchange_id + " user_name:" + user_name);
			$.ajax({
				type: "post",
				url: "/admin/exchange",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						layer.msg("驳回成功");
						console.log("user_name:" + user_name);
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
			}); /*end of ajax submit*/
		}, function () {
			layer.msg("兑换【" + exchange_id + "】操作已为您取消", {
				icon: 0
			});
		});

	}); /*end of admin_exchange_cancel click*/
	/* admin_exchange_cancel end*/

	/*积分规则处理*/

	$('#admin_exchange_add').on('click', function () {
		$('#admin_popup_background').show();
		$("#admin_exchange_popup_sub_title").text("新增规则");
		var rule_id = "无需填写，系统自动生成";
		$("#admin_exchange_popup_rule_id").val(rule_id);
		$("#admin_exchange_popup_rule_id").attr("readonly", true);
	});

	$('#admin_popup_close_button').on('click', function () {
		var rule_id = $("#admin_exchange_popup_rule_id").val();
		var rule_name = $("#admin_exchange_popup_rule_name").val();
		var need_points = $("#admin_exchange_popup_rule_points").val();
		var points_range = $("#admin_exchange_popup_rule_range").val();

		if (rule_id == "") {
			$("#admin_exchange_popup_rule_id").focus();
			layer.msg("ID不能为空");
			return false;
		}

		if (rule_name == "") {
			$("#admin_exchange_popup_rule_name").focus();
			layer.msg("兑换物品不能为空");
			return false;
		}

		if (need_points == "") {
			$("#admin_exchange_popup_rule_points").focus();
			layer.msg("兑换积分不能为空");
			return false;
		}

		if (points_range == "") {
			$("#admin_exchange_popup_rule_range").focus();
			layer.msg("最少兑换积分不能为空");
			return false;
		}

		if (isRealNum(need_points) === false) {
			$("#admin_exchange_popup_rule_points").focus();
			layer.msg("兑换积分只能是数字");
			return false;
		}

		if (isRealNum(points_range) === false) {
			$("#admin_exchange_popup_rule_range").focus();
			layer.msg("最少积分只能是数字");
			return false;
		}

		var operation = "modify";
		if (isRealNum(rule_id) === false) {
			operation = "add";
			rule_id = 0;
		}
		var submit_data = {
			"operation": operation,
			"rule_name": rule_name,
			"need_points": need_points,
			"min_points": points_range,
			"id": rule_id,
			"_xsrf": getCookie("_xsrf")
		};

		console.log("operation:" + operation + " rule_name:" + rule_name + " need_points:" + need_points + " points_range:" + points_range + " rule_id:" + rule_id);
		$.ajax({
			type: "post",
			url: "/admin/exchange",
			data: submit_data,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					layer.msg("提交成功");
					console.log("rule_name:" + rule_name);
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

		$('#admin_popup_background').hide();
		//setTimeout(function () {window.location.reload();}, 1000);
	});

	$('#admin_exchange_del').on('click', function () {
		var rule_id = $('#admin_exchange_table_body input[name="select_id"]:checked ').val();
		if ((typeof rule_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("rule_id: " + rule_id);
		console.log("click admin deduct delete");
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		//console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var rule_id = 0;
		var rule_name = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "rule_id") {
				rule_id = $(this).text();
				console.log("rule_id:" + rule_id);
			}

			if ($(this).attr('id') === "rule_name") {
				rule_name = $(this).text();
				console.log("rule_name:" + rule_name);
			}

		});

		layer.confirm("是否删除【" + rule_name + "】?", {
			btn: ['删除', '取消']//按钮
		}, function () {
			var submit_data = {
				"operation": "delete",
				"rule_name": "null",
				"need_points": "0",
				"min_points": "0",
				"id": rule_id,
				"_xsrf": getCookie("_xsrf")
			};

			console.log("operation:delete" + "rule_id:" + rule_id);
			$.ajax({
				type: "post",
				url: "/admin/exchange",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						layer.msg("删除成功");
						console.log("rule_id:" + rule_id);
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
			layer.msg("删除【" + deduct_name + "】操作已为您取消", {
				icon: 0
			});
		});

	});

	$('#admin_exchange_mod').on('click', function () {
		var rule_id = $('#admin_exchange_table_body input[name="select_id"]:checked ').val();
		if ((typeof rule_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("rule_id: " + rule_id);
		console.log("click admin member delete");
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		//console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var rule_id = "";
		var need_points = "";
		var rule_name = "";
		var points_range = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "rule_id") {
				rule_id = $(this).text();
				console.log("rule_id:" + rule_id);
			}

			if ($(this).attr('id') === "rule_name") {
				rule_name = $(this).text();
				console.log("rule_name:" + rule_name);
			}

			if ($(this).attr('id') === "need_points") {
				need_points = $(this).text();
				console.log("need_points:" + need_points);
			}

			if ($(this).attr('id') === "points_range") {
				points_range = $(this).text();
				console.log("need_points:" + points_range);
			}
		});

		$("#admin_exchange_popup_rule_id").val(rule_id);
		$("#admin_exchange_popup_rule_name").val(rule_name);
		$("#admin_exchange_popup_rule_points").val(need_points);
		$("#admin_exchange_popup_rule_range").val(points_range);
		$("#admin_exchange_popup_rule_id").attr("readonly", true);
		$("#admin_exchange_popup_rule_name").attr("readonly", true);
		$('#admin_popup_background').show();
		$("#admin_exchange_popup_sub_title").text("修改规则");

	});

}); /*end of ready function*/
