function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}

$(document).ready(function () {
    // handles feedback deal with
    $('#id_user_feedback_confirm').on('click', function () {
        var feedback_title = $("#id_user_feedback_title").val();
        var feedback_details = $("#id_user_feedback_details").val(); //选中的文本
        console.log("feedback_title:" + feedback_title);
        console.log("feedback_details: " + feedback_details);

        if (feedback_title === "") {
        $("#id_input_topic_name").focus();
        layer.msg("反馈标题不能为空");
        return false;
        }

        if (feedback_details === "") {
        $("#id_input_topic_brief").focus();
        layer.msg("反馈详情不能为空");
        return false;
        }

        var submit_data = {
        "operation": "feedback",
        "feedback_title": feedback_title,
        "feedback_details": feedback_details,
        "_xsrf": getCookie("_xsrf")
        };

        console.log(" feedback_title:" + feedback_title + " feedback_details:" + feedback_details );
        $.ajax({
            type: "post",
            url: "/feedback",
            data: submit_data,
            cache: false,
            success: function (arg) {
                console.log(arg);
                //arg是字符串
                var obj = JSON.parse(arg);
                if (obj.status) {
                    layer.msg("提交成功");
                    console.log("feedback_title:" + feedback_title);
                    window.location.reload();

                } else {
                    layer.msg(obj.message);
                }
            },
            error: function (arg) {
                console.log(arg);
                layer.msg("未知的错误");
            }
        }); // end of ajax
    }); //end of id click

	$('input[value="查看问题"]').click(function () {
		//获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
		var numId = $('input[value="查看问题"]').index($(this)) + 1;
		console.log(numId);
		//选择表格中的所有tr 通过eq方法取得当前tr
		var ttr = $('table tr').eq(numId);
		console.log(ttr);

		/*当前行使用find方法找到每一个td列
		each方法为每一个td设置function
		 */
		var serial_number = "0";
		ttr.find("td").each(function () {
			/*过滤 td中的元素
			checkbox 、 button、text 不需要执行append
			注意 return 为 跳出当前 each
			return false 为 跳出整个 each
			 */
			if ($(this).children("input[type='checkbox']").length > 0) {
				return;
			}
			if ($(this).children("input[type='button']").length > 0) {
				return;
			}
			if ($(this).children("input[type='text']").length > 0) {
				return;
			}

			var id = $(this).attr('id');
			var tdVal = $(this).html();
			//console.log(id);
			//console.log(tdVal);
			if (id == "id_admin_opinions_serial_number") {
				serial_number = tdVal;
			}
		});

		console.log(serial_number);
		if (serial_number == "") {
			layer.msg('编号不能为空');
		} else {
			var index = layer.open({
					type: 2, //iframe 层
					title: '查看详细信息',
					maxmin: true,
					shadeClose: true, //点击遮罩关闭层
					area: ['800px', '520px'],
					content: '/admin/opinions_popup?serial_number=' + serial_number
				});
		}
	});

	$('#id_admin_opinions_solution_submit').on('click', function () {
        var serial_number = $("#id_admin_opinions_report_serial_number").val();
        var resolved_status = $("#id_admin_opinions_resolved_status").val();
        var solution_methods = $("#id_admin_opinions_solution_methods").val(); //选中的文本

        if (serial_number === "") {
        $("#id_admin_opinions_report_serial_number").focus();
        layer.msg("编号不能为空");
        return false;
        }

        if (solution_methods === "") {
        $("#id_admin_opinions_solution_methods").focus();
        layer.msg("解决方案不能为空");
        return false;
        }

        var submit_data = {
        "operation": "resolved",
        "serial_number": serial_number,
        "resolved_status": resolved_status,
        "solution_methods": solution_methods,
        "_xsrf": getCookie("_xsrf")
        };

        console.log(" serial_number:" + serial_number + " solution_methods:" + solution_methods );
        $.ajax({
            type: "post",
            url: "/admin/opinions_popup",
            data: submit_data,
            cache: false,
            success: function (arg) {
                console.log(arg);
                //arg是字符串
                var obj = JSON.parse(arg);
                if (obj.status) {
                    layer.msg("提交成功");
                    console.log("serial_number:" + serial_number);
                    var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                    parent.layer.close(index); //再执行关闭
                    parent.location.reload();

                } else {
                    layer.msg(obj.message);
                    var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
		            parent.layer.close(index); //再执行关闭
                }
            },
            error: function (arg) {
                console.log(arg);
                layer.msg("未知的错误");
                var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                parent.layer.close(index); //再执行关闭
            }
        }); // end of ajax
	});


	$('#id_admin_opinions_solution_cancel').on('click', function () {
		var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
        console.log(index);

		parent.layer.close(index); //再执行关闭
	});

	var serial_number = 0;

	$('input[value="回归通过"]').click(function () {
	    console.log("click regression succeed");
        var button = $(this);
        var serial_number = button.attr('id');
        console.log("serial_number:"+ serial_number);

		layer.confirm("确认【" + serial_number + "】是否回归通过?", {
			btn: ['确认', '取消']//按钮
		}, function () {
			var submit_data = {
				"operation": "succeed",
				"serial_number":serial_number,
				"_xsrf": getCookie("_xsrf")
			};

			console.log("operation:succeed,serial_number:" + serial_number );

			$.ajax({
				type: "post",
				url: "/feedback",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						layer.msg("提交成功", {
							icon: 1
						});
						console.log("serial_number:" + serial_number);
						setTimeout(function () {
							window.location.reload();
						}, 1000);
					} else {
						alert(obj.message);
					}
				},
				error: function (arg) {
					layer.msg("未知的错误");
				}
			});

		}, function () {
			layer.msg("回归【" + serial_number + "】操作已为您取消", {
				icon: 0
			});
		});

	}); // end of  class_user_feedback_regression_succeed


	$('input[value="回归失败"]').click(function () {
        console.log("click regression failure");
        var button = $(this);
        var serial_number = button.attr('id');
        console.log("serial_number:"+ serial_number);

		layer.confirm("确认【" + serial_number + "】是否回归失败?", {
			btn: ['确认', '取消']//按钮
		}, function () {
			var submit_data = {
				"operation": "failure",
				"serial_number":serial_number,
				"_xsrf": getCookie("_xsrf")
			};

			console.log("operation:succeed,serial_number:" + serial_number );

			$.ajax({
				type: "post",
				url: "/feedback",
				data: submit_data,
				cache: false,
				success: function (arg) {
					console.log(arg);
					//arg是字符串
					var obj = JSON.parse(arg);
					if (obj.status) {
						layer.msg("提交成功", {
							icon: 1
						});
						console.log("serial_number:" + serial_number);
						setTimeout(function () {
							window.location.reload();
						}, 1000);
					} else {
						alert(obj.message);
					}
				},
				error: function (arg) {
					layer.msg("未知的错误");
				}
			});

		}, function () {
			layer.msg("回归不通过【" + serial_number + "】操作已为您取消", {
				icon: 0
			});
		});
	}); // end of class_user_feedback_regression_failure

    $("#admin_feedback_table_finish td").click(function(){
        var current_column = $(this).parent().find("td").index($(this)[0]); //获取当前点击的列
        if (current_column === 5) // 点击第六列的事件
        {
            var  current_row = $(this).parent().parent().find("tr").index($(this).parent()[0]); // 获取当前点击的行
            console.log("第" + (current_row + 1) + "行，第" + (current_column + 1) + "列");
            var feedback_history = $("#admin_feedback_table_finish").find("tr").eq(current_row+1).find("td").eq(0).text();

            layer.confirm("是否删除【" + feedback_history + "】记录?", {
			    btn: ['删除', '取消']//按钮
            }, function () {
                var submit_data = {
                    "operation": "delete_history",
                    "serial_number": feedback_history,
                    "subtraction":"false",
                    "_xsrf": getCookie("_xsrf")
                };

                console.log("operation:delete history ,id:" + feedback_history);

                $.ajax({
                    type: "post",
                    url: "/admin/opinions",
                    data: submit_data,
                    cache: false,
                    success: function (arg) {
                        console.log(arg);
                        //arg是字符串
                        var obj = JSON.parse(arg);
                        if (obj.status) {
                            layer.msg("删除成功", {
                                icon: 1
                            });
                            console.log("feedback_history:" + feedback_history);
                            setTimeout(function () {
                                window.location.reload();
                            }, 1000);
                        } else {
                            alert(obj.message);
                        }
                    },
                    error: function (arg) {
                        alert("未知的错误");
                    }
                });

            }, function () {
                layer.msg("删除【" + feedback_history + "】记录操作已为您取消", {
                    icon: 0
                });
            });


        }

    }); // end of click table


});//end of documents ready