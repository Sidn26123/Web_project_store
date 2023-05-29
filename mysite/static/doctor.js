

$(document).ready(function () {
    $('#id-appoint-next').data('id', '10');

});
//Update phần thông báo của bác sĩ (mỗi bác sĩ onl đều gửi định kỳ 5 p 1 lần 1 hàm cập nhật)
function update_notice() {
    var doctor_id = $('.get-id').data('id')
    $.ajax({
        url: '/doctor/get-notification/',
        type: 'GET',
        data: {
            'id': doctor_id,
        },
        success: function (data) {
            get_notice(data);
        }
    })
}
function get_notice(data) {
    ;
}

//Kiểm tra xem bác sĩ có cuộc hẹn nào sắp tới không
function check_appoint_upcoming() {
    var doctor_id = $('.get-id').data('id')
    return new Promise(function(resolve, reject) {
        $.ajax({
            url: '/doctor/check-upcoming-appoint/',
            type: 'GET',
            data: {
                'id': doctor_id,
            },
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
}

function set_appoint_status(appoint_id, status) {
    console.log(appoint_id, status)
    $.ajax({
        url: '/doctor/set-status-appointment/',
        type: 'GET',
        data: {
            'appoint_id': appoint_id,
            'status': status,
        },
        success: function (data) {
            alert('success', status);
        }
    })
}
var is_show_choice = false;
var is_show_having_appoint = false;


$(document).ready(function () {
    var doctor_id = $('.get-id').data('id')
    $('#choice-ok').on('click', function () {
        var appoint_status = check_appoint_upcoming();
        if (appoint_status == 'ok') {
            var appoint = check_appoint_upcoming();
            var appoint_id = appoint['id']
            var appoint_status = appoint['status']
            if (appoint_status == 'appointing' && is_show_having_appoint == false) {
                $('.notice-having-appoint-form').show();
                is_show_having_appoint = true;
                is_show_choice = false;
            }
            else if (appoint_status == 'having-appoint') {
                $('.choice-to-appoint').show();
                is_show_choice = true;
                is_show_having_appoint = false;
            }
        }
    });
});

function get_next_appoint_id() {
    var doctor_id = $('.get-id').data('id')
    $.ajax({
        url: '/doctor/get-next-appoint-id/',
        type: 'GET',
        data: {
            'id': doctor_id,
        },
        success: function (data) {
            return data.appoint_id;
        }
    })
}
var is_showed = false;
var set_check_loop = setInterval(function () {
    console.log("looping")
    var status = ""
    var appoint_id = -1
    check_appoint_upcoming().then(function (data){
        status = data.status;
        var appoint_id = data.appoint_id;
        var appointing_id = data.appointing_id;
        console.log("ing", appointing_id)
        if (status == 'have_appoint') {
            apt_id = data.appoint_id;
            $('#id-appoint-next').ready(function () {
                $('#id-appoint-next').data('id', (apt_id).toString());
                appoint_id = $('#id-appoint-next').data('id');
            });
        }
        if (status == 'waiting' && is_showed == false) {
            console.log("showing")
            $('.choice-to-appoint').show();
            is_showed = true;
        }
        else if (status == 'waiting_and_appointing' && is_show_having_appoint == false) {
            $('.notice-having-appoint-form').show();
            is_show_having_appoint = true;
        }
        setTimeout(function () {
            if ($('#choice-ok').is(':visible')){
                $('#choice-wait').click()
            }
        }, 1000*15); //Sau vài s tự thu về -> chọn wait

        $('#choice-ok').on('click', function () {
            set_appoint_status(appoint_id, 'appointing');
            openNewTabWithLink('/doctor/appoint-detail/' + appoint_id + '/')
            $(this).parent().hide();
        });
        $('#choice-cancel').on('click', function () {
            set_appoint_status(appointing_id, 'failure');
            $(this).parent().hide();
        });
        $('#choice-wait').on('click', function () {
            set_appoint_status(appoint_id, 'waiting');
            $(this).parent().hide();
        });
        $('.choice-cancel').on('click', function () {
            $(this).parent().parent().hide();
            set_appoint_status(appointing_id, 'denied');
        });
        $('.choice-ok').on('click', function () {
            $(this).parent().parent().hide();
        });
    });
}, 1000*5);

$(document).ready(function () {

});

function openNewTabWithLink(link) {
    window.open(link, '_blank');
}

$(document).ready(function () {
    $('#notification').on('click', function () {
        $('.notification-container').toggle();
        if ($('.notification-container').is(':visible')) {
            update_notification();
        }
    });
});

function update_notification(){
    var doctor_id = $('.get-id').data('id')
    $.ajax({
        url: '/doctor/get-notification/',
        type: 'GET',
        data: {
            'id': doctor_id,
        },
        success: function (data) {
            draw_notification(data);
        }
    })
}

function draw_notification(data) {
    var table_data = JSON.parse(data.table);
    for (var i = 0; i < table_data.length; i++) {
        var template = $('#notification-item-template').clone();
        var row = table_data[i];
        template.find('.content').text(row['content']);
        template.find('.time').text(row['time_notice']);
        $('.notification-area').append(template);
    }
}