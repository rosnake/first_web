var popup_index = 0;

$(document).ready(function(){
    //弹出一个iframe层
    $('#popup').on('click', function(){
        var user = $("#username").val();
        if(user == "")
        {
            layer.msg('用户名不能为空');
        }
        else
        {
            var index = layer.open({
                type: 2, //iframe 层
                title: '编辑',
                maxmin: true,
                shadeClose: true, //点击遮罩关闭层
                area : ['800px' , '520px'],
                content: '/layer?user='+user
                });
        }
    });

    $('#pop_close').on('click', function(){
        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
        parent.layer.close(index); //再执行关闭
        });

    });