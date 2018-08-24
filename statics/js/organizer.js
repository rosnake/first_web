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

			$("#id_admin_organizer_name").val(organizer_name);
			$("#id_admin_organizer_id").val(organizer_id);
		});
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
		layer.confirm("是否删除【" + organizer_name + "】?", {
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
			layer.msg("删除【" + organizer_name + "】操作已为您取消", {
				icon: 0
			});
		});
	});

	$('#id_admin_popup_organizer_submit').on('click', function () {
		var organizer_name = $("#id_admin_organizer_name").val();
		var organizer_id = $("#id_admin_organizer_id").val();

		console.log("organizer_id: " + organizer_id);
		console.log("organizer_name: " + organizer_name);

		setTimeout(function () {
			window.location.reload();
		}, 1000);
		$('#admin_popup_background').hide();
	});
});
