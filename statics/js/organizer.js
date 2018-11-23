function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
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

	$('#id_admin_organizer_assign').on('click', function () {

	    var now = new Date();
        //格式化日，如果小于9，前面补0
        var day = ("0" + now.getDate()).slice(-2);
        //格式化月，如果小于9，前面补0
        var month = ("0" + (now.getMonth() + 1)).slice(-2);
        //拼装完整日期格式
        var today = now.getFullYear()+"-"+(month)+"-"+(day) ;

        console.log(today);
        $("#id_admin_organizer_date").val(today);
		$('#id_admin_organizer_select_popup_background').show();

	});

	$('#id_admin_popup_organizer_select_confirm').on('click', function () {
		var organizer_id = $('#id_admin_organizer_select_popup_table_body input[name="select_id"]:checked ').val();
		if ((typeof organizer_id) === 'undefined') {
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
		var user_name = "";
		var chinese_name = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "id_admin_organizer_select_user_name") {
				user_name = $(this).text();
				console.log("user_name:" + user_name);
			}

			if ($(this).attr('id') === "id_admin_organizer_select_chinese_name") {
				chinese_name = $(this).text();
				console.log("chinese_name:" + chinese_name);
			}
		});

		$('#id_admin_organizer_select_popup_background').hide();


		$('#id_admin_organizer_edit_popup_background').show();
		$("#id_admin_deduct_edit_sub_title").text("指定组织者");

		$("#id_admin_organizer_name").val(chinese_name);
		$("#id_admin_organizer_id").val(user_name);
		$("#id_admin_organizer_name").attr("readonly", true);
		$("#id_admin_organizer_id").attr("readonly", true);
	});

	$('#id_admin_popup_organizer_select_cancel').on('click', function () {
		$('#id_admin_organizer_select_popup_background').hide();
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

		if (contrastTime(time_date) === true){
			$("#id_popup_leave_apply_date").focus();
			console.log("时间不能早于当前时间");
			layer.msg("时间不能早于当前时间");
			return false;
		}
		var submit_data = {
			"operation": "assign",
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
			//window.location.reload();
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
