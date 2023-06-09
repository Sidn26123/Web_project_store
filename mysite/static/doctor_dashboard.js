function update_doctor_info(){
    var doctor_id = $('.get-id').data('id');
    console.log(doctor_id);
    $.ajax({
        url: '/doctor/update-doctor-info/',
        type: 'GET',
        data: {
            'id': doctor_id,
        },
        success: function(data){
            $('.loader').hide();
            doctor = JSON.parse(data.doctor);
            $('#doctor-avatar').attr('src', doctor.avatar);
            $('#name').text(doctor.real_name);
            $('#position').text(doctor.position);
            $('#work_place').text(doctor.work_place);
            $('#work-experience').text(doctor.work_experience);
        },
    })
}

$(document).ready(function(){
    $('.info-table .loader').show();
    update_doctor_info();
});

$(document).ready(function(){
    update_doctor_money();
});

function update_doctor_money() {
    var doctor_id = $('.get-id').data('id');
    $.ajax({
        url: '/doctor/get-money-left/',
        type: 'GET',
        data: {
        'id': doctor_id,
        },
        success: function(data) {
        $('#money-left').text(data.money_left);
        console.log(data['money_left']);
        }
    }).always(function() {
        $.ajax({
        url: '/doctor/get-earn-money/',
        type: 'GET',
        data: {
            'id': doctor_id,
        },
        success: function(data) {
            // console.log(data);
            $('#earned-money').text(data.income);
        }
        });
    });
}

$(document).ready(function(){
    $('#loader-2').show();
    var doctor_id = $('.get-id').data('id');
    $.when(
        $.ajax({
            url: '/doctor/get-total-patient/',
            type: 'GET',
            data: {
                'id': doctor_id,
            }
        }),
        $.ajax({
            url: '/doctor/get-total-appointment/',
            type: 'GET',
            data: {
                'id': doctor_id,
            },

        }),
        $.ajax({
            url: '/doctor/get-appoint-next/',
            type: 'GET',
            data: {
                'id': doctor_id,
            },

        }),
    ).done(function(response1, response2, response3){
        $('#loader-2').hide()
        var total_patient = response1[0].total;
        var total_appointment = response2[0].total;
        var next_appointment = response3[0].next;
        var pending_appointment = response3[0].pending;
        $('#total-patient').text(total_patient);
        $('#total-appointment').text(total_appointment);
        $('#coming-appointment').text(next_appointment);
        $('#pending-appointment').text(pending_appointment);
    });
});

$(document).ready(function(){
    $('#loader-3').show();
    var doctor_id = $('.get-id').data('id');
    $.ajax({
        url: '/doctor/get-rate/',
        type: 'GET',
        data: {
            'id': doctor_id,
        },
        success: function(data){
            $('#loader-3').hide();
            $('#rate-point').text(data.rate.rate);
            $('#amount-rate').text(data.amount);
        }
    });
});

function get_appoint_table(doctor_id){
    var time = get_time_chose();
    $.ajax({
        url: '/doctor/get-appoint-table-data/',
        type: 'GET',
        data: {
            'id': doctor_id,
            'time': time,
        },
        success: function(data){
            draw_appoint_table(data);
        },
    })
}

function get_time_chose(){
    var time_chose_id = $('.condition-choose-box.active').attr('id');
    return time_chose_id;
}
$(document).ready(function(){
    $('#loader-table').show();
    get_appoint_table($('.get-id').data('id'));
});
function draw_appoint_table(data){
    var table_data = JSON.parse(data.table)
    console.log(table_data)
    if ($.fn.dataTable.isDataTable('#doctor-dashboard-appointment')){
        table = $('#doctor-dashboard-appointment').DataTable();
    }
    else {
        table = $('#doctor-dashboard-appointment').DataTable({
            "paging": true, // Phân trang
            "lengthChange": false, // Thay đổi số lượng bản ghi trên mỗi trang
            "searching": false, // Tìm kiếm
            "ordering": true, // Sắp xếp
            "info": false, // Hiển thị thông tin bảng
            "autoWidth": true, // Điều chỉnh tự động chiều rộng cột
            "responsive": true,
            "columns": [
                {"title": "ID",
                    "render": function(data, type, row){
                        return '<div class = "info-appoint appoint-id" data-id =' + row[0] + '>' + row[0] + '</div>'; 
                    },
                },
                {"title": "Tên bệnh nhân",
                    "render": function(data, type, row){
                        return '<div class = "info-patient" ><img src = ' + row[1][0] + '>' + row[1][1] +' </div>';
                    }
                },
                {"title": "Ngày khám"},
                {"title": "Nơi khám"},
                {"title": "Phí"},
                {"title": "",
                    "render": function(){
                        return '<div class = "show__item"><div class ="show-on">Xem</div><div class ="show-off">Xóa</div></div>'
                    }
                },
            ],
            drawCallback: function(){
                $('.loader').hide();
            }
        });
    table.clear();
    table.rows.add(table_data);
    table.draw();
    } 
}

$(document).on('click', '.show-on', function(){
    var appoint_id = $(this).closest('tr').find('.appoint-id').data('id');
    $('.appointment-detail-wrapper').toggleClass('hidden');
    get_appoint_detail(appoint_id);
})

