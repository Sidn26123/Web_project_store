var overview_chart = null
var overview_reg_chart = null
function update_overview_chart(selected_value){
    $.ajax({
        url: '../../ad/update-overview-chart/',
        type: 'GET',
        data: {
            'selected_value': selected_value,
        },
        success: function (data) {
            var ctx = document.getElementById('overview-chart').getContext('2d');
            if (overview_chart != null){
                overview_chart.destroy()
            }
            overview_chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        label: 'Number of patients',
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                    }]
                }
            });
        }
    });
}

$(document).ready(function () {
    var selected_value = $('#overview-register-chart-selector').val();
    update_overview_reg_chart(selected_value);
    $(document).on('change', '#overview-register-chart-selector', function () {
        selected_value = $(this).val();
        console.log(selected_value)
        update_overview_reg_chart(selected_value);
    });
});
$(document).ready(function () {
    var selected_value = $('#overview-chart-selector').val();
    update_overview_chart(selected_value);
    $(document).on('change', '#overview-chart-selector', function () {
        selected_value = $(this).val();
        console.log(selected_value)
        update_overview_chart(selected_value);
    });
});



function update_overview_reg_chart(selected_value){
    $.ajax({
        url: '../update-overview-reg-chart/',
        type: 'GET',
        data: {
            'selected_value': selected_value,
        },
        success: function (data) {
            var ctx = document.getElementById('overview-register-chart').getContext('2d');
            if (overview_reg_chart != null){
                overview_reg_chart.destroy()
            }
            overview_reg_chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        label: 'Number of patients',
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                    }]
                }
            });
        }
    });
}

var new_register_gender_chart = null;
var new_register_age_chart = null;

$(document).ready(function () {
    $.ajax({
        url: '../get-new-register-amount/',
        type: 'GET',
        success: function (data) {
            $('#new-register-amount').text(data.amount + " " + data.percent_diff);
            var ctx = document.getElementById('gender-proportion-chart').getContext('2d');
            if (new_register_gender_chart != null){
                new_register_gender_chart.destroy()
            }
            new_register_gender_chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.counts,
                        label: "A",
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                    }],
                },
                options: {
                    plugins: {
                        legend: {
                            display: true,
                            labels: {
                                color: 'rgb(255, 99, 132)'
                            }
                        }
                    }
                }
            });
            var ctx = document.getElementById('age-proportion-chart').getContext('2d');
            if (new_register_age_chart != null){
                new_register_age_chart.destroy()
            }
            document.getElementById('age-proportion-chart').height = 300;
            document.getElementById('age-proportion-chart').wight = 300;
            new_register_age_chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.age_labels,
                    datasets: [{
                        data: data.age_count,
                        label: "A",
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                    }],
                },
                options: {
                    plugins: {
                        legend: {
                            display: true,
                            labels: {
                                color: 'rgb(255, 99, 132)'
                            }
                        }
                    }
                }
            });
        } 
    });
});

var patient_account_status = null;
$(document).ready(function(){
    get_status_update();
    //Gọi hàm get_status_update mỗi 5 phút
    setInterval(get_status_update, 1000*60*5);
});

function get_status_update(){
    $.ajax({
        url: '../get-account-status/',
        type: 'GET',
        success: function (data) {
            var ctx = document.getElementById('account-status').getContext('2d');
            if (patient_account_status != null){
                patient_account_status.destroy()
            }
            patient_account_status = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.amounts,
                        label: "Nope",
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                    }],
                },
            });
        }
        
    });
}
// $('.search-submit-btn').on('click', function(event) {
//     var url = get_url();
//     $.ajax({

//     })
// });




