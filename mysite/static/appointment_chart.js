var appoint_bar_chart = null;
var appoint_status_chart = null;

$('#appoint-bar-chart-selector').ready(function () {
    var selected_value = $('#appoint-bar-chart-selector').val();
    get_appoint_bar_chart(selected_value);
    get_appoint_status_chart(selected_value);
    $(document).on('change', '#appoint-bar-chart-selector', function () {
        selected_value = $(this).val();
        get_appoint_status_chart(selected_value);
        get_appoint_bar_chart(selected_value);
    });
});

function get_appoint_bar_chart(selected_value) {
    $.ajax({
        url: '/ad/get-appointment-amounts',
        type: 'GET',
        data: {
            'selected_value': selected_value,
        },
        // dataType: 'json',
        success: function (data) {
            // document.getElementById('appoint-bar-chart').height = 20;
            document.getElementById('appoint-bar-chart').width = 10;
            var ctx = document.getElementById('appoint-bar-chart').getContext('2d');
            if (appoint_bar_chart != null) {
                appoint_bar_chart.destroy();
            }
            appoint_bar_chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'appoint',
                        data: data.amounts,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
            });
        },
        error: function (data) {
            console.log('Error:', data);
        }
    });
}
function get_appoint_status_chart(selected_value){
    $.ajax({
        url: '/ad/get-appointment-status-amounts',
        type: 'GET',
        data: {
            'selected_value': selected_value,
        },
        success: function(data){
            var canvas = document.getElementById('appoint-status-chart');
            var ctx = canvas.getContext('2d');
            if (appoint_status_chart != null){
                appoint_status_chart.destroy()
            }
            appoint_status_chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'appoint',
                        data: data.amounts,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                        ],
                    }]
                },
            });
        }
    });
}
var upcoming_appoint_chart = null;
$('#upcoming-appoint-chart-selector').ready(function () {
    var selected_value = $('#upcoming-appoint-chart-selector').val();
    time_end = ''
    time_start = ''
    var now = new Date();
    var time_now = now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds();
    get_upcoming_appoint_chart(selected_value, time_start, time_end, time_now);
    $(document).on('change', '#upcoming-appoint-chart-selector', function(){
        selected_value = $('#upcoming-appoint-chart-selector').val();
        get_time(selected_value,time_start, time_end, time_now);
    });
    $(document).on('blur', '#upcoming-appoint-chart-start-date, #upcoming-appoint-chart-end-date', function(){
        time_start = $('#upcoming-appoint-chart-start-date').val();
        time_end = $('#upcoming-appoint-chart-end-date').val();
        time_now = now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds();
        get_time(selected_value, time_start, time_end, time_now);
    });

});
function get_upcoming_appoint_chart(selected_value, time_start, time_end, time_now){
    $.ajax({
        url: '/ad/upcoming-appoint-chart-data',
        type: 'GET',
        data: {
            'selected_value': selected_value,
            'time_start': time_start,
            'time_end': time_end,
            'time_now': time_now,
        },
        success: function(data){
            var canvas = document.getElementById('upcoming-appoint-chart');
            var ctx = canvas.getContext('2d');
            if (upcoming_appoint_chart != null){
                upcoming_appoint_chart.destroy()
            }
            upcoming_appoint_chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.line_c_labels,
                    datasets: [{
                        label: 'Upcoming appoint',
                        data: data.line_c_amounts,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                        ],
                    }]
                },
            });
            upcoming_appoint_table(data)
        }
    }); 
}

