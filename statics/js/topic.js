var popup_index = 0;
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
				area: ['800px', '420px'],
				//content: '/layer?user='+user
				content: '/issues'
			});
	});

	$('#id_applications_confirm').on('click', function () {
		var topic_name = $("#id_input_topic_name").val();
		var topic_brief = $("#id_input_topic_brief").val();
		var topic_date = $("#id_select_topic_date").val(); //选中的文本
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

		if (contrastTime() === true){
			$("#id_select_topic_date").focus();
			layer.msg("时间不能早于当前时间");
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


    $('#id_user_issues_evaluation').on('click', function () {
		var issues_object = $('input[name="select_id"]:checked ');
		var issues_id = issues_object.val();
		if ((typeof issues_id) === 'undefined') {
			layer.msg("当前未选择任何项目");
			console.log("current not select any id");
			return;
		}
		var issues_id = issues_object.val();
		console.log("issues_id:"+issues_id);
        $('#id_issues_evaluation_id').val(issues_id);
		$('#id_issues_evaluation_popup_background').show();
    });

    $('#id_issues_evaluation_submit').on('click', function () {
        var issues_id = $('#id_issues_evaluation_id').val();
        var prepare_score = $("input[name='issues_prepare_score']:checked").val();
        var novel_score = $("input[name='issues_novel']:checked").val();
        var report_score = $("input[name='issues_report_score']:checked").val();

        console.log("issues_id:"+issues_id+" prepare_score:"+prepare_score+" novel_score:"+novel_score+" report_score:"+report_score);
        var submit_data = {
            "operation": "evaluate",
            "issues_id": issues_id,
            "prepare_score": prepare_score,
            "novel_score": novel_score,
            "report_score": report_score,
            "_xsrf": getCookie("_xsrf")
        };

        $.ajax({
            type: "post",
            url: "/topics",
            data: submit_data,
            cache: false,
            success: function (arg) {
                console.log(arg);
                //arg是字符串
                var obj = JSON.parse(arg);
                if (obj.status) {
                    layer.msg("打分成功");
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

		$('#id_issues_evaluation_popup_background').hide();
		$('#id_issues_evaluation_id').val("");
        $('input:radio[name="issues_prepare_score"]').removeAttr('checked');
        $('input:radio[name="issues_novel"]').removeAttr('checked');
        $('input:radio[name="issues_report_score"]').removeAttr('checked');
    });

    $('#id_issues_evaluation_cancel').on('click', function () {

		$('#id_issues_evaluation_popup_background').hide();
		$('#id_issues_evaluation_id').val("");

    });
});
