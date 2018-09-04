function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}

$(document).ready(function () {

	$('#admin_organizer_add').on('click', function () {

		$('#admin_popup_background').show();
		$("#admin_exchange_popup_sub_title").text("增加组织者");

	});

	$('#admin_organizer_mod').on('click', function () {
		var organizer_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
		if ((typeof organizer_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}

		$('#admin_popup_background').show();
		$("#admin_exchange_popup_sub_title").text("修改组织者");
		var ttr = $("input:checked").parents('tr');
		var organizer_name = "";
		var organizer_id = "";
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
		});

		$("#id_admin_organizer_name").val(organizer_name);
		$("#id_admin_organizer_id").val(organizer_id);

	});

	$('#admin_organizer_del').on('click', function () {
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
	var time_date = $('#id_admin_organizer_date option:selected').text(); //选中的文本
	console.log(" organizer_id: " + organizer_id + " organizer_name: " + organizer_name + " time_date:" + time_date);
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
});
});
