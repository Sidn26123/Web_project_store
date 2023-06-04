
$(document).ready(function () {
    set_doctor_info();
    $('#save-change').on('click', function () {
        save_change();
    });
});
function set_doctor_info(){
    var doctor_id = $('.get-id').data('id')
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/doctor/get-doctor-info/',
        type: 'POST',
        data: {
            'id': doctor_id,
        },
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (data) {
            console.log(data)
            $('.doctor-avatar').attr('src', data.doctor['avatar']);
            $('#username').val(data.doctor['username']);
            $('#real_name').val(data.doctor['real_name']);
            $('#date_of_birth').val(data.doctor['date_of_birth']);
            $('#phone').val(data.doctor['phone']);
            $('#email').val(data.doctor['email']);
        }
    });
}

function save_change(){
    var is_change = true;
    var doctor_id = $('.get-id').data('id')
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    var infos = $('.doctor-info-field').find('input');
    var data = {};
    infos.each(function () {
        data[$(this).attr('id')] = $(this).val();
    });
    console.log(data)
    $.ajax({
        url: '/doctor/save-change/',
        type: 'POST',
        data: {
            'id': doctor_id,
            'data': JSON.stringify(data),
        },
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (data){
            alert("Thay đổi thành công")
        }
    });
}