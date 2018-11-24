function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}

$(document).ready(function () {
	$('#id_admin_user_topic_designate').on('click', function () {
		var index = layer.open({
				type: 2, //iframe 层
				title: '指定议题',
				maxmin: true,
				shadeClose: true, //点击遮罩关闭层
				area: ['800px', '520px'],
				content: '/admin/issues?type=designate'
			});
	});

	$('#id_admin_user_topic_invitation').on('click', function () {
		var index = layer.open({
				type: 2, //iframe 层
				title: '特邀议题',
				maxmin: true,
				shadeClose: true, //点击遮罩关闭层
				area: ['800px', '520px'],
				content: '/admin/issues?type=invitation'
			});
	});

	$('#id_admin_user_topic_del').on('click', function () {
		var issues_object = $('input[name="select_id"]:checked ');
		var issues_id = issues_object.val();
		if ((typeof issues_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		var root_div_obj = issues_object.parents('div').parents('div');
		var father_div_obj = root_div_obj.children('div');

		var admin_topic_user_name = father_div_obj.children('div').children('#id_admin_topic_user_name').html();
		var admin_topic_title = father_div_obj.children('div').children('#id_admin_topic_title').html();
		var topic_brief = "null";
		var topic_date = "null";
		console.log("issues_id: " + issues_id);
		console.log("admin_topic_title: " + admin_topic_title);
		console.log("admin_topic_user_name: " + admin_topic_user_name);
		console.log("click admin topics delete");
		layer.confirm("是否删除【" + admin_topic_title + "】?", {
			btn: ['删除', '取消']//按钮
		}, function () {
			var submit_data = {
				"operation": "delete",
				"topic_user": admin_topic_user_name,
				"topic_name": admin_topic_title,
				"topic_brief": topic_brief,
				"topic_date": topic_date,
				"issues_id": issues_id,
				"_xsrf": getCookie("_xsrf")
			};

			console.log("topic_user:" + admin_topic_user_name + " topic_name:" + admin_topic_title + " topic_brief:" + topic_brief + " topic_date:" + topic_date);
			$.ajax({
				type: "post",
				url: "/admin/topics",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						layer.msg("删除成功");
						console.log("topic_name:" + admin_topic_title);
						setTimeout(function () {
							window.location.reload();
						}, 1000);
					} else {
						layer.msg(obj.message);
					}
				},
				error: function (arg) {
					console.log(arg);
					layer.msg("未知的错误");
				}
			});

		}, function () {
			layer.msg("删除【" + admin_topic_title + "】操作已为您取消", {
				icon: 0
			});
		});

	});

	$('#id_admin_user_topic_mod').on('click', function () {
		var issues_object = $('input[name="select_id"]:checked ');
		var issues_id = issues_object.val();
		if ((typeof issues_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		var admin_topic_user_name = issues_object.parents('div').children('#id_admin_topic_user_name').html();
		var admin_topic_title = issues_object.parents('div').children('.topic_details').children('#id_admin_topic_title').html();

		console.log("issues_id: " + issues_id);
		console.log("admin_topic_title: " + admin_topic_title);
		console.log("admin_topic_user_name: " + admin_topic_user_name);
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
		var topic_user = $("#id_input_topic_user").val();
		var topic_name = $("#id_input_topic_name").val();
		var topic_brief = $("#id_input_topic_brief").val();
		var topic_date = $("#id_admin_issues_date").val();
		var issues_id = 0;
        var issues_type = $('#id_admin_issues_type').html();

		var check_user = $('#'+topic_user).html();
		console.log("check_user:"+check_user+" issues_type:"+issues_type);

		if(check_user ==null && issues_type === "designate")
        {
            $("#id_input_topic_user").focus();
            layer.msg("系统找不到该用户");
            return false;
        }

		if (topic_user === "") {
			$("#id_input_topic_user").focus();
			layer.msg("主讲人不能为空");
			return false;
		}

		if (topic_name === "") {
			$("#id_input_topic_name").focus();
			layer.msg("议题不能为空");
			return false;
		}

		if (topic_brief === "") {
			$("#id_input_topic_brief").focus();
			layer.msg("议题简介不能为空");
			return false;
		}

		if (topic_date === "") {
			$("#id_select_topic_date").focus();
			layer.msg("议题时间不能为空");
			return false;
		}

		var submit_data = {
			"operation": "add",
			"topic_user": topic_user,
			"topic_name": topic_name,
			"topic_brief": topic_brief,
			"topic_date": topic_date,
			"issues_id": issues_id,
            "issues_type":issues_type,
			"_xsrf": getCookie("_xsrf")
		};

		console.log("topic_user:" + topic_user + " topic_name:" + topic_name + " topic_brief:" + topic_brief + " topic_date:" + topic_date);
		$.ajax({
			type: "post",
			url: "/admin/topics",
			data: submit_data,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					layer.msg("提交成功");
					console.log("topic_name:" + topic_name);
				} else {
					layer.msg(obj.message);
				}
			},
			error: function (arg) {
				console.log(arg);
				layer.msg("未知的错误");
			}
		});

		setTimeout(function () {
			window.parent.location.reload();
		}, 1000);
		var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
		setTimeout(function () {
			parent.layer.close(index);
		}, 800);

	});

	$('#id_admin_mod_issues_confirm').on('click', function () {
		var issues_id = $("#id_admin_mod_issues").val();
		var topic_user = $("#id_input_topic_user").val();
		var topic_name = $("#id_input_topic_name").val();
		var topic_brief = $("#id_input_topic_brief").val();
		var topic_date = $("#id_admin_issues_modify_date").val();

		if (topic_user === "") {
			$("#id_input_topic_user").focus();
			layer.msg("主讲人不能为空");
			return false;
		}

		if (topic_name === "") {
			$("#id_input_topic_name").focus();
			layer.msg("议题不能为空");
			return false;
		}

		if (topic_brief === "") {
			$("#id_input_topic_brief").focus();
			layer.msg("议题简介不能为空");
			return false;
		}

		if (topic_date === "") {
			$("#id_select_topic_date").focus();
			layer.msg("议题时间不能为空");
			return false;
		}

		var submit_data = {
			"operation": "modify",
			"topic_user": topic_user,
			"topic_name": topic_name,
			"topic_brief": topic_brief,
			"topic_date": topic_date,
			"issues_id": issues_id,
			"_xsrf": getCookie("_xsrf")
		};

		console.log("issues_id" + issues_id + " topic_user:" + topic_user + " topic_name:" + topic_name + " topic_brief:" + topic_brief + " topic_date:" + topic_date);
		$.ajax({
			type: "post",
			url: "/admin/topics",
			data: submit_data,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					layer.msg("修改成功");
					console.log("topic_name:" + topic_name);
					setTimeout(function () {
						window.parent.location.reload();
					}, 1000);
				} else {
					layer.msg(obj.message);
				}
			},
			error: function (arg) {
				console.log(arg);
				layer.msg("未知的错误");
			}
		});

		setTimeout(function () {
			window.parent.location.reload();
		}, 1000);
		var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
		setTimeout(function () {
			parent.layer.close(index);
		}, 800);
		//再执行关闭
	});

	$('#id_admin_add_issues_cancel').on('click', function () {
		var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
		parent.layer.close(index);
		window.parent.location.reload();

	});

	$('#id_admin_mod_issues_cancel').on('click', function () {
		var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
		parent.layer.close(index);
		window.parent.location.reload();

	});
	/*
	$('#admin_organizer_add').on('click', function () {
	$('#admin_popup_background').show();
	$("#admin_exchange_popup_sub_title").text("增加组织者");
	});
	$('#id_admin_popup_organizer_submit').on('click', function () {
	$('#admin_popup_background').hide();
	});
	 */
});
