$("form[name=signup-form").submit(function(e) {
    
    var $form = $(this);
    var $error = $form.find('.error');
    var data = $form.serialize();
    
    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        datatype: "json",
        success: function(resp) {
            console.log(resp);
        },
        error: function(resp) {
            console.log(resp);
        }
    });
    e.preventDefault();
});