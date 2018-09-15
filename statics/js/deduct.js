$(document).ready(function () {
	$('#id_admin_deduct_add').on('click', function () {
	    $('#id_admin_deduct_edit_deduct_id').val("0");
	    $('#id_admin_deduct_edit_operation').val("add");
		$('#id_admin_deduct_edit_popup_background').show();
		$("#id_admin_deduct_edit_sub_title").text("增加扣分项目");
	});

	$('#id_admin_deduct_del').on('click', function () {
		var deduct_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
		if ((typeof deduct_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("deduct_id: " + deduct_id);
		console.log("click admin deduct delete");
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		//console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var deduct_name = "";
		var deduct_points = 0;
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "deduct_id") {
				var deduct_id = $(this).val();
				console.log("deduct_id:" + deduct_id);
			}

			if ($(this).attr('id') === "deduct_name") {
				deduct_name = $(this).text();
				console.log("deduct_name:" + deduct_name);
			}

			if ($(this).attr('id') === "deduct_points") {
				 deduct_points = $(this).val();
				console.log("deduct_points:" + deduct_points);
			}
		});

		layer.confirm("是否删除【" + deduct_name + "】?", {
			btn: ['删除', '取消']//按钮
		}, function () {
			var submit_data = {
			"operation": "delete",
			"deduct_name": deduct_name,
			"deduct_points": deduct_points,
			"id":deduct_id,
			"_xsrf": getCookie("_xsrf")
			};

			console.log("operation:add,deduct_name:"+deduct_name+" deduct_points:"+deduct_points+" deduct_id:"+deduct_id);

			$.ajax({
				type: "post",
				url: "/admin/deduct",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						layer.msg("删除成功", {	icon: 1	});
						console.log("deduct_name:"+ deduct_name);
						setTimeout(function () {window.location.reload();}, 1000);
					} else {
						alert(obj.message);
					}
				},
				error:function(arg) {
					alert("未知的错误");
				}
			});

		}, function () {
			layer.msg("删除【" + deduct_name + "】操作已为您取消", {
				icon: 0
			});
		});

		//setTimeout(function () {window.location.reload();}, 1000);
	});

	$('#id_admin_deduct_mod').on('click', function () {
		var deduct_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
		if ((typeof deduct_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		console.log("deduct_id: " + deduct_id);
		console.log("click admin member delete");
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var ttr = $("input:checked").parents('tr');
		//console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var deduct_id = "";
		var deduct_points = 0;
		var deduct_name = "";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */

			if ($(this).attr('id') === "deduct_id") {
				deduct_id = $(this).text();
				console.log("user_id:" + deduct_id);
			}

			if ($(this).attr('id') === "deduct_points") {
				deduct_points = $(this).text();
				console.log("deduct_points:" + deduct_points);
			}

			if ($(this).attr('id') === "deduct_name") {
				deduct_name = $(this).text();
				console.log("deduct_name:" + deduct_name);
			}
		});

		console.log("deduct_id: " + deduct_id);
		console.log("deduct_name: " + deduct_name);
		console.log("deduct_points: " + deduct_points);
	    $('#id_admin_deduct_edit_deduct_id').val(deduct_id);
	    $('#id_admin_deduct_edit_operation').val("modify");
	    $('#id_admin_deduct_edit_deduct_name').val(deduct_name);
	    $('#id_admin_deduct_edit_deduct_name').attr("readonly", true)
	    $("#id_admin_deduct_edit_deduct_point").val(deduct_points);
		$('#id_admin_deduct_edit_popup_background').show();
		$("#id_admin_deduct_edit_sub_title").text("修改扣分项目");
	});

	$('#id_admin_deduct_edit_submit').on('click', function ()
	{
	    var operation = $("#id_admin_deduct_edit_operation").val();
		var deduct_id = $("#id_admin_deduct_edit_deduct_id").val();
		var deduct_name = $("#id_admin_deduct_edit_deduct_name").val();
		var deduct_points = $("#id_admin_deduct_edit_deduct_point").val();

		if (deduct_name == "") {
			$("#id_admin_deduct_edit_deduct_name").focus();
			layer.msg("扣分项不能为空.");
			return false;
		}

		if (deduct_points == "") {
			$("#id_admin_deduct_edit_deduct_point").focus();
			layer.msg("扣分值不能为空.");
			return false;
		}
		if (deduct_points >= 0) {
			$("#id_admin_deduct_edit_deduct_point").focus();
			layer.msg("扣分值不能大于0.");
			return false;
		}

		var submit_data = {
			"operation": operation,
			"deduct_name": deduct_name,
			"deduct_points": deduct_points,
			"id":deduct_id,
			"_xsrf": getCookie("_xsrf")
			};

		console.log("operation:"+operation+"deduct_name:"+deduct_name+" deduct_points:"+deduct_points+" deduct_id:"+deduct_id);

        $.ajax({
            type: "post",
            url: "/admin/deduct",
            data: submit_data,
            cache: false,
            success: function (arg) {
                console.log(arg);
                //arg是字符串
                var obj = JSON.parse(arg);
                if (obj.status) {
                    layer.alert("提交成功", {skin: 'layui-layer-molv' ,closeBtn: 0}, function () {window.location.reload();});
                } else {
                    layer.alert(obj.message, {skin: 'layui-layer-molv' ,closeBtn: 0}, function () {window.location.reload();});
                }
            },
            error:function(arg) {
                alert("未知的错误");
            }
        });

        $("#id_admin_deduct_edit_deduct_id").val("");
		$("#id_admin_deduct_edit_deduct_name").val("");
	    $('#id_admin_deduct_edit_operation').val("");

		$("#id_admin_deduct_edit_deduct_point").val("");
		$('#id_admin_deduct_edit_popup_background').hide();

    });

	$('#id_admin_deduct_edit_cancel').on('click', function ()
	{
        $("#id_admin_deduct_edit_deduct_id").val("");
		$("#id_admin_deduct_edit_deduct_name").val("");
	    $('#id_admin_deduct_edit_operation').val("");
	    $("#id_admin_deduct_edit_deduct_point").val("");
		$('#id_admin_deduct_edit_popup_background').hide();
    });
});
