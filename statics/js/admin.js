$(document).ready(function(){
    $('#admin_member_add').on('click', function(){
        var member_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();

        console.log("member_id: "+member_id);
    });

    $('#admin_member_del').on('click', function(){
        var member_id = $('#admin_member_table_body input[name="select_id"]:checked ').val();
        console.log("member_id: "+member_id);
        console.log("click admin member delete");
        //获取每一个<编辑>按钮的 下标（从0开始 所以需要+1 = 按钮在表格的所在行数）
        var ttr = $("input:checked").parents('tr');
        console.log(ttr);

        /*当前行使用find方法找到每一个td列
         each方法为每一个td设置function
         */
         var user="";
         var operation="browse";
        ttr.find("td").each(function () {
            /*过滤 td中的元素
             checkbox 、 button、text 不需要执行append
             注意 return 为 跳出当前 each
             return false 为 跳出整个 each
             */
            if($(this).attr('id') === "user_id")
            {
                tmpid = $(this).text();
                console.log("user_id:"+ tmpid);
            }

            if($(this).attr('id') === "user_name")
            {
                tmpid = $(this).text();
                console.log("user_name:"+ tmpid);
            }

            if($(this).attr('id') === "user_role")
            {
                tmpid = $(this).text();
                console.log("user_role:"+ tmpid);
            }

        });
    });


});