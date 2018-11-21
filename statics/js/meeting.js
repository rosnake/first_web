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

//判断当前选择时间是否小于是当前实际时间
function contrastTime(select_time) {
	var d = new Date();
	var str = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();//获取当前实际日期
	if (Date.parse(str) > Date.parse(select_time)) {//时间戳对比
	       return true;
	}
	return false;
}

$(document).ready(function () {
	$('#id_admin_meeting_mod').on('click', function () {
		var issues_id = $('#id_admin_meeting_table_body input[name="select_id"]:checked ').val();
		if ((typeof issues_id) === 'undefined') {
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
		var issues_id = "";
		var keynote_user_name = "";
		var meeting_room = "";
		var meeting_date = "";
		var issues_title = "";
		var current_issues_flags = "";

		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "id_meeting_issues_id") {
				issues_id = $(this).text();
				console.log("issues_id:" + issues_id);
			}

			if ($(this).attr('id') === "id_meeting_keynote_user_name") {
				keynote_user_name = $(this).text();
				console.log("user_name:" + keynote_user_name);
			}

			if ($(this).attr('id') === "id_meeting_room") {
				meeting_room = $(this).text();
				console.log("meeting_room:" + meeting_room);
			}

			if ($(this).attr('id') === "id_meeting_date") {
				meeting_date = $(this).text();
				console.log("meeting_date:" + meeting_date);
			}

			if ($(this).attr('id') === "id_meeting_issues_title") {
				issues_title = $(this).text();
				console.log("issues_title:" + issues_title);
			}

			if ($(this).attr('id') === "id_meeting_issues_current_flags") {
				current_issues_flags = $(this).text();
				console.log("current_issues_flags:" + current_issues_flags);
			}
		});

		if (current_issues_flags == "True")
        {
            console.log(" is current issues,can not modify it");
            return;
        }
        var now = new Date();
        //格式化日，如果小于9，前面补0
        var day = ("0" + now.getDate()).slice(-2);
        //格式化月，如果小于9，前面补0
        var month = ("0" + (now.getMonth() + 1)).slice(-2);
        //拼装完整日期格式
        var today = now.getFullYear()+"-"+(month)+"-"+(day) ;

        console.log(today);

        var strArray = meeting_date.split(" ");
        var date_time = strArray[0];
        if (contrastTime(date_time) === true){
			date_time = today;
		}

		$("#id_admin_meeting_issues_id").val(issues_id);
		$('#id_admin_meeting_issues_title').val(issues_title);
		$("#id_admin_meeting_keynote_user_name").val(keynote_user_name);
		$("#id_admin_meeting_meeting_room").val(meeting_room);
		$("#id_admin_meeting_meeting_date").val(date_time);
		$("#id_admin_meeting_issues_operation").val("modify");
		$("#id_admin_meeting_issues_id").attr("readonly", true);
		$('#id_admin_meeting_edit_popup_background').show();
		$("#id_admin_meeting_edit_popup_title").text("修改会议信息");

	});

	$('#id_admin_meeting_add').on('click', function () {

		$('#id_meeting_select_popup_background').show();
		$("#id_meeting_select_popup_title").text("增加会议信息");

	});

	$('#id_admin_meeting_popup_edit_submit').on('click', function () {
		var operation = $("#id_admin_meeting_issues_operation").val();
		var issues_id = $("#id_admin_meeting_issues_id").val();
		var keynote_user_name = $("#id_admin_meeting_keynote_user_name").val();
		var meeting_room = $("#id_admin_meeting_meeting_room").val();
		var meeting_date = $("#id_admin_meeting_meeting_date").val();
		var issues_title = $('#id_admin_meeting_issues_title').val();
		console.log("operation:" + operation + " issues_id: " + issues_id + " keynote_user_name: " + keynote_user_name +
			" meeting_date: " + meeting_date + " meeting_room: " + meeting_room);

		if (keynote_user_name == "") {
			$("#id_admin_meeting_keynote_user_name").focus();
			layer.msg("用户名不能为空");
			return false;
		}

		if (meeting_room == "") {
			$("#id_admin_meeting_meeting_room").focus();
			layer.msg("会议室不能为空");
			return false;
		}

		if (meeting_date == "") {
			$("#id_admin_meeting_meeting_date").focus();
			layer.msg("时间不能为空");
			return false;
		}
		if (contrastTime(meeting_date) === true){
			$("#id_popup_leave_apply_date").focus();
			console.log("时间不能早于当前时间");
			layer.msg("时间不能早于当前时间");
			return false;
		}

		if (issues_title == "") {
			$("#id_admin_meeting_issues_title").focus();
			layer.msg("会议议题不能为空");
			return false;
		}
		var submit_data = {
			"operation": operation,
			"issues_id": issues_id,
			"keynote_user_name": keynote_user_name,
			"meeting_room": meeting_room,
			"meeting_date": meeting_date,
			"issues_title": issues_title,
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
					layer.msg("提交成功");
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

		$("#id_admin_meeting_issues_operation").val("");
		$("#id_admin_meeting_issues_id").val("");
		$("#id_admin_meeting_keynote_user_name").val("");
		$('#id_admin_meeting_issues_title').val("");
		$('#id_admin_meeting_meeting_room').val("");
		$('#id_admin_meeting_meeting_date').val("");
		$("#id_admin_meeting_edit_popup_title").text("");
		$('#id_admin_meeting_edit_popup_background').hide();
	});

	$('#id_admin_meeting_set_current').on('click', function () {
		var issues_id = $('#id_admin_meeting_table_body input[name="select_id"]:checked ').val();
		if ((typeof issues_id) === 'undefined') {
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
		var issues_id = "";
		var keynote_user_name = "";
		var meeting_room = "";
		var meeting_date = "";
		var issues_title = "";

		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "id_meeting_issues_id") {
				issues_id = $(this).text();
				console.log("issues_id:" + issues_id);
			}

			if ($(this).attr('id') === "id_meeting_keynote_user_name") {
				keynote_user_name = $(this).text();
				console.log("user_name:" + keynote_user_name);
			}

			if ($(this).attr('id') === "id_meeting_room") {
				meeting_room = $(this).text();
				console.log("meeting_room:" + meeting_room);
			}

			if ($(this).attr('id') === "id_meeting_date") {
				meeting_date = $(this).text();
				console.log("meeting_date:" + meeting_date);
			}

			if ($(this).attr('id') === "id_meeting_issues_title") {
				issues_title = $(this).text();
				console.log("issues_title:" + issues_title);
			}
		});

		var operation = "set_current";
		console.log("operation:" + operation + " issues_id: " + issues_id + " keynote_user_name: " + keynote_user_name +
			" meeting_date: " + meeting_date + " meeting_room: " + meeting_room);

		var submit_data = {
			"operation": operation,
			"issues_id": issues_id,
			"keynote_user_name": keynote_user_name,
			"meeting_room": meeting_room,
			"meeting_date": meeting_date,
			"issues_title": issues_title,
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
					layer.msg("提交成功");
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

	$('#id_admin_meeting_popup_edit_cancel').on('click', function () {
		$("#id_admin_meeting_issues_operation").val("");
		$("#id_admin_meeting_issues_id").val("");
		$("#id_admin_meeting_keynote_user_name").val("");
		$('#id_admin_meeting_issues_title').val("");
		$('#id_admin_meeting_meeting_room').val("");
		$('#id_admin_meeting_meeting_date').val("");
		$("#id_admin_meeting_edit_popup_title").text("");
		$('#id_admin_meeting_edit_popup_background').hide();
	});

	/*select popup*/
	$('#id_admin_meeting_select_confirm').on('click', function () {
		var issues_id = $('#id_admin_meeting_select_table_body input[name="select_id"]:checked ').val();
		if ((typeof issues_id) === 'undefined') {
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
		var issues_id = "";
		var keynote_user_name = "";
		var issues_title = "";
		var issues_date_time = "";

		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "id_meeting_add_issues_id") {
				issues_id = $(this).text();
				console.log("issues_id:" + issues_id);
			}

			if ($(this).attr('id') === "id_meeting_add_keynote_user_name") {
				keynote_user_name = $(this).text();
				console.log("keynote_user_name:" + keynote_user_name);
			}

			if ($(this).attr('id') === "id_meeting_add_issues_title") {
				issues_title = $(this).text();
				console.log("issues_title:" + issues_title);
			}

			if ($(this).attr('id') === "id_meeting_add_issues_date_time") {
				issues_date_time = $(this).text();
				console.log("issues_date_time:" + issues_date_time);
			}
		});

        var now = new Date();
        //格式化日，如果小于9，前面补0
        var day = ("0" + now.getDate()).slice(-2);
        //格式化月，如果小于9，前面补0
        var month = ("0" + (now.getMonth() + 1)).slice(-2);
        //拼装完整日期格式
        var today = now.getFullYear()+"-"+(month)+"-"+(day) ;

        console.log(today);

        var strArray = issues_date_time.split(" ");
        var date_time = strArray[0];
        if (contrastTime(date_time) === true){
			date_time = today;
		}

		$("#id_admin_meeting_issues_operation").val("add");
		$("#id_admin_meeting_issues_id").val(issues_id);
		$("#id_admin_meeting_keynote_user_name").val(keynote_user_name);
		$('#id_admin_meeting_issues_title').val(issues_title);
		$('#id_admin_meeting_meeting_date').val(date_time);
		$("#id_admin_meeting_issues_id").attr("readonly", true);
		$("#id_admin_meeting_keynote_user_name").attr("readonly", true);
		$('#id_meeting_select_popup_background').hide();
		$('#id_admin_meeting_edit_popup_background').show();
		$("#id_admin_meeting_edit_popup_title").text("增加会议信息");

	});

	$('#id_admin_meeting_select_cancel').on('click', function () {
		console.log("id_admin_meeting_select_cancel");
		$('#id_meeting_select_popup_background').hide();
	});

	$('#id_admin_meeting_del').on('click', function () {
		var issues_id = $('#id_admin_meeting_table_body input[name="select_id"]:checked ').val();
		if ((typeof issues_id) === 'undefined') {
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
		var issues_id = "";
		var keynote_user_name = "";
		var meeting_room = "";
		var meeting_date = "";
		var issues_title = "";
        var current_issues_flags = "";

		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "id_meeting_issues_id") {
				issues_id = $(this).text();
				console.log("issues_id:" + issues_id);
			}

			if ($(this).attr('id') === "id_meeting_keynote_user_name") {
				keynote_user_name = $(this).text();
				console.log("user_name:" + keynote_user_name);
			}

			if ($(this).attr('id') === "id_meeting_room") {
				meeting_room = $(this).text();
				console.log("meeting_room:" + meeting_room);
			}

			if ($(this).attr('id') === "id_meeting_date") {
				meeting_date = $(this).text();
				console.log("meeting_date:" + meeting_date);
			}

			if ($(this).attr('id') === "id_meeting_issues_title") {
				issues_title = $(this).text();
				console.log("issues_title:" + issues_title);
			}

			if ($(this).attr('id') === "id_meeting_issues_current_flags") {
				current_issues_flags = $(this).text();
				console.log("current_issues_flags:" + current_issues_flags);
			}
		});

		if (current_issues_flags == "True")
        {
            console.log(" is current issues,can not delete it");
            return;
        }

		var operation = "del";
		console.log("operation:" + operation + " issues_id: " + issues_id + " keynote_user_name: " + keynote_user_name +
			" meeting_date: " + meeting_date + " meeting_room: " + meeting_room);

		layer.confirm("是否删除【" + issues_title + "】?", {
			btn: ['删除', '取消']//按钮
		}, function () {
		var submit_data = {
			"operation": operation,
			"issues_id": issues_id,
			"keynote_user_name": keynote_user_name,
			"meeting_room": meeting_room,
			"meeting_date": meeting_date,
			"issues_title": issues_title,
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

		}, function () {
			layer.msg("删除【" + issues_title + "】操作已为您取消", {
				icon: 0
			});
		});
	});

	$('#id_admin_meeting_set_finish').on('click', function () {
		var issues_id = $('#id_admin_meeting_table_body input[name="select_id"]:checked ').val();
		if ((typeof issues_id) === 'undefined') {
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
		var issues_id = "";
		var keynote_user_name = "";
		var meeting_room = "";
		var meeting_date = "";
		var issues_title = "";
		var current_issues_flags = "";

		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "id_meeting_issues_id") {
				issues_id = $(this).text();
				console.log("issues_id:" + issues_id);
			}

			if ($(this).attr('id') === "id_meeting_keynote_user_name") {
				keynote_user_name = $(this).text();
				console.log("user_name:" + keynote_user_name);
			}

			if ($(this).attr('id') === "id_meeting_room") {
				meeting_room = $(this).text();
				console.log("meeting_room:" + meeting_room);
			}

			if ($(this).attr('id') === "id_meeting_date") {
				meeting_date = $(this).text();
				console.log("meeting_date:" + meeting_date);
			}

			if ($(this).attr('id') === "id_meeting_issues_title") {
				issues_title = $(this).text();
				console.log("issues_title:" + issues_title);
			}

			if ($(this).attr('id') === "id_meeting_issues_current_flags") {
				current_issues_flags = $(this).text();
				console.log("current_issues_flags:" + current_issues_flags);
			}

		});

		if (current_issues_flags == "False")
        {
            console.log(" is not current issues,can not set it");
            return;
        }

        if (contrastTime(meeting_date) === false){
			layer.msg("议题时间未到，不能结束");
			return false;
		}

		var operation = "issues_finish";
		console.log("operation:" + operation + " issues_id: " + issues_id + " keynote_user_name: " + keynote_user_name +
			" meeting_date: " + meeting_date + " meeting_room: " + meeting_room);

		layer.confirm("是否设置【" + issues_title + "】为当前议题?", {
			btn: ['是', '否']//按钮
		}, function () {
            var submit_data = {
                "operation": operation,
                "issues_id": issues_id,
                "keynote_user_name": keynote_user_name,
                "meeting_room": meeting_room,
                "meeting_date": meeting_date,
                "issues_title": issues_title,
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

		}, function () {
			layer.msg("取消设置【" + issues_title + "】为当前议题", {
				icon: 0
			});
		});
	});


	$('#id_admin_meeting_cancel_current').on('click', function () {
		var issues_id = $('#id_admin_meeting_table_body input[name="select_id"]:checked ').val();
		if ((typeof issues_id) === 'undefined') {
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
		var issues_id = "";
		var keynote_user_name = "";
		var meeting_room = "";
		var meeting_date = "";
		var issues_title = "";
		var current_issues_flags = "";

		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "id_meeting_issues_id") {
				issues_id = $(this).text();
				console.log("issues_id:" + issues_id);
			}

			if ($(this).attr('id') === "id_meeting_keynote_user_name") {
				keynote_user_name = $(this).text();
				console.log("user_name:" + keynote_user_name);
			}

			if ($(this).attr('id') === "id_meeting_room") {
				meeting_room = $(this).text();
				console.log("meeting_room:" + meeting_room);
			}

			if ($(this).attr('id') === "id_meeting_date") {
				meeting_date = $(this).text();
				console.log("meeting_date:" + meeting_date);
			}

			if ($(this).attr('id') === "id_meeting_issues_title") {
				issues_title = $(this).text();
				console.log("issues_title:" + issues_title);
			}

			if ($(this).attr('id') === "id_meeting_issues_current_flags") {
				current_issues_flags = $(this).text();
				console.log("current_issues_flags:" + current_issues_flags);
			}

		});

		if (current_issues_flags == "False")
        {
            console.log(" is not current issues,can not set it");
            return;
        }
		var operation = "issues_cancel";
		console.log("operation:" + operation + " issues_id: " + issues_id + " keynote_user_name: " + keynote_user_name +
			" meeting_date: " + meeting_date + " meeting_room: " + meeting_room);

		layer.confirm("是否取消【" + issues_title + "】为当前议题?", {
			btn: ['是', '否']//按钮
		}, function () {
            var submit_data = {
                "operation": operation,
                "issues_id": issues_id,
                "keynote_user_name": keynote_user_name,
                "meeting_room": meeting_room,
                "meeting_date": meeting_date,
                "issues_title": issues_title,
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

		}, function () {
			layer.msg("放弃取消【" + issues_title + "】为当前议题", {
				icon: 0
			});
		});
	});

});
