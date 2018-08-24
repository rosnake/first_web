$(document).ready(function () {

	$('#admin_exchange_confirm').on('click', function () {
		var user_id = $('#admin_user_exchange_table_body input[name="select_id"]:checked ').val();
		if ((typeof user_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("user_id: " + user_id);
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		var user_name = "";
		var exchange_item = "";
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
			layer.msg("兑换成功", {
				icon: 1
			});
			setTimeout(function () {
				window.location.reload();
			}, 1000);
		}, function () {
			layer.msg("兑换【" + deduct_name + "】操作已为您取消", {
				icon: 0
			});
		});

	});

	$('#admin_exchange_cancel').on('click', function () {
		var user_id = $('#admin_user_exchange_table_body input[name="select_id"]:checked ').val();
		if ((typeof user_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("user_id: " + user_id);
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		var user_name = "";
		var exchange_item = "";
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
			layer.msg("驳回成功", {
				icon: 1
			});
			setTimeout(function () {
				window.location.reload();
			}, 1000);
		}, function () {
			layer.msg("兑换【" + deduct_name + "】操作已为您取消", {
				icon: 0
			});
		});
	});
	/*积分规则处理*/

	$('#admin_exchange_add').on('click', function () {
		$('#admin_popup_background').show();
		$("#admin_exchange_popup_sub_title").text("新增规则");
	});

	$('#admin_popup_close_button').on('click', function () {
		var rule_id = $("#admin_exchange_popup_rule_id").val();
		var rule_name = $("#admin_exchange_popup_rule_name").val();
		var need_points = $("#admin_exchange_popup_rule_points").val();
		var points_range = $("#admin_exchange_popup_rule_range").val();

		console.log("rule_id: " + rule_id);
		console.log("rule_name: " + rule_name);
		console.log("need_points: " + need_points);
		console.log("points_range: " + points_range);
		setTimeout(function () {
			window.location.reload();
		}, 1000);
		$('#admin_popup_background').hide();
	});

	$('#admin_exchange_del').on('click', function () {
		var deduct_id = $('#admin_exchange_table_body input[name="select_id"]:checked ').val();
		if ((typeof deduct_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("deduct_id: " + deduct_id);
		console.log("click admin deduct delete");
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		//console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var deduct_name = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "deduct_id") {
				var deduct_id = $(this).text();
				console.log("deduct_id:" + deduct_id);
			}

			if ($(this).attr('id') === "deduct_name") {
				deduct_name = $(this).text();
				console.log("deduct_name:" + deduct_name);
			}

			if ($(this).attr('id') === "deduct_points") {
				var deduct_points = $(this).text();
				console.log("deduct_points:" + deduct_points);
			}
		});

		//ret = confirm("是否删除【"+deduct_name+"】?");
		layer.confirm("是否删除【" + deduct_name + "】?", {
			btn: ['删除', '取消']//按钮
		}, function () {
			//这里放删除提交
			layer.msg("删除成功", {
				icon: 1
			});
			setTimeout(function () {
				window.location.reload();
			}, 1000);

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
});