function get_time(selected_value, time_start, time_end, time_now){
    if (selected_value != 'custom'){
        get_upcoming_appoint_chart(selected_value, time_start, time_end, time_now);
        $('.time-range-selector').hide();
    }
    else{
        $('.time-range-selector').show();
        //checkValidity() chỉ tác dụng trên DOM HTML5 nên phải chuyển qua DOM HTML5 = [0] chứ jquery không hỗ trợ
        var time_start_validate = $('#upcoming-appoint-chart-start-date')[0].checkValidity();
        var time_end_validate = $('#upcoming-appoint-chart-end-date')[0].checkValidity();
        if (time_start_validate && time_end_validate){
            time_start = $('#upcoming-appoint-chart-start-date').val();
            time_end = $('#upcoming-appoint-chart-end-date').val();
            get_upcoming_appoint_chart(selected_value, time_start, time_end, time_now);
        }
    }
}
function upcoming_appoint_table(data){
    table_data = JSON.parse(data.table_data)
    if ( $.fn.dataTable.isDataTable( '#upcoming-appoint-table' ) ) {
        table = $('#upcoming-appoint-table').DataTable();
    }
    else {
        table = $('#upcoming-appoint-table').DataTable( {
            "paging": true, // Phân trang
            "lengthChange": true, // Thay đổi số lượng bản ghi trên mỗi trang
            "searching": false, // Tìm kiếm
            "ordering": true, // Sắp xếp
            "info": false, // Hiển thị thông tin bảng
            "autoWidth": true // Điều chỉnh tự động chiều rộng cột
        } );
    }

    table.clear();
    // for (var i = 0; i < table_data.length; i++){
    //     console.log(typeof(table_data[i]))
    //     table.rows.add(table_data[i]);
    // }
    // table.rows.add([[2,"A","B","201", "D", "1"],[1,"A","B","201", "D", "1"]]);
    // table.row.add([{'ID':1, 'Bác sĩ': "A", "Bệnh nhân": "B", "Thời gian": "201", "Số tiền": 2023, "Chuyên khoa": "A"}]);
    table.rows.add(table_data)
    table.draw();
}
var failed_appoint_chart = null;

function get_failed_appoint_chart(selected_value, time_start, time_end, time_now){
    $.ajax({
        url: '/ad/failed-appoint-chart-data',
        type: 'GET',
        data: {
            'selected_value': selected_value,
            'time_start': time_start,
            'time_end': time_end,
            'time_now': time_now,
        },
        success: function(data){
            var canvas = document.getElementById('failed-appoint-chart');
            var ctx = canvas.getContext('2d');
            if (failed_appoint_chart != null){
                failed_appoint_chart.destroy()
            }
            failed_appoint_chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'failed appoint',
                        data: data.amounts,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                        ],
                    }]
                }
            });
            failed_table(data)
        }
    });
}

function failed_table(data){
    var table_data = JSON.parse(data.table_data)
    if ( $.fn.dataTable.isDataTable( '#failed-appoint-table' ) ) {
        table = $('#failed-appoint-table').DataTable();
    }
    else {
        table = $('#failed-appoint-table').DataTable( {
            "paging": true, // Phân trang
            "lengthChange": true, // Thay đổi số lượng bản ghi trên mỗi trang
            "searching": false, // Tìm kiếm
            "ordering": true, // Sắp xếp
            "info": false, // Hiển thị thông tin bảng
            "autoWidth": true // Điều chỉnh tự động chiều rộng cột
        });
    }
    table.clear();
    table.rows.add(table_data);
    table.draw();
}

function update_failed(){
    var time_start = $('#failed-appoint-chart-start-date').val();
    var time_end = $('#failed-appoint-chart-end-date').val();
    var selected_value = $('#failed-appoint-chart-selector').val();
    var now = new Date()
    var time_now = now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds();
    if (selected_value != 'custom'){
        get_failed_appoint_chart(selected_value, time_start, time_end, time_now);
        $('.failed-chart .time-range-selector').hide();
    }
    else if (selected_value == 'custom'){
        $('.failed-chart .time-range-selector').show();
        var time_start_validate = $('#failed-appoint-chart-start-date')[0].checkValidity();
        var time_end_validate = $('#failed-appoint-chart-end-date')[0].checkValidity();
        if (time_start_validate && time_end_validate && time_start && time_end){
            get_failed_appoint_chart(selected_value, time_start, time_end, time_now);
        }
    }
}
$('#failed-appoint-chart-selector').ready(function () {
    var selected_value = $('#failed-appoint-chart-selector').val();
    var time_start = ''
    var time_end = ''
    var now = new Date();
    var time_now = now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds();
    get_failed_appoint_chart(selected_value, time_start, time_end, time_now);
    $(document).on('change', '#failed-appoint-chart-selector', function () {
        update_failed();
    });
    $(document).on('blur', '#failed-appoint-chart-start-date, #failed-appoint-chart-end-date', function () {
        update_failed();
    });
});