function get_appoint_detail(appoint_id){
    $.ajax({
        url: '/doctor/get-transaction-detail/',
        type: 'GET',
        data: {
            'id': appoint_id,
        },
        success: function(data){
            
            $('.appointment-detail__item img').attr('src', data['patient'][1]);
            $('.appointment-detail__item #patient-name').text(data['patient'][0]);
            $('.appointment-detail__item #birthday').text(data['patient'][2]);
            $('.appointment-detail__item #gender').text(data['patient'][3]);
            $('.appointment-detail__item #province').text(data['patient'][4]);
            $('.appointment-detail__item #book-day').text(data['transaction_time']);
            $('.appointment-detail__item #appointment-day').text(data['appoint_time']);
            $('.appointment-detail__item #cost').text(data['amount_transact']);
            $('.appointment-detail__item #note').text(data['note']);
            $('.appointment-detail__item #status').text(data['status']);
        },
    })
}


// $('').on('click', function(event){
//     $('.add-form').hide();

// })

$(document).ready(function(){
    get_period_available();
    $(document).on('click', '.edit-btn', function(event){
        var date = new Date();
        var hour_1 = date.getHours();
        var hour_2 = hour_1;
        if (hour_1 === 23){
            hour_2 = 0;
        }
        else{
            hour_2 = hour_1 + 1;
        }
        var minute = date.getMinutes();
        var time = hour_1 + ":" + minute;
        $('#start-time').val(time);
        time = hour_1 + ":" + minute;
        $('#end-time').val(time);
        $('.add-form').addClass('show');
    });
    $(document).on('click', '.close-btn-form', function(event){
        $('.add-form').toggleClass('show');
    })
    
    // $(document).on('click', function(event){
    //     if (event.target !== $('.add-form')){
    //         $('.add-form').hide();
    //     }
    // })
});

function get_period_available(){
    var doctor_id = $('.get-id').data('id');
    var day = $('input[name="day-frame-select"]:checked').val();
    if (day === undefined){
        day = 1;
    }
    console.log(day)
    $.ajax({
        url: '/doctor/get-period-available/',
        type: 'GET',
        data: {
            'id': doctor_id,
            'day': day,

        },
        success: function(data){
            data = JSON.parse(data.period);
            for (var i=0; i < data.length; i++){
                var template = $('#period-item-template').clone();
                template.find('span').text(data[i]['time_start'] + "-" + data[i]['time_end']);
                if (data[i]['left'] <= 0){
                    template.addClass('unavailable period-item-unavailable');
                }
                $('.period-area').append(template);

            }
        }
    })
}

$(document).on('click', '.delete-time-frame',function(){
    var chose_day = $('input[name="day-frame-select"]:checked').val();
    var chose_time = $(this).parent().find('span').text();
    var time_arr = chose_time.split('-');
    delete_time_frame(chose_day, time_arr[0], time_arr[1]);
    $(this).parent().remove();
})

$(document).on('click', '.add-time-frame', function(){
    var chose_day = $('span.chose-day').attr('value');
    var time_start = $('#start-time').val();
    var time_end = $('#end-time').val();
    if (time_start > time_end){
        var temp = time_start;
        time_start = time_end;
        time_end = temp;
        $('#start-time').val(time_start);
        $('#end-time').val(time_end);
    }
    add_time_frame(chose_day, time_start, time_end);
})
function delete_time_frame(day, time_start, time_end){
    var doctor_id = $('.get-id').data('id');
    $.ajax({
        url: '/doctor/delete-time-frame/',
        type: 'GET',
        data: {
            'id': doctor_id,
            'day': day,
            'time_start': time_start,
            'time_end': time_end,
        },
        success: function(data){
            console.log(data);
        }
    })
}


function get_time_per_period(){
    var doctor_id = $('.get-id').data('id');
    $.ajax({
        url: '/doctor/get-period-available-show/',
        type: 'GET',
        data: {
            'id': doctor_id,
        },
        success: function(data){
            time_per_appoint = data['time']
            $('#time-per-period option[value='+time_per_appoint+']').prop('selected', true);
        }
    })
}
function update_time_per_period(time_per_period){
    var doctor_id = $('.get-id').data('id');
    console.log(doctor_id)
    $.ajax({
        url: '/doctor/update-time-per-period/',
        type: 'GET',
        data: {
            'id': doctor_id,
            'amount': time_per_period,
        },
        success: function(data){

        }
    })
}
function update_time_period_area(day){
    var doctor_id = $('.get-id').data('id');
    $.ajax({
        url: '/doctor/get-period-available/',
        type: 'GET',
        data: {
            'id': doctor_id,
            'day': day,
        },
        success: function(data){
            data = JSON.parse(data.period)
            for (var i=0; i < data.length; i++){
                var template = $('#period-item-template').clone();
                template.find('span').text(data[i]['time_start'] + "-" + data[i]['time_end']);
                if (data[i]['left'] <= 0){
                    template.addClass('unavailable period-item-unavailable');
                }
                $('.period-area').append(template);
            }
        }
    })
}

function add_time_frame(){
    var doctor_id = $('.get-id').data('id');
    var time_start = $("#start-time").val();
    var time_end = $("#end-time").val();
    var day = $('input[name="day-frame-select"]:checked').val();
    $.ajax({
        url: '/doctor/add-period-available/',
        type: 'GET',
        data: {
            'id': doctor_id,
            'day': day,
            'time_start': time_start,
            'time_end': time_end,
        },
        success: function(data){
        }
    });
    
}
$(document).ready(function(){
    $('#day-1').prop('checked', true);
    get_time_per_period();
    // update_time_period_area($('#day-1').val());
    $('input[name="day-frame-select"]').on('click', function(){
        $('.period-area').empty();
        console.log($(this).val())
        update_time_period_area($(this).val());
    });
    $('#add-time').on('click', function(){
        add_time_frame();
    });
    $('#time-per-period').on('blur', function(){
        update_time_per_period($(this).val());
    });
});