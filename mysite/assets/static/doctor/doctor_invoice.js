function get_search_condition(){
    return $('#search_query').val();
}

function get_time_condition(){
    var time_condition_node = $('#time_condition');
    var time_condition = ""
    time_condition_node.each(function(){
        if ($(this).hasClass('checked')){
            time_condition = $(this).val();
        }
    });
}

function update_time_pos(){
    var time_start = $('#time_start').val();
    var time_end = $('#time_end').val();
    var start = new Date(time_start);
    var end = new Date(time_end);
    if (start > end && (time_start != "" && time_end != "")){
        var temp = time_start;
        time_start = time_end;
        time_end = temp;
        
        $('#time_start').val(time_start);
        $('#time_end').val(time_end);
    }
}

$(document).ready(function(){
    $('.time-condition').click(function(){
        $(this).prop('checked', true);
    });
});

$(document).ready(function(){
    $('.time-condition').blur(function(){
        update_time_pos();
    });
});

function get_invoice_table(){
    var time_condition = get_time_condition();
    var query_condition = get_search_condition();
    var id = $('.get-id').data('id');
    $.ajax({
        url: '/doctor/get-invoice/',
        type: 'GET',
        data: {
            'doctor-id': id,
            'time-condition': time_condition,
            'query-condition': query_condition,
        },
        success: function(data){
            draw_invoice_table(data);
        },
    });
}

function draw_invoice_table(data){
    var table_data = JSON.parse(data.table)
    console.log(table_data)
    if ($.fn.dataTable.isDataTable('#invoice-table')){
        table = $('#invoice-table').DataTable();
    }
    else {
        table = $('#invoice-table').DataTable({
            "paging": true, // Phân trang
            "lengthChange": false, // Thay đổi số lượng bản ghi trên mỗi trang
            "searching": false, // Tìm kiếm
            "ordering": true, // Sắp xếp
            "info": false, // Hiển thị thông tin bảng
            "autoWidth": true, // Điều chỉnh tự động chiều rộng cột
            "responsive": true,
            "columns": [
                {"title": "ID"
                    // "render": function(data, type, row){
                    //     return '<div class = "info-invoice invoice-id" data-id =' + row[0] + '>' + row[0] + '</div>'; 
                    // },
                },
                {"title": "ID bệnh nhân",
                    "render": function(data, type, row){
                        return '<div class = "info-invoice patient-id" data-id =' + row[1] + '>#' + row[1] + '</div>'; 
                    }
                },
                {"title": "Tên bệnh nhân",
                    "render": function(data, type, row){
                        return '<div class = "info-patient" ><img src = ' + row[2][0] + '</img>' + row[2][1] +' </div>';
                    }
                },
                {"title": "Ngày khám"},
                {"title": "Nơi khám"},
                {"title": "Phí"},
                {"title": "Trạng thái"},
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

$(document).ready(function(){
    get_invoice_table();
    $('.submit-time').on('click', function(){
        get_invoice_table();
    });
});