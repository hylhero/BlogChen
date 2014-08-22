$(function(){
    function showErrorMsg(title,message){
        $('.comment_error_msg').show();
        $('.comment_error_msg .error_title').text(title);
        $('.comment_error_msg .error_msg').text(message);
    }
    $("#id_comment_submit").click(function(){
        var form     = $('#id_comment_form');
        $('#id_comment_submit').text('正在提交...');

        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: form.serialize(),
//            dataType: 'json"'
        }).success(function(data){
            if (!data['status']){
                showErrorMsg('表单填写有误',data['errorMsg']);
            }else{
                showErrorMsg('评论成功',data['errorMsg']);

                var newcomment = "<li class=\"one_comment\">"+
                                    "<a class=\"com_head_img\"href=\"\"><img src=\"/static/blog/images/headimg/userhead.png\"></a>"+
                                    "<div class=\"one_com_body\">"+
                                        "<div class=\"one_com_title\">"+
                                            "<a class=\"com_user\" href=\"#\">"+$('#id_user_nickname').val()+"</a>"+
                                            "<span class=\"com_time\">刚刚</span>"+
                                        "</div>"+
                                        "<div class=\"one_com_content\">"+
                                            "<p>"+$('#id_user_comment').val()+"</p>"+
                                        "</div>"+
                                    "</div>"+
                                "</li>"

                $('.comment_list .com_list').prepend(newcomment);

                $('#id_user_nickname').val('');
                $('#id_user_email').val('');
                $('#id_user_blog').val('');
                $('#id_user_comment').val('');
                $('#id_user_idcode').val('');

            }

        }).error(function(){
            showErrorMsg('发生错误', '表单提交失败：服务器或网络错误，请重试。');
        }).complete(function(){
            $('#id_comment_submit').text('提交评论');
        });
        return false;
    });
    $('.comment_error_msg .error_ok').click(function(){
        $('.comment_error_msg').hide();
    })
    $('#id_idcode').click(function(){
        var i = Math.random();
        $('#id_idcode img').attr('src','/mcaptcha/image/'+i+'/')
        $.ajax({
            url: '/mcaptcha/refresh/',
            type: 'GET',
        }).success(function(data){
            alert(data);
        }).complete(function(){

		});
        return false;
    });
})