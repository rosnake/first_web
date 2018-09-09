function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}
function isDigitNumber(inputData) {
	//isNaN(inputData)不能判断空串或一个空格
	//如果是一个空串或是一个空格，而isNaN是做为数字0进行处理的，而parseInt与parseFloat是返回一个错误消息，这个isNaN检查不严密而导致的。
	if (parseFloat(inputData).toString() == "NaN") {
		return false;
	} else {
		return true;
		　　
	}
}

$(document).ready(function () {
   $('#id_admin_meeting_mod').on('click', function () {
		var tpoic_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
		if ((typeof tpoic_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		//console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var topic_id = "";
		var user_name = "";
		var meeting_room = "";
		var meeting_date = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "topic_id") {
				topic_id = $(this).text();
				console.log("topic_id:" + topic_id);
			}

			if ($(this).attr('id') === "user_name") {
				user_name = $(this).text();
				console.log("user_name:" + user_name);
			}

			if ($(this).attr('id') === "meeting_room") {
				meeting_room = $(this).text();
				console.log("meeting_room:" + meeting_room);
			}

			if ($(this).attr('id') === "meeting_date") {
				meeting_date = $(this).text();
				console.log("meeting_date:" + meeting_date);
			}
		});

		$("#id_admin_meeting_topic_id").val(topic_id);
		$("#id_admin_meeting_user_name").val(user_name);
		$("#id_admin_meeting_meeting_room").val(meeting_room);
		$("#id_admin_meeting_meeting_date").val(meeting_date);

		$("#id_admin_meeting_topic_id").attr("readonly", true);
		$('#admin_popup_background').show();
		$("#id_admin_meeting_sub_title").text("修改会议信息");

	});

      $('#id_admin_meeting_add').on('click', function () {

		$('#admin_popup_background').show();
		$("#id_admin_meeting_sub_title").text("增加会议信息");

	});


	$('#id_admin_meeting_submit').on('click', function () {
		var topic_id = $("#id_admin_meeting_topic_id").val();
		var user_name = $("#id_admin_meeting_user_name").val();
		var meeting_room = $("#id_admin_meeting_meeting_room").val();
		var meeting_date = $("#id_admin_meeting_meeting_date").val();

		console.log(" topic_id: " + topic_id+" user_name: " + user_name+
			" meeting_date: " + meeting_date+" meeting_room: " + meeting_room);

		var submit_data = {
			"operation": "modify",
			"topic_id": topic_id,
			"user_name": user_name,
			"meeting_room":meeting_room,
			"meeting_date":meeting_date,
			"_xsrf": getCookie("_xsrf")
			};

		$.ajax({
			type: "post",
			url: "/admin/meeting",
			data: submit_data,
			cache: false,
			success: function (arg) {
				console.log(arg);
				//arg是字符串
				var obj = JSON.parse(arg);
				if (obj.status) {
					layer.msg("修改成功");
					console.log("topic_id:"+ topic_id);
					setTimeout(function () {window.location.reload();}, 1000);
				} else {
					layer.msg(obj.message);
				}
			},
			error:function(arg) {
				console.log(arg);
				layer.msg("未知的错误");
			}
		});

		$('#admin_popup_background').hide();
	});

});