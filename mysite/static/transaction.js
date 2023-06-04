$('#transaction-table').ready(function(){
    get_spec_data();
    $('#transaction-details').on('change', function(){
        get_spec_data();
    });
});
function transaction_table(data){
    table_data = JSON.parse(data.table_data);
    if ( $.fn.dataTable.isDataTable( '#transaction-table') ) {
        table = $('#transaction-table').DataTable();
    }
    else {
        table = $('#transaction-table').DataTable( {
            "paging": true, // Phân trang
            "lengthChange": false, // Thay đổi số lượng bản ghi trên mỗi trang
            "searching": false, // Tìm kiếm
            "ordering": true, // Sắp xếp
            "info": false, // Hiển thị thông tin bảng
            "autoWidth": true // Điều chỉnh tự động chiều rộng cột
        });
    }
    table.clear();
    table.rows.add(table_data)
    table.draw();
}
function get_spec_data(){
    $.ajax({
        url: '/ad/get-transactions-data',
        type: 'GET',
        data: {
            'selected_value': $('#transaction-details').val(),
        },
        success: function(data){
            transaction_table(data);
        }
    });
}