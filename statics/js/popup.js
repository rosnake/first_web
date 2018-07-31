var popup_index = 0;

$(document).ready(function(){
    //弹出一个iframe层
       //标签+属性选择所有<编辑>按钮
    $('input[value="编辑"]').click(function () {
        //获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
        var numId = $('input[value="编辑"]').index($(this))+1;
        console.log(numId);
        //选择表格中的所有tr 通过eq方法取得当前tr
        var ttr = $('table tr').eq(numId);
        console.log(ttr);

        /*当前行使用find方法找到每一个td列
         each方法为每一个td设置function
         */
         var user="";
        ttr.find("td").each(function () {
            /*过滤 td中的元素
             checkbox 、 button、text 不需要执行append
             注意 return 为 跳出当前 each
             return false 为 跳出整个 each
             */
            if($(this).children("input[type='checkbox']").length>0){
                return ;
            }
            if($(this).children("input[type='button']").length>0){
                return ;
            }
            if($(this).children("input[type='text']").length>0){
                return ;
            }

            var id = $(this).attr('id');
            var tdVal = $(this).html();
            //console.log(id);
            //console.log(tdVal);
            if(id == "name")
            {
                user = tdVal;
            }
        });

        console.log(user);
        if(user == "")
        {
            layer.msg('用户名不能为空');
        }
        else
        {
            console.log(user);
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
                content: '/layer?user='+person
                });
        }
    });

    $('#pop_close').on('click', function(){
        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
        parent.layer.close(index); //再执行关闭
        });

    });