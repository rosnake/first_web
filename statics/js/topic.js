var popup_index = 0;
function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}

$(document).ready(function () {
	//弹出一个iframe层
	$("#applications").click(function () {
		var index = layer.open({
				type: 2, //iframe 层
				title: '议题申报',
				maxmin: true,
				shadeClose: true, //点击遮罩关闭层
				area: ['800px', '520px'],
				//content: '/layer?user='+user
				content: '/issues'
			});
	});

	//弹出一个iframe层
	$("#applications_continue").click(function () {
		var index = layer.open({
				type: 2, //iframe 层
				title: '议题申报',
				maxmin: true,
				shadeClose: true, //点击遮罩关闭层
				area: ['800px', '520px'],
				//content: '/layer?user='+user
				content: '/issues'
			});
	});

	$('#id_applications_confirm').on('click', function () {
		var topic_name = $("#id_input_topic_name").val();
		var topic_brief = $("#id_input_topic_brief").val();
		var topic_date = $('#id_select_topic_date option:selected').text(); //选中的文本
		console.log("topic_name:" + topic_name);
		console.log("topic_brief: " + topic_brief);
		console.log("topic_date: " + topic_date);

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
			"operation": "apply_issues",
			"topic_name": topic_name,
			"topic_brief": topic_brief,
			"topic_date": topic_date,
			"_xsrf": getCookie("_xsrf")
		};

		console.log(" topic_name:" + topic_name + " topic_brief:" + topic_brief + " topic_date:" + topic_date);
		$.ajax({
			type: "post",
			url: "/applications",
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

		var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
		setTimeout(function () {
			parent.layer.close(index);
		}, 800);
		setTimeout(function () {
			window.parent.location.reload();
		}, 1000);
	});

});
