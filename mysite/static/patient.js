// Lấy ngày hiện tại
var currentDate = new Date();
var year = currentDate.getFullYear();
var month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
var day = currentDate.getDate().toString().padStart(2, '0');
var formattedDate = year + '-' + month + '-' + day;
// $('.doc-' + id).find('input').val(formattedDate);
var day_of_week = [1,2,3,4,5,6,7]
var day_of_week_index =((currentDate.getDay() + 6) % 7) + 1;
// update_time(id);
// $(document).on('blur', '.start_date', function(){
//     $('#doctor-time-area').empty();

//     var id = $(this).parent().data('doctor-id')
//     console.log(id)
//     update_time(id);

// })



$(document).ready(function(){
    var doc_node = $('.doctor-info');
    doc_node.each( function(index, value){
        var id = $(this).data('doctor-id');
        // var cur_date = get_day_cur();
        // cur_date = new Date(cur_date)
        // day_of_week_index =((cur_date.getDay() + 6) % 7) + 1;
        $('.start_date').val(formattedDate);
        var day_cur = get_day_index(new Date(get_day_cur()));
        update_time(id, day_cur);
        add_day();
    });
    $(document).on('click', '.span-text', function(){
        var id_doc = $(this).parent().parent().data('time-id');
        var time_te = $(this).text();
        var time_now_date = $(this).parent().parent().parent().parent().find('.start_date').val();
        console.log(time_now_date)
        var day_indexx = get_day_index(new Date(time_now_date))
        booking(id_doc, time_te, day_indexx);
    })
})
$('.start_date').on('blur', function(){
    var ids = $(this).parent().data('doctor-id');
    $('.doctor-'+ids).empty();
    var time_now_date = $(this).val();
    var day = get_day_index(new Date(time_now_date));
    update_time(ids, day);
    add_day();
});
function get_day_cur(){
    return $('#start_date').val();
}
function get_day_index(day){
    return ((day.getDay() + 6) % 7) + 1;
}

function add_day(){
    $('.start_date').each(function(index, value){
        console.log($(this).parent().find('a').addClass("A"))
        $(this).parent().find('a').attr('data-day-cur', $(this).val())
    })
}
function update_time(id, day_index){
    $.ajax({
        'url': "/patient/get-time-available",
        'type': 'GET',
        data: {
            'id': id,
        },
        success: function(data){
            // var day_cur = new Date(get_day_cur());
            time_available = data['available_time']
            var amounts = data['amount'];
            // day_of_week_index =((day_cur.getDay() + 6) % 7) + 1;
            for (var i =0; i < time_available.length; i++){
                if (time_available[i]['day'] == day_index){
                    var a = (time_available[i]['time'].length)
                    // for (var j = 0; j< a; j++){
                    var time = time_available[i]['time']
                    for (var k = 0; k < time.length; k++){
                        var time_template = $('#doctor-time-template').clone().removeAttr('id');
                        time_template.find('.span-text').text(time[k]['time-start'] + '-' + time[k]['time-end']);
                        var t_start = parseTimeString(time[k]['time-start']);
                        var t_end = parseTimeString(time[k]['time-end']);
                        var left = Math.floor(Math.floor((t_end - t_start)/60000 - time[k]['count']*amounts)/amounts);
                        if (left == 0){
                            time_template.addClass('disabled');
                        }
                        time_template.attr('data-time-id', id);
                        time_template.attr('data-date', day_index);
                        // time_template.find('.span-text').attr('data-day-cur');
                        $('.doctor-' + id).append(time_template);
                    }
                    // }
                }
            }
        }
    })
    
}
function booking(doctor_id, time, day){
    var times = day + '-' + time;
    $.ajax({
        'url': '/patient/check-available-to-book',
        'type': 'GET',
        data: {
            'id': doctor_id,
            'time': times,
        },
        success: function(data){
            is_available = data['available'];
            if (is_available){
                window.location.href  = '/patient/book_appointment1/' + doctor_id + '/' + day + '-' + time + '/';
            }
        }
    });
}

function is_available_to_book(id, time){
    var is_available = false;
    $.ajax({
        'url': '/patient/check-available-to-book',
        'type': 'GET',
        data: {
            'id': id,
            'time': time,
        },
        success: function(data){
            is_available = data['available'];
        }
    })
    return is_available;
}

function update_status_time(){
    var doc_node = $('.doctor-info');
    doc_node.each( function(index, value){
        var id = $(this).data('doctor-id');
        var time_node = $('.doctor-time').find('.span-text');
        time_node.each( function(index, value){
            var time = $(this).text();
            var day = $(this).parent().parent().parent().parent().find('.start_date').val();
            var day_index = get_day_index(new Date(day));
            var is_available = is_available_to_book(id, day_index + '-' + time);
            if (is_available){
                $(this).removeClass('disabled');
            } else {
                $(this).addClass('disabled');
            }
        });
    });
}
function parseTimeString(timeString) {
    var parts = timeString.split(":");
    var hours = parseInt(parts[0], 10);
    var minutes = parseInt(parts[1], 10);
    
    var date = new Date();
    date.setHours(hours);
    date.setMinutes(minutes);
    
    return date;
}

$(document).ready(function() {
    $('#info-appointment').submit(function(e) {
        e.preventDefault(); // Ngăn chặn hành động mặc định khi submit form

        // Lấy dữ liệu form
        var formData = $(this).serialize();

        // Gửi dữ liệu form bằng Ajax
        $.ajax({
            url: "/patient/save-appoint/",
            type: "POST",
            data: formData,
            success: function(response) {
                // Xử lý phản hồi từ server (nếu cần)
                console.log(response);
            },
            error: function(xhr, status, error) {
                // Xử lý lỗi (nếu có)
                console.log(error);
            }
        });
    });
});