function patient_table(data){

    table_data = data.table_data
    if ($.fn.dataTable.isDataTable('#patient-table')){
        table = $('#patient-table').DataTable();
    }
    else {
        table = $('#patient-table').DataTable({
            "paging": true, // Phân trang
            "lengthChange": false, // Thay đổi số lượng bản ghi trên mỗi trang
            "searching": false, // Tìm kiếm
            "ordering": true, // Sắp xếp
            "info": false, // Hiển thị thông tin bảng
            "autoWidth": true, // Điều chỉnh tự động chiều rộng cột
            "responsive": true, // Điều chỉnh độ phản hồi
            'columns': [
                {'title': 'ID', 'data': 0},
                {'title': 'Họ tên ',
                    'render': function (data, type, row) {
                        return '<img src = ' + row[1][0] + ' class = "patient-thumbnail"><span class ="name-span">'+row[1][1] +'</span>';
                    },
                },
                {'title': 'Tuổi'},
                {'title': 'Giới tính'},
                {'title': 'Quê quán'},
                {'title': 'CMND/CCCD'},
                {'title': 'Số điện thoại'},
                {'title': 'Ngày đăng ký'},
                {'title': 'Hoạt động'},
                {'title': 'Hoạt độnga',
                    'render': function (data, type, row) {
                        return '<input class = "page-patient-choose-box" type = "checkbox"' + (row[8] ? 'checked' : '') + '/>';
                    },
                },
            ],
            'columnDefs': [
                // {
                //     'targets': 1,
                //     'render': function (data, type, row) {
                        
                //     }
                // },
                {
                    'targets': 8,
                    'visible': false,
                },

                // { // Cột checkbox (index 2)
                //     // 'targets': 9, // Cột checkbox
                //     "data": null,
                //     "render": function (data, type, row) {
                //         return '<input class = "page-patient-choose-box" type="checkbox" ' + (row[8] ? 'checked' : '') + '/>';
                //     }
                // },
            ],
            drawCallback: function(){
                // Ẩn spinner khi bảng được vẽ xong
                $('.loader').hide();
            }
        });
    }
    table.clear();
    table.rows.add(table_data);
    table.draw();
}
$('#patient-table').ready(function(){
    update_table();
    $('#search-submit-btn').on('click', function(event){
        update_table();
    });
});
function update_table(){
    $('.loader').show();
    // const currentURL = new URL(window.location.href);
    // const queryString = currentURL.search;
    const queryString = get_url();
    $.ajax({
        url: '../get-patient-table/',
        type: 'GET',
        data: queryString,
        success: function (data) {
            patient_table(data);
            // $('.loader').hide();
        }
    });
}

$(document).ready(function(){
    $(document).on('click', '.page-patient-choose-box',function(event){
        event.preventDefault();
        // var box_checked_before = !($(this).is(':checked'));
        var row = $(this).closest('tr');
        var row_data = table.row(row).data();
        var box_checked = $(this).is(':checked');
        var cur_box = $(this);
        $('.page-patient-choose-box-confirm').show()

        $('.page-patient-choose-box-confirm').on('click', '.confirm__yes-btn',function(){
            $('.page-patient-choose-box-confirm').hide();
            $.ajax({
                url: '../update-patient-status/',
                type: 'GET',
                data: {
                    'id': row_data[0],
                    'is_active': row_data[8],
                },
                success: function () {
                    // alert('Cập nhật thành công');
                    cur_box.prop('checked', !box_checked);
                    if (!box_checked){
                        cur_box.addClass('unchecked')
                        cur_box.removeClass('checked');
                    }
                    else{
                        cur_box.addClass('checked');
                        cur_box.removeClass('unchecked');
                    }
                },
                error: function () {
                    alert('Cập nhật thất bại');
                },
            });

        });
        $('.page-patient-choose-box-confirm').on('click', '.confirm__no-btn',function(){
            $('.page-patient-choose-box-confirm').hide();
            console.log("A")
            // $(this).closet('').prop('checked', !box_checked);
        });
        $('.page-patient-choose-box-confirm').on('click', '#change-status-close-btn',function(){
            console.log('close')
            $('.page-patient-choose-box-confirm').hide();
        });
    });
    $(document).on('click', '.patient-thumbnail', function(event) {
        event.stopPropagation() //Nganws chặn sự kiện mở rộng (event click không tác động vào thẻ cha, vì nếu click vào thì sẽ đảo lại status choose nên cần chặn ở thunbmail click tràn ra thẻ chả)
        var row = $(this).closest('tr');
        var row_data = table.row(row).data();
        var p_id = row_data[0]; //Lấy id của patient hiện tại
        // var form_data = new FormData(); //Tạo form data
        $.ajax({
            url: "/ad/get-data-patient",
            data: {
                'id': p_id,
                // 'form_data': form_data,
            },
            success: function(data){ //Thành công thì sẽ lấy data được trả về từ views có url trên
                $('.overlay').addClass('overlay--visible') //Hiển thị overlay
                $('.patient-details').removeClass('hidden') //Hiện patient details div
                $('.overlay').attr('data-id', data.id); //Thêm data-id vào overlay để có thể lấy id của patient hiện tại hoặc lấy từ các nơi khác trong overlay id patient hiện tại
                $('.overlay .name').text(data.name);
                $('.overlay .cccd').text("CCCD/CMND: " + data.citizen_id);
                $('.overlay .phone').text("Điện thoại: " + data.phone);
                $('.overlay .email').text("Email: " + data.email);
                $('.overlay .d_o_b').text("Ngày sinh: " + data.date_of_birth);
                $('.overlay .province').text("Tỉnh/TP" + data.province);
                $('.overlay .address').text("Địa chỉ: " + data.address);
                $('.overlay .age').text("Tuổi: " + data.age);
                $('.overlay .total_appointments').text("Tổng lượt hẹn: " + data.patient_count);
                $('.overlay .total_spent').text("Tổng tiền đã chi: " + data.patient_total)
                // $('.overlay .patient-thumbnail-in-details').attr('src', data.avatar)
                
            }
        })

        // Thêm class patient-details--visible và overlay--visible vào overlay và patient-details
    });
    $(document).on('click', '.overlay', function(event) {
        // Nếu người dùng nhấp vào overlay thì loại bỏ class patient-details--visible và overlay--visible
        $(event.target).removeClass('overlay--visible'); //event.target để hiển thị cái hiện tại (h không cần thiết vì đã build 1 overlay riêng không trong vòng for)
    });
});

