$(document).ready(function(){
    $('#admin_member_add').on('click', function(){
        var member_id=prompt("请输入新的工号.");
        var user_name=prompt("请输入姓名.");
        var user_role=prompt("请输入角色.");
        console.log("member_id: "+member_id);
        console.log("user_name: "+user_name);
        console.log("user_role: "+user_role);
        ret = confirm("是否新增【"+user_name+"】?");
         if (ret===true)
        {
            alert("新增成功");
        }
        else
        {
            alert("取消新增");
        }
        window.location.reload();
    });

    $('#admin_member_del').on('click', function(){
        var member_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
        if((typeof member_id) === 'undefined')
        {
            alert("current not select any id.");
            console.log("current not select any id");
            return;
        }
        console.log("member_id: "+member_id);
        console.log("click admin member delete");
        //获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
        var ttr = $("input:checked").parents('tr');
        //console.log(ttr);

        /*当前行使用find方法找到每一个td列
         each方法为每一个td设置function
         */
         var user_name = "";
        ttr.find("td").each(function () {
            /*过滤 td中的元素
             checkbox 、 button、text 不需要执行append
             注意 return 为 跳出当前 each
             return false 为 跳出整个 each
             */

            if($(this).attr('id') === "user_id")
            {
                var user_id = $(this).text();
                console.log("user_id:"+ user_id);
            }

            if($(this).attr('id') === "user_name")
            {
                user_name = $(this).text();
                console.log("user_name:"+ user_name);
            }

            if($(this).attr('id') === "user_role")
            {
                var user_role = $(this).text();
                console.log("user_role:"+ user_role);
            }
        });

         ret = confirm("是否删除【"+user_name+"】?");
         if (ret === true)
        {
            alert("删除成功");
        }
        else
        {
            alert("删除取消");
        }
        window.location.reload();
    });

     $('#admin_member_mod').on('click', function(){
        var member_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
        if((typeof member_id) === 'undefined')
        {
            alert("current not select any id.");
            console.log("current not select any id");
            return;
        }
        console.log("member_id: "+member_id);
        console.log("click admin member delete");
        //获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
        var ttr = $("input:checked").parents('tr');
        //console.log(ttr);

        /*当前行使用find方法找到每一个td列
         each方法为每一个td设置function
         */
         var user_name = "";
         var user_id = "";
         var user_role = "";
        ttr.find("td").each(function () {
            /*过滤 td中的元素
             checkbox 、 button、text 不需要执行append
             注意 return 为 跳出当前 each
             return false 为 跳出整个 each
             */

            if($(this).attr('id') === "user_id")
            {
                user_id = $(this).text();
                console.log("user_id:"+ user_id);
            }

            if($(this).attr('id') === "user_name")
            {
                user_name = $(this).text();
                console.log("user_name:"+ user_name);
            }

            if($(this).attr('id') === "user_role")
            {
                user_role = $(this).text();
                console.log("user_role:"+ user_role);
            }
        });
        member_id=prompt("请输入新的工号,当前工号【"+user_id+"】");
        user_name=prompt("请输入新的用户名,当前用户名【"+user_name+"】");
        user_role=prompt("请输入新的角色,当前角色【"+user_role+"】");
        console.log("member_id: "+member_id);
        console.log("user_name: "+user_name);
        console.log("user_name: "+user_name);
         ret = confirm("是否修改【"+user_name+"】?");
         if (ret === true)
        {
            alert("修改成功");
        }
        else
        {
            alert("取消修改");
        }
        window.location.reload();
     });
     /*----------------------------------*/
    $('#admin_deduct_add').on('click', function(){
        var deduct_id=prompt("请输入新的扣分项目编号.");
        if(deduct_id === "")
        {
             layer.msg("您未输入有效的项目编号，已为您取消操作。", {icon: 2});
             return;
        }
        var deduct_name=prompt("请输入扣分项目.");
        if(deduct_name === "")
        {
             layer.msg("您未输入有效的项目名称，已为您取消操作。", {icon: 2});
             return;
        }
        var deduct_points=prompt("请输入扣分值.");
        if(deduct_name === "")
        {
             layer.msg("您未输入有效的扣分值，已为您取消操作。", {icon: 2});
             return;
        }
        console.log("deduct_id: "+deduct_id);
        console.log("deduct_name: "+deduct_name);
        console.log("deduct_points: "+deduct_points);
        ret = confirm("是否新增【"+deduct_name+"】?");
         if (ret===true)
        {
            alert("新增成功");
        }
        else
        {
            alert("取消新增");
        }
        window.location.reload();
    });

    $('#admin_deduct_del').on('click', function(){
        var deduct_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
        if((typeof deduct_id) === 'undefined')
        {
            layer.msg("当前未选择任何项目");
            console.log("current not select any id");
            return;
        }
        console.log("deduct_id: "+deduct_id);
        console.log("click admin deduct delete");
        //获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
        var ttr = $("input:checked").parents('tr');
        //console.log(ttr);

        /*当前行使用find方法找到每一个td列
         each方法为每一个td设置function
         */
         var deduct_name = "";
        ttr.find("td").each(function () {
            /*过滤 td中的元素
             checkbox 、 button、text 不需要执行append
             注意 return 为 跳出当前 each
             return false 为 跳出整个 each
             */

            if($(this).attr('id') === "deduct_id")
            {
                var deduct_id = $(this).text();
                console.log("deduct_id:"+ deduct_id);
            }

            if($(this).attr('id') === "deduct_name")
            {
                deduct_name = $(this).text();
                console.log("deduct_name:"+ deduct_name);
            }

            if($(this).attr('id') === "deduct_points")
            {
                var deduct_points = $(this).text();
                console.log("deduct_points:"+ deduct_points);
            }
        });

        //ret = confirm("是否删除【"+deduct_name+"】?");
        layer.confirm("是否删除【"+deduct_name+"】?", {
        btn: ['删除','取消'] //按钮
        }, function(){
        //这里放删除提交
            layer.msg("删除成功", {icon: 1});
        }, function(){
            layer.msg("删除【"+deduct_name+"】操作已为您取消", {icon: 0});
        });

        window.location.reload();
    });

     $('#admin_deduct_mod').on('click', function(){
        var deduct_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
        if((typeof deduct_id) === 'undefined')
        {
            layer.msg("当前未选择任何项目");
            console.log("current not select any id");
            return;
        }
        console.log("deduct_id: "+deduct_id);
        console.log("click admin member delete");
        //获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
        var ttr = $("input:checked").parents('tr');
        //console.log(ttr);

        /*当前行使用find方法找到每一个td列
         each方法为每一个td设置function
         */
         var deduct_id = "";
         var deduct_points = "";
         var deduct_name = "";
        ttr.find("td").each(function () {
            /*过滤 td中的元素
             checkbox 、 button、text 不需要执行append
             注意 return 为 跳出当前 each
             return false 为 跳出整个 each
             */

            if($(this).attr('id') === "deduct_id")
            {
                deduct_id = $(this).text();
                console.log("user_id:"+ deduct_id);
            }

            if($(this).attr('id') === "deduct_points")
            {
                deduct_points = $(this).text();
                console.log("deduct_points:"+ deduct_points);
            }

            if($(this).attr('id') === "deduct_name")
            {
                deduct_name = $(this).text();
                console.log("deduct_name:"+ deduct_name);
            }
        });

        deduct_points=prompt("请输入新的【"+deduct_name+"】扣分值,当前扣分值【"+deduct_points+"】");
        if(deduct_points === "")
        {
             layer.msg("您未输入有效的扣分值，已为您取消操作。", {icon: 2});
             return;
        }
        console.log("deduct_id: "+deduct_id);
        console.log("deduct_name: "+deduct_name);
        console.log("deduct_points: "+deduct_points);
         ret = confirm("是否修改【"+deduct_name+"】为【"+deduct_points+"】?");
         if (ret === true)
        {
            alert("修改成功");
        }
        else
        {
            alert("取消修改");
        }
        window.location.reload();
     });
     /*----------------------------------*/

});
