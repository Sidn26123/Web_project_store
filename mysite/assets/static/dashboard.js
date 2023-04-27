// var contx = document.getElementById("test-canvas").getContext('2d');
// var my_chart = new Chart(contx, {
//     type: 'bar',
//     data: {
//         labels : ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
//         datasets:[{
//             label: "Test chart",
//             data: [10,1,2,6],
//             backgroundColor: 'rgba(54, 162, 235, 0.2)',
//             borderColor: 'rgba(54, 162, 235, 1)',
//             borderWidth:1,
//         }]
//     },
//     // option: {
//     //     scales:{
//     //         yAxes: [{
//     //             ticks: {
//     //                 begin: {
//     //                     beginAtZero: true,
//     //                 }
//     //             }
//     //         }]
//     //     }
//     // }
// });

//AJAX patient
$(document).ready(function() {
    $('#patient-choose-time-box').on('change', function() {
        var selected_value = $(this).val(); // lấy giá trị đã chọn
        $.ajax({
            url: '/ad/get-new-data',
            // type: 'POST',
            data: {
                'selected_value': selected_value
            },
            success: function(data) {
                $('#patient-new-register-total').html('<span>Đăng ký hôm nay ' + data.total_registers + '</span>')
            },
            error: function(error) {
                console.log(error)
            },
        });
    });
});

//Doctor
$(document).ready(function() {
    $('#doctor-choose-time-box').on('change', function() {
        var selected_value = $(this).val(); // lấy giá trị đã chọn
        $.ajax({
            url: '/ad/get-new-data-doctor',
            // type: 'POST',
            data: {
                'selected_value': selected_value
            },
            success: function(data) {
                $('#doctor-new-register-total').html('<span>Đăng ký hôm nay ' + data.total_registers + '</span>')
            },
            error: function(error) {
                console.log(error)
            },
        });
    });
});


//appointment
$(document).ready(function() {
    $('#patient-choose-time-box').on('change', function() {
        var selected_value = $(this).val(); // lấy giá trị đã chọn
        $.ajax({
            url: '/ad/get-new-data-booking',
            // type: 'POST',
            data: {
                'selected_value': selected_value
            },
            success: function(data) {
                $('#booking-total').html('<span>Tống lượt đặt hẹn hôm nay ' + data.total_appointments + '</span>')
            },
            error: function(error) {
                console.log(error)
            },
        });
    });
});

$(document).ready(function() {
    $('#transaction-amount-choose-time-box').on('change', function() {
        var selected_value = $(this).val(); // lấy giá trị đã chọn
        $.ajax({
            url: '/ad/get-new-data-transaction',
            // type: 'POST',
            data: {
                'selected_value': selected_value
            },
            success: function(data) {
                $('#finance-total').html('<span>Tổng giao dịch hôm nay ' + data.total + '</span>')
            },
            error: function(error) {
                console.log(error)
            },
        });
    });
});
//Biến toàn cục 
var appoint_chart_months = null;
var appoint_chart_states = null;

function update_appoint_chart(selected_value){
    $.ajax({
        url: '../appoints-total',
        data:{
            'selected_value': selected_value
        },
        success: function(data){
            var canvas = document.getElementById("appointment-in-months-chart")
            var span_replace = document.getElementById("appointer-chart-wrapper")
            if (span_replace !== null){
                span_replace.parentNode.replaceChild(canvas, span_replace);
            }
            canvas.style.display = "block";
            var contx = document.getElementById("appointment-in-months-chart").getContext('2d');
            if (appoint_chart_months !== null) {
                appoint_chart_months.destroy();
            }
            appoint_chart_months = new Chart(contx, {
                type: 'bar',
                data: {
                    labels: data.months,
                    datasets: [{
                        data :  data.appoints_list,
                        label: "My dataset", // Tên của dataset
                        borderColor: "#3e95cd", // Màu viền của đường
                        fill: false // Không tô màu nền
                    }]
                }
            });
        }
    });
}
$(document).ready(function(){
    var selected_value = document.getElementById("appoint-years").value
    update_appoint_chart(selected_value);
    $('#appoint-years').on('change', function() {
        selected_value = $(this).val(); // lấy giá trị đã chọn
        update_appoint_chart(selected_value)
    });
});



function update_appoint_state_chart(selected_value){
    $.ajax({
        url: '../appoints-state-data',
        data:{
            'selected_value': selected_value
        },
        success: function(data){
            var canvas = document.getElementById("appointment-state-chart")
            var span_replace = document.getElementById("appointment-state-span")
            if (span_replace){
                span_replace.parentNode.replaceChild(canvas, span_replace);
            }
            canvas.style.display = "block";
            var contxs = document.getElementById("appointment-state-chart").getContext('2d');
            if (appoint_chart_states !== null){
                appoint_chart_states.destroy();
            }
            appoint_chart_states = new Chart(contxs, {
                type: 'pie',
                data: {
                    labels: JSON.parse(data.labels),
                    datasets: [{
                        data :  JSON.parse(data.values),
                        label: "My dataset", // Tên của dataset
                        borderColor: "#3e95cd", // Màu viền của đường
                        fill: false // Không tô màu nền
                    }]
                },
                option: {
                    plugins: {
                        legend: {
                            display: true,
                            position: {x: 10, y: 10},
                        }
                    },
                }
            });
        }
    });
}
$(document).ready(function(){
    var selected_value = document.getElementById("appoint-state-choose-box").value
    update_appoint_state_chart(selected_value);
    $('#appoint-state-choose-box').on('change', function() {
        selected_value = $(this).val(); // lấy giá trị đã chọn
        update_appoint_state_chart(selected_value);
    });
});