$(document).ready(function(){
    var is_change = false;
    var form = $('.patient-details.forms');

    // form.on('change', 'input', function(){ //Nếu có thay đổi trong formƯ
    //     is_change = true;
    // });
    var origin_html = $(".patient-details.d-col-flex").html();
    $(document).on('click', '.edit-profile-btn', function(event) {
        var id = $('.overlay').data('id');
        get_data_patient_to_form(id);
        $('.patient-details.d-col-flex').addClass('hidden'); //Ẩn patient details
        $('.patient-details.d-col-flex.forms').removeClass('hidden'); //Ẩn patient details
        $('.patient-details.d-col-flex.forms').addClass('display'); //Hiện form chỉnh sửa
        is_change = false;
        form.on('change', 'input', function(){ //Nếu có thay đổi trong formƯ
            is_change = true;
            console.log(is_change)
        });
    });
    $('.save-btn').on('click', function(event) { //Save
        var id = $('.overlay').data('id');
        if (is_change){ //Kiểm tra xem có thay đổi gì không
            $('#id-number').val(id)
            console.log($('#id-number').val())
            form.submit();
            is_change = false;
        } else {
            $('.patient-details.forms').removeClass('display'); //Ẩn form chỉnh sửa
            $('.patient-details.d-col-flex').removeClass('hidden'); //Hiện patient details
        }
    });

    $('.delete-btn').on('click', function(){ //Click vào nút xóa thông tin
        var id = $('.overlay').data('id'); //Lấy id của patient hiện tại
        $('.confirm-delete-form').addClass('display'); //Hiện form xác nhận xóa
        $('.confirm-delete-form__delete-btn').on('click', function(event) {
            console.log("ok");
            $.ajax({
                url: "/ad/delete-patient",
                data: {
                    'id':id,
                },
                success: function(){
                    $('.alert.alert-success').show() //Gửi thành công thì hiển thị thông báo
                }
            });
        });
        $('.patient-details.d-col-flex.forms').removeClass('display'); //Hiện form chỉnh sửa
    });
    
    $('.close-details').on('click', function(event) { //Click vào nút close
        $('.patient-details.d-col-flex').addClass('hidden'); //Ẩn patient details
        $('.overlay').removeClass('overlay--visible'); //Ẩn overlay
        $('.patient-details.forms').removeClass('display'); //Ẩn form chỉnh sửa

    });
    $('.close-form-btn').on('click', function(event) { //Khi close form
        if (is_change){ // Nếu có sự thay đổi
            $('.confirm-form').addClass('display'); //Hiện form xác nhận thoát
            $('.confirm-form').on('click', '.confirm-form__save-btn', function(event) { //Lưu và thoát form
                form.submit();
            });
            $('.confirm-form').on('click', '.confirm-form__cancel-btn', function(event) { //Không lưu va thoát
                $('.confirm-form').removeClass('display');
                $('.patient-details.d-col-flex.forms').removeClass('display'); //Ẩn form chỉnh sửa
                $('.patient-details.d-col-flex').removeClass('hidden'); //Hiện patient details
            });
            $('.confirm-form').on('click', '.confirm-form__close-btn', function(event) { //Ẩn confirm-form
                $('.confirm-form').removeClass('display');
            });
        }
        else{
            $('.patient-details.d-col-flex.forms').removeClass('display'); //Ẩn form chỉnh sửa
            $('.patient-details.d-col-flex').removeClass('hidden'); //Hiện patient details
        }
    });
});

