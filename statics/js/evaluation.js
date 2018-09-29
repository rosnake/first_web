function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}

$(document).ready(function () {
    $('#id_admin_user_issues_evaluation_finish').on('click', function () {
		var issues_object = $('input[name="select_id"]:checked ');
		var issues_id = issues_object.val();
		if ((typeof issues_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}

		var operation = "evaluate_finish";
		console.log("operation:" + operation + " issues_id: " + issues_id);

		var submit_data = {
			"operation": operation,
			"issues_id": issues_id,
			"_xsrf": getCookie("_xsrf")
		};

		$.ajax({
			type: "post",
			url: "/admin/evaluating",
			data: submit_data,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					layer.msg(obj.message);
					console.log("issues_id:" + issues_id);
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

	});


});