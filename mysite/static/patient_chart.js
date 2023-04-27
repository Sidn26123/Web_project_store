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