$.validator.addMethod("username_exist", function(value, element) {
    var is_exist = false;
    $.ajax({
        url: '/ad/check_username_exist/',
        type: 'GET',
        data: {
            'username': value,
        },
        success: function(data) {
            is_exist = data;
        }
    });
    return this.required(element) && is_exist
});

$.validator.addMethod("username_valid", function(value, element) {
    var is_valid = false;
    var regex = /^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$/
    is_valid = regex.test(value);
    return this.required(element) && is_valid
});

$.validator.addMethod("password_valid", function(value, element) {
    var is_valid = false;
    //Mật khẩu phải có ít nhất 1 ký tự viết hoa, 1 ký tự viết thường, 1 ký tự số, độ dài từ 6-20 ký tự
    var regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$/
    is_valid = regex.test(value);
    return this.required(element) && is_valid
});

$.validator.addMethod("number_str", function(value, element) {
    var is_valid = false;
    var regex = /^[0-9]+$/
    is_valid = regex.test(value);
    return this.required(element) && is_valid
});

$.validator.addMethod("date_format", function(value, element) {
    var is_valid = false;
    //Kểm tra theo format dd/mm/yyyy, {2}, {4} là số lượng ký tự
    var regex = /^([0-9]{2})\/([0-9]{2})\/([0-9]{4})$/ 
    is_valid = regex.test(value);
    return this.required(element) && is_valid
});

$.validator.addMethod("email_format", function(value, element) {
    var is_valid = false;
    //Check email theo format
    //^: Bắt đầu, $: Kết thúc, [^\s@]: Không có khoảng trắng và @, +@: 1 @, +\. Có ít nhất 1 dấu ., [^\s@]+: Không có khoảng trắng + @ và có ít nhất 1 ký tự sau dấu .
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    is_valid = regex.test(value);
    return this.required(element) && is_valid
});
$.validator.addMethod("phone_number", function(value, element) {
    var is_valid = false;
    var regex = /^[0-9]{10,11}$/;
    is_valid = regex.test(value);
    return this.optional(element) && is_valid
}),
$.validator.addMethod("blood_group", function(value, element) {
    var is_valid = false;
    var regex = /^(A|B|AB|O)[+-]$/
    is_valid = regex.test(value);
    return this.required(element) && is_valid
}),

$(document).ready(function() {
    $('.add-patient-form').validate({
        rules: {
            "new-patient-username": {
                required: true,
                minlength: 3,
                maxlength: 40,
                username_exist: false,
                username_valid: true,
            },
            "new-patient-password": {
                required: true,
                minlength: 5,
                maxlength: 20,
                password_valid: true,
            },
            "new-patient-name":{
                required: true,
                minlength: 3,
                maxlength: 40,
            },
            "new-patient-ci_id":{
                required: true,
                length: 12|9,
                number_str: true,
            },
            "new-patient-phone":{
                phone_number: true,
                minlength: 10,
            },
            "new-patient-email":{
                required: true,
                email_format: true,
            },
            "new-patient-dob":{
                required: true,
                date_format: true,
            },
        },
        messages: {
            "new-patient-username": {
                required: "Vui lòng nhập tên đăng nhập",
                minlength: "Tên đăng nhập phải có ít nhất 3 ký tự",
                maxlength: "Tên đăng nhập không được vượt quá 40 ký tự",
            },
            "new-patient-password": {
                required: "Vui lòng nhập mật khẩu",
                minlength: "Mật khẩu phải có ít nhất 5 ký tự",
                maxlength: "Mật khẩu không được vượt quá 20 ký tự",
                password_valid: "Mật khẩu phải có ít nhất 1 ký tự viết hoa, 1 ký tự viết thường, 1 ký tự số, độ dài từ 6-20 ký tự",
            },
            "new-patient-name":{
                required: "Vui lòng nhập họ tên",
                minlength: "Họ tên phải có ít nhất 3 ký tự",
                maxlength: "Họ tên không được vượt quá 40 ký tự",
            },
            "new-patient-ci_id":{
                required: "Vui lòng nhập CMND/CCCD",
                length: "CMND/CCCD phải có 9 hoặc 12 ký tự",
                number_str: "CMND/CCCD phải là chuỗi số",
            },
            "new-patient-phone":{
                phone_number: "Số điện thoại phải có 10 hoặc 11 ký tự",
                minlength: "Số điện thoại phải có ít nhất 10 ký tự",
            },
            "new-patient-email":{
                required: "Vui lòng nhập email",
                email_format: "Email không đúng định dạng",
            },
            "new-patient-dob":{
                required: "Vui lòng nhập ngày sinh",
                date_format: "Ngày sinh không đúng định dạng",
            },

        },
            //Xác định vị trí hiển thị thông báo lỗi
        errorPlacement: function(error, element) {
        //insertAfter(element): Chèn sau element lỗi
            error.insertAfter(element);
        }
    });

    $('.register-form').validate({
        rules: {
            "real_name":{
                required: true,
                minlength: 3,
                maxlength: 40,
            },
        },
        messages: {
                required: "Vui lòng nhập họ tên",
                minlength: "Họ tên phải có ít nhất 3 ký tự",
                maxlength: "Họ tên không được vượt quá 40 ký tự",
            }
    });
});