var success_appoint_chart = null;

$('#success-appoint-chart-selector').ready(function () {
    var selected_value = $('#success-appoint-chart-selector').val();
    var time_start = ''
    var time_end = ''
    var now = new Date();
    var time_now = now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds();
    get_success_appoint_chart(selected_value, time_start, time_end, time_now);
    $(document).on('change', '#success-appoint-chart-selector', function(){
        //Cập nhật lại thay đổi trước khi truyền vào
        selected_value = $('#success-appoint-chart-selector').val();
        update_success(selected_value,time_start, time_end, time_now);
    });
    $(document).on('blur', '#success-appoint-chart-start-date, #success-appoint-chart-end-date', function(){
        //Cập nhật lại thay đổi trước khi truyền vào
        time_start = $('#success-appoint-chart-start-date').val();
        time_end = $('#success-appoint-chart-end-date').val();
        time_now = now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds();
        update_success(selected_value, time_start, time_end, time_now);
    });
});


function get_success_appoint_chart(selected_value, time_start, time_end, time_now){
    $.ajax({
        url: '/ad/success-appoint-chart-data',
        type: 'GET',
        data: {
            'selected_value': selected_value,
            'time_start': time_start,
            'time_end': time_end,
            'time_now': time_now,
        },
        success: function(data){
            var canvas = document.getElementById('success-appoint-chart');
            var ctx = canvas.getContext('2d');
            if (success_appoint_chart != null){
                success_appoint_chart.destroy()
            }
            success_appoint_chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'success appoint',
                        data: data.amounts,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                        ],
                    }]
                },
            });
            success_appoint_table(data);
        }
    });
}
function success_appoint_table(data){
    table_data = JSON.parse(data.table_data)
    if ( $.fn.dataTable.isDataTable( '#success-appoint-table' ) ) {
        table = $('#success-appoint-table').DataTable();
    }
    else {
        table = $('#success-appoint-table').DataTable( {
            "paging": true, // Phân trang
            "lengthChange": true, // Thay đổi số lượng bản ghi trên mỗi trang
            "searching": false, // Tìm kiếm
            "ordering": true, // Sắp xếp
            "info": false, // Hiển thị thông tin bảng
            "autoWidth": true // Điều chỉnh tự động chiều rộng cột
        } );
    }

    table.clear();
    table.rows.add(table_data)
    //Cập nhật thay đổi
    table.draw();
}
function update_success(selected_value, time_start, time_end, time_now){
    if (selected_value != 'custom'){
        get_success_appoint_chart(selected_value, time_start, time_end, time_now);
        $('.success-chart .time-range-selector').hide();
    }
    else{
        $('.success-chart .time-range-selector').show();
        //checkValidity() chỉ tác dụng trên DOM HTML5 nên phải chuyển qua DOM HTML5 = [0] chứ jquery không hỗ trợ
        var time_start_validate = $('#success-appoint-chart-start-date')[0].checkValidity();
        var time_end_validate = $('#success-appoint-chart-end-date')[0].checkValidity();
        console.log(time_start_validate)
        if (time_start_validate && time_end_validate){
            time_start = $('#success-appoint-chart-start-date').val();
            time_end = $('#success-appoint-chart-end-date').val();
            get_success_appoint_chart(selected_value, time_start, time_end, time_now);
        }
    }
}
var spec_appoint_chart = null;
var spec_appoint_pie_chart = null;


$('#spec-appoint-chart-selector').ready(function () {
    var selected_value = $('#spec-appoint-chart-selector').val();
    var spec_value = get_checkbox_id_str_chose('spec-selector-checkbox')
    get_spec_appoint_chart(selected_value, spec_value);

    $(document).on('change', '#spec-appoint-chart-selector', function () {
        selected_value = $(this).val();
        // spec_value = update_str_chose_checkbox($('#spec-appoint-chart-selector'),'spec-selector-checkbox')
        spec_value = get_checkbox_id_str_chose('spec-selector-checkbox')
        // update_all_select($('#spec-appoint-chart-selector'),'spec-selector-checkbox')
        get_spec_appoint_chart(selected_value, spec_value);
    });

    $(document).on('change', '.spec-selector-checkbox', function () {
        spec_value = get_checkbox_id_str_chose('spec-selector-checkbox')
        // spec_value = update_str_chose_checkbox($('#spec-appoint-chart-selector'),'spec-selector-checkbox')
        if ($(this).attr('id') == 'spec-all'){
            var is_checked = $(this).prop('checked');
            $('.spec-selector-checkbox').not('#spec-all').prop('checked', is_checked);
            if (is_checked){
                $('[for="spec-all"]').text('Unselect all')
            }
            else{
                $('[for="spec-all"]').text('Select all')
            }
        }
        spec_value = get_checkbox_id_str_chose('spec-selector-checkbox')
        get_spec_appoint_chart(selected_value, spec_value);
    });
});


