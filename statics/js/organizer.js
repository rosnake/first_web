function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}

$(document).ready(function () {

	$('#id_admin_organizer_add').on('click', function () {
		var myDate = new Date();
		var current_date = myDate.getFullYear(); //获取完整的年份(4位,1970-????)
		$('#id_admin_organizer_edit_popup_background').show();
		$('#id_admin_organizer_edit_operation').val("add");
		$('#id_admin_organizer_edit_id').val("0");
		$('#id_admin_organizer_date').text(current_date);
		$("#id_admin_deduct_edit_sub_title").text("增加组织者");

	});

	$('#id_admin_organizer_mod').on('click', function () {
		var organizer_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
		if ((typeof organizer_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}

		$('#id_admin_organizer_edit_popup_background').show();
		$("#id_admin_deduct_edit_sub_title").text("修改组织者");
		var ttr = $("input:checked").parents('tr');
		var organizer_name = "";
		var organizer_id = "";
		var organizer_date = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "organizer_id") {
				organizer_id = $(this).text();
				console.log("organizer_id:" + organizer_id);
			}

			if ($(this).attr('id') === "organizer_name") {
				organizer_name = $(this).text();
				console.log("organizer_name:" + organizer_name);
			}
			if ($(this).attr('id') === "date") {
				organizer_date = $(this).text();
				console.log("organizer_date:" + organizer_date);
			}

		});

		$("#id_admin_organizer_name").val(organizer_name);
		$("#id_admin_organizer_id").val(organizer_id);
		$("#id_admin_organizer_date").val(organizer_date);
	});

	$('#id_admin_organizer_del').on('click', function () {
		var organizer_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
		if ((typeof organizer_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		var ttr = $("input:checked").parents('tr');

		var organizer_name = "";
		var organizer_id = "";
		var time_date = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "organizer_id") {
				organizer_id = $(this).text();
				console.log("organizer_id:" + organizer_id);
			}

			if ($(this).attr('id') === "organizer_name") {
				organizer_name = $(this).text();
				console.log("organizer_name:" + organizer_name);
			}
			if ($(this).attr('id') === "date") {
				time_date = $(this).text();
				console.log("time_date:" + time_date);
			}
		});

		layer.confirm("是否删除【" + organizer_name + "】?", {
			btn: ['删除', '取消']//按钮
		}, function () {
			console.log(" organizer_id: " + organizer_id + " organizer_name: " + organizer_name + " time_date:" + time_date);
			var submit_data = {
				"operation": "delete",
				"organizer_name": organizer_name,
				"organizer_id": organizer_id,
				"time_date": time_date,
				"_xsrf": getCookie("_xsrf")
			};

			$.ajax({
				type: "post",
				url: "/admin/organizer",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						layer.msg("提交成功");
						console.log("organizer_name:" + organizer_name);
						setTimeout(function () {
							window.location.reload();
						}, 1000);
					} else {
						layer.msg(obj.message);
					}
				},
				error: function (arg) {
					var obj = JSON.parse(arg);
					layer.msg(obj.message);
				}
			});

		}, function () {
			layer.msg("删除【" + organizer_name + "】操作已为您取消", {
				icon: 0
			});
		});
	});

	$('#id_admin_popup_organizer_submit').on('click', function () {
		var organizer_name = $("#id_admin_organizer_name").val();
		var organizer_id = $("#id_admin_organizer_id").val();
		var time_date = $('#id_admin_organizer_date').val(); //选中的文本
		console.log(" organizer_id: " + organizer_id + " organizer_name: " + organizer_name + " time_date:" + time_date);

		if (organizer_name == "") {
			$("#id_admin_organizer_name").focus();
			layer.msg("组织者不能为空");
			return false;
		}

		if (organizer_id == "") {
			$("#id_admin_organizer_id").focus();
			layer.msg("组织者ID不能为空");
			return false;
		}

		if (time_date == "") {
			$("#id_admin_organizer_date").focus();
			layer.msg("时间不能为空");
			return false;
		}

		var submit_data = {
			"operation": "update",
			"organizer_name": organizer_name,
			"organizer_id": organizer_id,
			"time_date": time_date,
			"_xsrf": getCookie("_xsrf")
		};

		$.ajax({
			type: "post",
			url: "/admin/organizer",
			data: submit_data,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					layer.msg("提交成功");
					console.log("organizer_name:" + organizer_name);
					setTimeout(function () {
						window.location.reload();
					}, 1000);
				} else {
					layer.msg(obj.message);
				}
			},
			error: function (arg) {
				var obj = JSON.parse(arg);
				layer.msg(obj.message);
			}
		});

		setTimeout(function () {
			window.location.reload();
		}, 1000);
		$('#admin_popup_background').hide();
		$("#id_admin_organizer_name").val("");
		$("#id_admin_organizer_id").val("");
		$("#id_admin_organizer_date").val("");
	});

	$('#id_admin_popup_organizer_cancel').on('click', function () {
		$('#id_admin_organizer_edit_operation').val("");
		$('#id_admin_organizer_edit_id').val("");
		$("#id_admin_organizer_name").val("");
		$("#id_admin_organizer_id").val("");
		$("#id_admin_organizer_date").val("");
		$('#id_admin_organizer_edit_popup_background').hide();
	});
});
