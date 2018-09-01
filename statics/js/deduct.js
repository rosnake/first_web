$(document).ready(function () {
	$('#admin_deduct_add').on('click', function () {
		var deduct_name = prompt("请输入扣分项目.");
		if (deduct_name === "" || deduct_name === null) {
			layer.msg("您未输入有效的项目名称，已为您取消操作。", {
				icon: 2
			});
			return;
		}
		var deduct_points = prompt("请输入扣分值.");
		if (deduct_points === "" || deduct_points === null) {
			layer.msg("您未输入有效的扣分值，已为您取消操作。", {
				icon: 2
			});
			return;
		}
		var deduct_id = "0";
		console.log("deduct_id: " + deduct_id);
		console.log("deduct_name: " + deduct_name);
		console.log("deduct_points: " + deduct_points);
		ret = confirm("是否新增【" + deduct_name + "】?");
		if (ret === true) {
			var submit_data = {
			"operation": "add",
			"deduct_name": deduct_name,
			"deduct_points": deduct_points,
			"id":deduct_id,
			"_xsrf": getCookie("_xsrf")
			};

			console.log("operation:add,deduct_name:"+deduct_name+" deduct_points:"+deduct_points+" deduct_id:"+deduct_id);

			$.ajax({
				type: "post",
				url: "/admin/deduct",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						alert("添加成功");
						console.log("deduct_name:"+ deduct_name);
						window.location.reload();
					} else {
						alert(obj.message);
					}
				},
				error:function(arg) {
					alert("未知的错误");
				}
			});

		} else {
			alert("取消新增");
		}
		window.location.reload();
	});

	$('#admin_deduct_del').on('click', function () {
		var deduct_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
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
		var deduct_points = 0;
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "deduct_id") {
				var deduct_id = $(this).val();
				console.log("deduct_id:" + deduct_id);
			}

			if ($(this).attr('id') === "deduct_name") {
				deduct_name = $(this).text();
				console.log("deduct_name:" + deduct_name);
			}

			if ($(this).attr('id') === "deduct_points") {
				 deduct_points = $(this).val();
				console.log("deduct_points:" + deduct_points);
			}
		});

		layer.confirm("是否删除【" + deduct_name + "】?", {
			btn: ['删除', '取消']//按钮
		}, function () {
			var submit_data = {
			"operation": "delete",
			"deduct_name": deduct_name,
			"deduct_points": deduct_points,
			"id":deduct_id,
			"_xsrf": getCookie("_xsrf")
			};

			console.log("operation:add,deduct_name:"+deduct_name+" deduct_points:"+deduct_points+" deduct_id:"+deduct_id);

			$.ajax({
				type: "post",
				url: "/admin/deduct",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						layer.msg("删除成功", {	icon: 1	});
						console.log("deduct_name:"+ deduct_name);
						setTimeout(function () {window.location.reload();}, 1000);
					} else {
						alert(obj.message);
					}
				},
				error:function(arg) {
					alert("未知的错误");
				}
			});

		}, function () {
			layer.msg("删除【" + deduct_name + "】操作已为您取消", {
				icon: 0
			});
		});

		//setTimeout(function () {window.location.reload();}, 1000);
	});

	$('#admin_deduct_mod').on('click', function () {
		var deduct_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
		if ((typeof deduct_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("deduct_id: " + deduct_id);
		console.log("click admin member delete");
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		//console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var deduct_id = "";
		var deduct_points = 0;
		var deduct_name = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "deduct_id") {
				deduct_id = $(this).text();
				console.log("user_id:" + deduct_id);
			}

			if ($(this).attr('id') === "deduct_points") {
				deduct_points = $(this).text();
				console.log("deduct_points:" + deduct_points);
			}

			if ($(this).attr('id') === "deduct_name") {
				deduct_name = $(this).text();
				console.log("deduct_name:" + deduct_name);
			}
		});

		var deduct_new_points = prompt("请输入新的【" + deduct_name + "】扣分值,当前扣分值【" + deduct_points + "】");
		if (deduct_points === "") {
			layer.msg("您未输入有效的扣分值，已为您取消操作。", {
				icon: 2
			});
			return;
		}
		console.log("deduct_id: " + deduct_id);
		console.log("deduct_name: " + deduct_name);
		console.log("deduct_points: " + deduct_new_points);
		ret = confirm("是否修改【" + deduct_name + "】为【" + deduct_new_points + "】?");
		if (ret === true) {
			var submit_data = {
			"operation": "modify",
			"deduct_name": deduct_name,
			"deduct_points": deduct_new_points,
			"id":deduct_id,
			"_xsrf": getCookie("_xsrf")
			};

			console.log("operation:add,deduct_name:"+deduct_name+" deduct_points:"+deduct_points+" deduct_id:"+deduct_id);

			$.ajax({
				type: "post",
				url: "/admin/deduct",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						alert("修改成功");
						console.log("deduct_name:"+ deduct_name);
						window.location.reload();
					} else {
						alert(obj.message);
					}
				},
				error:function(arg) {
					alert("未知的错误");
				}
			});

		} else {
			alert("取消修改");
		}
		window.location.reload();
	});

});