function get_spec_appoint_chart(selected_value, spec_value, time_start, time_end, time_now){
    $.ajax({
        url: '/ad/spec-appoint-chart-data',
        type: 'GET',
        data: {
            'selected_value': selected_value,
            'spec_value': spec_value,
            'time_start': time_start,
            'time_end': time_end,
            'time_now': time_now,
        },
        success: function(data){
            var canvas = document.getElementById('spec-appoint-chart');
            var ctx = canvas.getContext('2d');
            if (spec_appoint_chart != null){
                spec_appoint_chart.destroy()
            }
            var chart_datasets = []
            var temp = {}
            for (var i = 0; i < data.amounts.length; i++){
                var temp_data = []
                for (var j = 0; j < data.amounts[i].length; j++){
                    temp_data.push(data.amounts[i][j])
                }
                chart_data = {
                    label: data.spec_labels[i],
                    data: temp_data,
                }
                chart_datasets.push(chart_data)
            }
            spec_appoint_chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: chart_datasets,
                            // data: data.amounts,
                            // backgroundColor: [
                            //     'rgba(255, 99, 132, 0.2)',
                            //     'rgba(54, 162, 235, 0.2)',
                            //     'rgba(255, 206, 86, 0.2)',
                            // ],
                },
            });
            var pie_canvas = document.getElementById('spec-appoint-pie-chart');
            var pie_ctx = pie_canvas.getContext('2d');
            if (spec_appoint_pie_chart != null){
                spec_appoint_pie_chart.destroy()
            }
            spec_appoint_pie_chart = new Chart(pie_ctx, {
                type: 'pie',
                data: {
                    labels: data.pie_c_labels,
                    datasets: [{
                        label: 'success appoint',
                        data: data.pie_c_amounts,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                        ],
                    }]
                },
            });
        }
    });
}

function get_checkbox_id_str_chose(checkbox_class){
    var spec_value_node = $('.'+checkbox_class);
    var id_str = '';
    for (var i =0; i < spec_value_node.length; i++){
        if (spec_value_node[i].checked){
            id_str += spec_value_node[i].id + ',';
        }
        //Loại bỏ , cuối cùng
    }
    if (id_str){
        id_str = id_str.slice(0, id_str.length - 1)
    }
    return id_str;
}

// function update_str_chose_checkbox(selector, checkbox_class){
//     var selected_value = selector.val();
//     var spec_str = get_checkbox_id_str_chose(checkbox_class)
//     if (spec_str.slice(0,3) != 'all'){
//         return spec_str;
//     }
//     else if (spec_str.slice(0,3) == 'all'){
//         var spec_value_node = $('.'+checkbox_class);
//         for (var i =0; i < spec_value_node.length; i++){
//             $('#' + spec_value_node[i].id).prop('checked', true);
//         }
//         spec_str = get_checkbox_id_str_chose(checkbox_class)
//         return spec_str;
//     }
// }
function update_all_select(selector, checkbox_class){
    var selected_value = selector.prop('checked');
    var spec_value_node = $('.' + checkbox_class);
    if (selected_value){
        for (var i =0; i < spec_value_node.length; i++){
            if (!(spec_value_node[i].checked)){
            $('#' + spec_value_node[i].id).prop('checked', true);
            }
        }
        selector.innerText = "Bỏ chọn tất cả"

    }
    else{
        console.log(selected_value)
        for (var i =0; i < spec_value_node.length; i++){
            if (spec_value_node[i].checked){
                $('#' + spec_value_node[i].id).prop('checked', false);
            }
        }
        selector.innerText = "Chọn tất cả";
    }
}