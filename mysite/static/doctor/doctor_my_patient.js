
function update_my_patient(){
    var id = $('.get-id').data('id');
    var condition = get_condition();
    console.log(condition)
    $.ajax({
        url: '/doctor/get-patient/',
        type: 'GET',
        data: {
            'id': id,
            'condition': condition,
        },
        success: function(data){
            data = JSON.parse(data.patients);
            $('#patient-info-wrapper').empty();
            for (var i = 0; i < data.length; i++){
                var template = $('#patient-info-template').clone();
                template.removeAttr('id');
                var patient = (data[i]['patient'])
                template.find('.patient-name').text(patient['name']);
                template.find('.patient-id').text(patient['id']);
                template.find('.patient-avatar').attr('src', data[i]['avatar']);
                template.find('.patient-age').text(patient['age']);
                template.find('.patient-phone').text(patient['phone']);
                template.find('.patient-address').text(patient['address']);
                template.find('.last-time').text(data[i]['last_time']);
                template.find('.patient-email').text(patient['email']);
                template.find('.patient-blood-group').text(patient['blood_group']);
                $('#patient-info-wrapper').append(template)
            }
            $('.delete-btn').click(function(){
                var patient_id = $(this).parent().parent().find('.patient-id').text()
                delete_my_patient(patient_id);
            })
            $('.more-info-btn').click(function(){
                $(this).parent().parent().find('.patient-info-more').toggle();
            })
        }
    })
}
function delete_my_patient(patient_id){
    $.ajax({
        url: '/doctor/delete-my-patient/',
        type: 'GET',
        data: {
            'id': patient_id,
        },
        success: function(data) {
            if (data.status == 'ok'){
                alert("Đã xóa thành công")
                $('.id .'+patient_id).remove();
            }
        }
    })
}
// $('.condition-choose-box').on('click', function(){
//     if ($(this).attr('id') == 'all'){
//         if ($(this).hasClass('chose')){
//             $(this).removeClass('chose');
//             $('.condition-choose-box').removeClass('chose');
//         }
//         else {
//             $(this).addClass('chose');
//             $('.condition-choose-box').addClass('chose');
//         }
//     }
//     if ($(this).attr('id' != 'all')){
//         console.log("A")
//         if ($(this).hasClass('chose')){
//             $(this).removeClass('chose');
//             $('#all').removeClass('chose')
//         }
//         else {
//             $(this).addClass('chose');
//             $('#all').removeClass('chose')
//         }
//     }
// })
$(document).ready(function() {
    // Bắt sự kiện click cho các phần tử có class "condition-choose-box"
    update_my_patient();
    $('.condition-choose-box').click(function() {
      // Lấy id của phần tử được click
      var id = $(this).attr('id');
      
      // Kiểm tra nếu click vào phần tử có id là "all"
      if (id === 'all') {
        console.log("A")
        // Thêm / xóa toàn bộ checked cho các phần tử khác
        if ($(this).hasClass('chose')) {
          $('.condition-choose-box').removeClass('chose');
        }
        else{
            $('.condition-choose-box').addClass('chose');
        }
      } else {
        // Prop checked của phần tử được click và xóa checked của phần tử có id là "all"
        $(this).toggleClass('chose');
        $('#all').removeClass('chose');
        }
        update_my_patient();
    });
});
function get_condition(){
    var condition = "";
    $('.condition-choose-box').each(function(index, value){
        if ($(this).hasClass('chose')){
            condition += $(this).attr('id') + ',';
        }
    })
    condition = condition.slice(0, -1);
    return condition
}