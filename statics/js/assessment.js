function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}

$(document).ready(function () {
	$('input[value="不感兴趣"]').click(function () {
	    console.log("click uninterested");
        var button = $(this);
        var issues_id = button.attr('id');
        console.log("issues_id:"+ issues_id);

        var submit_data = {
            "operation": "uninterested",
            "issues_id":issues_id,
            "_xsrf": getCookie("_xsrf")
        };
        $.ajax({
            type: "post",
            url: "/topics/assessment",
            data: submit_data,
            cache: false,
            success: function (arg) {
                console.log(arg);
                //arg是字符串
                var obj = JSON.parse(arg);
                if (obj.status) {
                    layer.msg("不感兴趣", {
                        icon: 1
                    });
                    console.log("issues_id:" + issues_id);
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

	}); // end of  class_user_feedback_regression_succeed

	$('input[value="感兴趣"]').click(function () {
	    console.log("click interested");
        var button = $(this);
        var issues_id = button.attr('id');
        console.log("issues_id:"+ issues_id);

        var submit_data = {
            "operation": "interested",
            "issues_id":issues_id,
            "_xsrf": getCookie("_xsrf")
        };
        $.ajax({
            type: "post",
            url: "/topics/assessment",
            data: submit_data,
            cache: false,
            success: function (arg) {
                console.log(arg);
                //arg是字符串
                var obj = JSON.parse(arg);
                if (obj.status) {
                    layer.msg("感兴趣", {
                        icon: 1
                    });
                    console.log("issues_id:" + issues_id);
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
	}); // end of class_user_feedback_regression_failure


});//end of documents ready