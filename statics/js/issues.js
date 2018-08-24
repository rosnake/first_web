$(document).ready(function () {
	$('#admin_user_topic_add').on('click', function () {
		var index = layer.open({
				type: 2, //iframe 层
				title: '增加议题',
				maxmin: true,
				shadeClose: true, //点击遮罩关闭层
				area: ['800px', '520px'],
				//content: '/layer?user='+user
				content: '/admin/issues'
			});
	});

	$('#admin_user_topic_del').on('click', function () {
		var issues_object = $('input[name="select_id"]:checked ');
		var issues_id = issues_object.val();
		if ((typeof issues_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		var admin_topic_username = issues_object.parents('div').children('#id_admin_topic_user_name').html();
		var admin_topic_title = issues_object.parents('div').children('.topic_details').children('#id_admin_topic_title').html();

		console.log("issues_id: " + issues_id);
		console.log("admin_topic_title: " + admin_topic_title);
		console.log("admin_topic_username: " + admin_topic_username);
		console.log("click admin topics delete");
		layer.confirm("是否删除【" + admin_topic_title + "】?", {
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
			layer.msg("删除【" + admin_topic_title + "】操作已为您取消", {
				icon: 0
			});
		});

	});

	$('#admin_user_topic_mod').on('click', function () {
		var issues_object = $('input[name="select_id"]:checked ');
		var issues_id = issues_object.val();
		if ((typeof issues_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		var admin_topic_username = issues_object.parents('div').children('#id_admin_topic_user_name').html();
		var admin_topic_title = issues_object.parents('div').children('.topic_details').children('#id_admin_topic_title').html();

		console.log("issues_id: " + issues_id);
		console.log("admin_topic_title: " + admin_topic_title);
		console.log("admin_topic_username: " + admin_topic_username);
		console.log("click admin topics modify");

		var index = layer.open({
				type: 2, //iframe 层
				title: '增加议题',
				maxmin: true,
				shadeClose: true, //点击遮罩关闭层
				area: ['800px', '520px'],
				//content: '/layer?user='+user
				content: '/admin/issues_modify?issues_id=' + issues_id
			});

	});

	$('#id_admin_add_issues_confirm').on('click', function () {

		var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
		parent.layer.close(index); //再执行关闭
	});

	$('#admin_organizer_add').on('click', function () {
		$('#admin_popup_background').show();
		$("#admin_exchange_popup_sub_title").text("增加组织者");
	});
	$('#id_admin_popup_organizer_submit').on('click', function () {
		$('#admin_popup_background').hide();
	});
});
