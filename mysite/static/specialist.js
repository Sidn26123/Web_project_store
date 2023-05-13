$('#spec-table').ready(function(){
    get_spec_data();
});

function get_spec_data(){
    $.ajax({
        url: '/ad/get-spec-data',
        type: 'GET',
        success: function(data){
            table_data = JSON.parse(data.table_data);
            if ( $.fn.dataTable.isDataTable( '#spec-table' ) ) {
                table = $('#spec-table').DataTable();
            }
            else {
                table = $('#spec-table').DataTable( {
                    "paging": true, // Phân trang
                    "lengthChange": false, // Thay đổi số lượng bản ghi trên mỗi trang
                    "searching": false, // Tìm kiếm
                    "ordering": true, // Sắp xếp
                    "info": false, // Hiển thị thông tin bảng
                    "autoWidth": true // Điều chỉnh tự động chiều rộng cột
                });
                table.clear();
                table.rows.add(table_data)
                table.draw();
            }
        }
    });
}