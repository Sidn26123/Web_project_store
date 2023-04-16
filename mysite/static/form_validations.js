// $.validate.addMethod("is_username_exist", function(value, element) {
//     var is_exist = false;
//     $.ajax({
//         url: '/ad/check_username_exist/',
//         type: 'GET',
//         data: {
//             'username': value,
//         }
//     });
// });

// $.validate.addMethod("is_username_valid", function(value, element) {

// });
$(document).ready(function() {
    $('.add-patient-form').validate({
        rules: {
            "new-patient-username": {
                required: true,
                minlength: 3,
                maxlength: 40,
            },
            "new-patient-password": {
                required: true,
                minlength: 5,
                maxlength: 20,
            },
        },
        messages: {
            "new-patient-username": {
                required: "Vui lòng nhập tên đăng nhập",
                minlength: "Tên đăng nhập phải có ít nhất 3 ký tự",
                maxlength: "Tên đăng nhập không được vượt quá 40 ký tự",
            }
        },
            //Xác định vị trí hiển thị thông báo lỗi
            errorPlacement: function(error, element) {
            //insertAfter(element): Chèn sau element lỗi
                error.insertAfter(element);
            }
    });
});