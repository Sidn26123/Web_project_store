
$(document).ready(function(){
    doctor_table();
    $('#search-submit-btn').on('click', function(){
        doctor_table();
    });
});


function doctor_table(){
    $('#doctor-table').ready(function(){
        var query_string = get_url();
        $('.loader').show();
        $.ajax({
            url: '/ad/get-doctor-table-data/',
            data: query_string,
            success: function(data){
                draw_doctor_table(data);
            },
            failure: function(data){
                alert('Got an error dude');
                $('.loader').hide();
            },
        })
    });
}


function draw_doctor_table(data){
    var table_data = JSON.parse(data.table)
    console.log(table_data)
    if ($.fn.dataTable.isDataTable('#doctor-table')){
        table = $('#doctor-table').DataTable();
    }
    else {
        table = $('#doctor-table').DataTable({
            "paging": true, // Phân trang
            "lengthChange": false, // Thay đổi số lượng bản ghi trên mỗi trang
            "searching": false, // Tìm kiếm
            "ordering": true, // Sắp xếp
            "info": false, // Hiển thị thông tin bảng
            "autoWidth": true, // Điều chỉnh tự động chiều rộng cột
            "responsive": true,
            "columns": [
                {"title": "ID"},
                {"title": "Họ tên",
                    "render": function(data, type, row){
                        return '<div class = "info-doctor" ><img src = ' + row[1][0] + '</img>' + row[1][1] +' </div>';
                    }
                },
                {"title": "Độ tuổi"},
                {"title": "Số điện thoại"},
                {"title": "Email"},
                // {"title": "Noi lam viec"},
                {"title": "Chuc vu"},
                {"title": "Chuyen nganh"},
                {"title": "Danh gia"},
                {"title": "Thu nhap"}
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
