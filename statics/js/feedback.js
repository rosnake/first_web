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


});//end of documents ready