function update_specialities_table(selected_value){
    $.ajax({
        url: '../specialities_table_data', //Link lấy data
        data: {
            'selected_value': selected_value,
        },
        success: function(data){
            
            var tbody = document.getElementById("spec-list-body");
            tbody.innerHTML = '';
            // table_body.empty(); //Xóa nội dung trong body
            var tr = document.createElement('tr');
            
            data.data.forEach(obj =>{
                console.log(obj)
                var td = document.createElement('td');
                td.textContent = obj.medical_specialty__name;
                tr.appendChild(td);
                console.log(tr)

            });
            tbody.appendChild(tr);

            }
        });
    }


$(document).ready(function(){
    var selected_value = document.getElementById("speciality-selections").value
    update_specialities_table(selected_value);
    $("#speciality-selections").on('change', function(selected_value){
        update_specialities_table(selected_value);
    })
});

// var data = [
//     {key1: 'value1', key2: 'value2', key3: 'value3'},
//     {key1: 'value4', key2: 'value5', key3: 'value6'},
//     {key1: 'value7', key2: 'value8', key3: 'value9'}
// ];

// Lấy phần tử tbody
// var tbody = document.querySelector('#myTable tbody');

// // Xóa các hàng hiện có trong tbody
// tbody.innerHTML = '';

// // Lặp qua các phần tử trong data
// for (var i = 0; i < data.length; i++) {
//     // Tạo một hàng mới
//     var tr = document.createElement('tr');

//     // Lặp qua các thuộc tính của đối tượng hiện tại
//     for (var key in data[i]) {
//         // Tạo một ô mới
//         var td = document.createElement('td');

//         // Đặt nội dung của ô bằng giá trị của thuộc tính hiện tại
//         td.textContent = data[i][key];

//         // Thêm ô vào hàng
//         tr.appendChild(td);
//     }

//     // Thêm hàng vào tbody
//     tbody.appendChild(tr);
// }
var spec_income_chart = null;
function update_spec_income_chart(selected_value){
    $.ajax({
        url: '../spec-income-chart-data',
        data: {
            'selected_value': selected_value,
        },
        success: function(data){
            // console.log(data.data)
            var canvas = document.getElementById("specialty-income-chart")
            var span_replace = document.getElementById("specialty-income-chart-wrapper")
            if (span_replace !== null){
                span_replace.parentNode.replaceChild(canvas, span_replace);
            }
            canvas.style.display = "block";
            var contx = document.getElementById("specialty-income-chart").getContext('2d');
            if (spec_income_chart !== null) {
                spec_income_chart.destroy();
            }
            spec_income_chart = new Chart(contx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data :  data.amounts,
                        label: "My dataset", // Tên của dataset
                        borderColor: "#3e95cd", // Màu viền của đường
                        fill: false // Không tô màu nền
                    }]
                    // {
                    //     label: "2",
                    //     data: [1,5,3,2],
                        
                    // }]
                },
                // options: {
                //     responsive: true,
                //     scales: {
                //         yAxes: [{
                //             ticks: {
                //                 beginAtZero: true
                //             }
                //         }]
                //     }
                // }
            });
        }
    });
}
$(document).ready(function(){
    var selected_value = document.getElementById("speciality-time-select-box").value
    update_spec_income_chart(selected_value);
    $('#speciality-time-select-box').on('change', function() {
        selected_value = $(this).val(); // lấy giá trị đã chọn
        update_spec_income_chart(selected_value);
    });
});


// $(document).ready(function(){
//     var data_row = [1,2,3,45];
//     // document.querySelector(".export-list button").on('change', function(){
//     //     $('#patient-list input[name="chose-checkbox"]:checked').each(function(){
//     //         var row = {};
//     //         row.id = $(this).closest('tr').find('.page-obj-id').text();
//     //         row.age = $(this).closest('tr').find('.page-obj-age').text();
//     //         row.gender= $(this).closest('tr').find('.page-obj-gender').text();
//     //         row.province = $(this).closest('tr').find('.page-obj-province').text();
//     //         data_row.push(row);
//     //     });
//         $.ajax({
//             type: 'POST',
//             url: '../export_file',
//             data:{
//                 'datas': JSON.stringify(data_row),
//             },
//             // data: {
//             //     'data': request.POST.data,
//             // },
//             success: function(response){
//                 console.log(response)
//             }
//         });

//     });
// });

$(document).ready(function(){
    var data_row = [1,2,3,4,5];
        $.ajax({
            type: 'POST',
            url: '../export_file',
            data:{
                'data': JSON.stringify(data_row),
            },
            success: function(response){
                console.log(response)
            }
        });

    });