function get_data_patient_to_form(id){
    $.ajax({
        url: "/ad/get-data-patient",
        data: {
            'id':id,
        },
        success: function(data){
            var patient_name = data.name;
            var patient_address = data.address;
            var patient_phone = data.phone;
            var patient_account_status = data.account_status;
            $('.name-text').val(patient_name).trigger('change');
            $('.address-text').prop('value', patient_address).trigger('change');
            $('.phone-text').prop('value', patient_phone).trigger('change');
            $('.account-status').prop('checked', patient_account_status).trigger('change');
        }
    });

}

function get_filter_params(){
    const checkbox_choice_list = document.querySelector(".search-filter").querySelectorAll('input[type = "checkbox"]');
    const params = [];
    for (var i = 0; i < checkbox_choice_list.length; i++){
        if (checkbox_choice_list[i].checked){
            params.push(checkbox_choice_list[i].name + "=" + encodeURIComponent(checkbox_choice_list[i].value))
        }
    }
    return params.join("&");
}



function get_order_filter_params(){
    const order_filter_node = document.querySelector("#sort-choice");
    let orders = order_filter_node.value;
    return "sort_by=" + orders.toString();
}

function get_search_input(){
    const search_input = document.querySelector("#search-request-text");
    let search_input_text = search_input.value;
    if (search_input_text){
        return "search_query=" + search_input_text;
    }
    else return ""
}

function change_on_url(name_param, change_value){
    // let url = new URLSearchParams(window.location.href);
    let params = new URLSearchParams(window.location.search);
    //Neu co phan nay thi thay doi
    params.set(name_param, change_value);
    return params;
}


// const next_btn = document.querySelector(".next-btn.next-btn--active")
// if (next_btn){ //Node này có 2 trường hợp, active nếu còn trang sau, disable nếu là trang cuối
//     next_btn.addEventListener("click", function(event){
//         event.preventDefault();
//         const btn_node = document.getElementById('next-btn--actived');
//         //Lấy số trang tiếp theo
//         const pageResults = (parseInt(btn_node.dataset.pageResults)+1).toString();
//         let page = "page";
//         //Lấy url hiện tại
//         let url = new URLSearchParams(window.location.origin);
//         //Cập nhật hoặc thêm vào page = page_next_num trên url
//         let url_paramaters = change_on_url(page, pageResults);
//         //Phần sau ? là các query pamater, lấy từ hàm url_pa...
//         let new_url = window.location.pathname + "?" + url_paramaters.toString();
//         //Chuyển đến url mới
//         window.location.href = new_url;
//     });
// }
// if (document.getElementById("search-submit-btn") != null){  //Nếu có nút search
//     //Tạo url cho query patient để hiển thị kết quả tìm kiếm
//     document.getElementById("search-submit-btn").addEventListener('click', function(event){ //Thực hiện khi click vào submibutton
//         event.preventDefault();
//         let url = get_url();
//         window.location.href = url; //Chuyển đến url mới
//     });
// }
// $('.search-submit-btn').on('click', function(event) {
//     var url = get_url();
// });


function get_url(){
    let params = get_filter_params(); //Lấy các tham số filter là các mục trong phần filter được chọn (click lẻ lần)
    let sorts = get_order_filter_params(); //Lấy từ oder filter
    let search_query = get_search_input(); //Lấy từ search input

    // var url = new URL(window.location.href) + "&" + params;
    //Nếu thêm dấu '/' ở đầu thì nó sẽ tự động lấy đây làm bắt đầu url, nếu khác thì nó sẽ thêm vào sau
    if (search_query !== ""){ //Nếu search_query khác rỗng thì thêm vào url
        var url ='?' + params + "&"+ sorts + "&" + search_query;
    }
    else{
        var url ='?' + params + "&"+ sorts;
    }
    return url;
}