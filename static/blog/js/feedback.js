$(function(){
    function showFeedbackError(title, message){
        $('.filter').show();
        $('.error').show();
        $('.error .error-title').text(title);
        $('.error .error-body').text(message);
    }
    $('#id_feedback_submit').click(function(){
        var form        = $('#id_feedback_form');
        $(this).text('正在提交...');
        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: form.serialize(),
            dataType: 'json'
        }).success(function(data){
            if (!data['status']){
                showFeedbackError('表单填写有误',data['errorMsg']);
            }else{
                showFeedbackError('评论成功',data['errorMsg']);
                $('#id_feedback_user').val('');
                $('#id_feedback_email').val('');
                $('#id_feedback_suggestion').val('');
            }
        }).error(function(){
            showFeedbackError('发生错误', '表单提交失败：服务器或网络错误，请重试。');
        }).complete(function(){
            $('#id_feedback_submit').text('提交');
        });
        return false;
    });
    $('.error #id_error_ok').click(function(){
        $('.error').hide();
        $('.filter').hide();
    });
});