
$(document).ready(function(){
    get_confirming_table();
})
function get_confirming_table(){
    var id = $('.get-id').data('id');
    $.ajax({
        url: '/doctor/get-confirming-appointment/',
        type: 'GET',
        data: {
            'id': id,
        },
        success: function(data){
            draw_confirming_appointment(data);
        },
    })
}
function draw_confirming_appointment(data){
    var table_data = JSON.parse(data.table)
    if ($.fn.dataTable.isDataTable('#confirming-appoint-table')){
        console.log("a")
        table = $('#confirming-appoint-table').DataTable().clear();
    }
    else {
        table = $('#confirming-appoint-table').DataTable({
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
                        return '<div class = "transaction-id" data-id =' + row[0] + '>' + row[0] + '</div>'; 
                    },
                },
                {"title": "ID bệnh nhân",
                    "render": function(data, type, row){
                        return '<div class = "info-invoice patient-id" data-id =' + row[1] + '>#' + row[1] + '</div>'; 
                    }
                },
                {"title": "Tên bệnh nhân",
                    "render": function(data, type, row){
                        return '<div class = "info-patient" ><img src = "' + row[2][1] + '">' + row[2][0] +' </div>';
                    }
                },
                {"title": "Giới tính"},
                {"title": "Ngày khám"},
                {"title": "Nơi khám"},
                {"title": "Phí"},
                {"title": "Trạng thái"},
                {"title": "",
                    "render": function(){
                        return '<div class = "show__item"><div class ="accept-appointment">Chấp nhận</div><div class ="deny-appointment">Từ chối</div></div>'
                    }
                },
            ],
            drawCallback: function(){
                $('.loader').hide();
            }
        });

    } 
    table.clear();
    table.rows.add(table_data);
    table.draw();
}

$('.accept-appointment').on('click', function(){
    $('.accept-confirm').show();
});

$(document).on('click',function(event){
    var appoint_id = $(event.target).parent().parent().parent().find('.transaction-id').data('id');

    if ($(event.target).attr('class') == 'accept-appointment'){
        window.url = '/doctor/update-appointment-status/';
        $('.accept-confirm').toggle();
        $('.deny-confirm').hide();
    }
    if ($(event.target).attr('class') == 'deny-appointment'){
        $('.deny-confirm').toggle();
        $('.accept-confirm').hide();
    }
    $('.confirm-btn--no').on('click', function(){
        $(this).parent().parent().hide();  
    });
    $('.confirm-btn--yes').on('click', function(){
        var choice = $(this).parent().parent().attr('id');
        $.ajax({
            url: '/doctor/update-appointment-status/',
            type: 'GET',
            data: {
                'appoint_id': appoint_id,
                'choice': choice,
            },
            success: function(data){
                data = JSON.parse(data.row);
                if (data[2] == 'success'){
                    $('.success-notice').find('.transaction-id-span').text(data[0] + " - " + data[1])
                    $('.success-notice').show()
                }
                else if (data[2] = 'denied'){
                    $('.denied-success-notice').find('.transaction-id-span').text(data[0] + " - " + data[1]) 
                    $('.denied-success-notice').show()
                }
            }
        }).then(function(){
            get_confirming_table();
        })
    });
    $('.confirm-btn--yes').on('click', function(){
        $(this).parent().parent().hide();
    });
    $('.confirm-btn--no').on('click', function(){
        $(this).parent().parent().hide();
    });
    $('.success-notice .close-btn').on('click', function(){
        $('.success-notice').hide();
    });
    $('.success-notice .ok-btn').on('click', function(){
        $('.success-notice').hide();
    });
    $('.denied-success-notice .close-btn').on('click', function(){
        $('.denied-success-notice').hide();
    });
    $('.denied-success-notice .ok-btn').on('click', function(){
        $('.denied-success-notice').hide();
    });
});
