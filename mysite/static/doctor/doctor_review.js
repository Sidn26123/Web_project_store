// $(document).ready(function(){
//     var condition = "all";
//     patient_info(condition);
//     $('.condition-choose-box').click(function(){
//         condition = $(this).attr('id');
//         patient_info(condition);
//     });
// });

// function patient_info(condition){
//     var id = $('.get-id').data('id');
//     $.ajax({
//         url: '/doctor/get-patient/',
//         type: 'GET',
//         data: {
//             'id': id,
//             'condition': condition,
            
//         },
//         success: function(data) {
//             data = JSON.parse(data.patients);
//             for (var i =0; i < data.length; i++){
//                 var template = $('#patient-info-template').clone();

//                 var id_str = data[i]['id'].toString();
//                 var id_before = "";
//                 if (i > 0){
//                     id_before = data[i-1]['id'].toString();

//                 }
//                 template.find('.patient-id').parent().parent().removeClass(id_before);
//                 template.find('.patient-id').parent().parent().addClass(id_str);
//                 template.find('img').prop('src', data[i]['image'])
//                 template.find('.patient-name').text(data[i]['patient_name']);
//                 template.find('.patient-phone').text(data[i]['phone']);
//                 template.find('.patient-age').text(data[i]['age']);
//                 template.find('.address').text(data[i]['address']);
//                 template.find('.last-time').text(data[i]['last_time']);
//                 template.find('.email').text(data[i]['email']);
//                 template.find('.phone').text(data[i]['phone']);
//                 template.find('.blood-group').text(data[i]['blood-group']);
//                 $('#patient-info-wrapper').append(template);
//             }
//         }
//     })
// }

function delete_my_patient(patient_id){
    $.ajax({
        url: '/doctor/delete-my-patient/',
        type: 'GET',
        data: {
            'patient_id': patient_id,
        },
        success: function(data) {
            if (data.status == 'ok'){
                $('.id .'+patient_id).remove();
            }
        }
    })
}
// /*
//  * jQuery Pagination
//  * Author: Austin Wulf (@austinwulf)
//  *
//  * Call the paginate method on an array
//  * of elements. Accepts # of items per page
//  * as an argument. Defaults to 5.
//  *
//  * Example:
//  *     $(selector).paginate(3);
//  *
//  * Released under the MIT License.
//  *
//  * v 1.0
//  */

// (function($){
    
//     var paginate = {
//         startPos: function(pageNumber, perPage) {
//             // determine what array position to start from
//             // based on current page and # per page
//             return pageNumber * perPage;
//         },

//         getPage: function(items, startPos, perPage) {
//             // declare an empty array to hold our page items
//             var page = [];

//             // only get items after the starting position
//             items = items.slice(startPos, items.length);

//             // loop remaining items until max per page
//             for (var i=0; i < perPage; i++) {
function get_star_condition(){
    var ids = [];

    $('.filter-item.checked').each(function() {
        if ($(this).attr('id') != 'all'){

            ids.push($(this).attr('id')[0]);
        }
    });
    
    return ids.join(',');
    // console.log(star_condition)
    // return star_condition[0, star_condition.length - 1];
    // var star_condition = ""
    // var star_node = $('.filter-item');
    // star_node.each(function(){
    //     if ($(this).hasClass('checked')){
    //         // if ($(this).attr('id') == 'all'){
    //         //     star_condition = 'all';
    //         //     return star_condition;
    //         // }
    //         if ($(this).attr('id') != 'all'){
    //             star_condition += $(this).attr('id')[0] + ',';
    //         }
    //     }
    // });
    // return star_condition[0, star_condition.length - 1]
}

function update_review_stats(doctor_id, star_condition){
    console.log(star_condition)
    $.ajax({
        url: '/doctor/get-review-data/',
        type: 'GET',
        data: {
            'doctor-id': doctor_id,
            'star-condition': star_condition,
        },
        success: function(data) {
            $('#review-area').empty();
            var star = JSON.parse(data['star_detail'])
            var star_avg = JSON.parse(data['star_avg'])
            var reviews = JSON.parse(data['reviews'])
            var doctor = JSON.parse(data['doctor']);
            $('.doctor-info').find("img").attr('src', doctor['avatar']);
            $('#doctor-name').text(doctor['real_name']);
            $('#rate-point').text(star_avg['avg']);
            $('#amount-rate').text(star_avg['count']);
            $('#5-star').text(star['5']);
            $('#4-star').text(star['4']);
            $('#3-star').text(star['3']);
            $('#2-star').text(star['2']);
            $('#1-star').text(star['1']);
            for (var i = 0; i < reviews.length; i++){
                var template = $('#review-template').clone();
                template.find('.reviewer-avatar').attr('class', reviews[i]['avatar']);
                template.find('.reviewer-name').text(reviews[i]['name']);
                template.find('.review-time').text(reviews[i]['time_review'])
                template.find('.rates').text(reviews[i]['rate'])
                template.find('.review-content').text(reviews[i]['feedback'])
                $('#review-area').append(template)
            }
        }
    })
}

$(document).ready(function(){

});

// function get_star_condition(node){
//     var str = ""
//     $('.filter-item').each(function(){
//         if (this.hasClass('checked')){
//             str += this.attr('id')[0] + ',';
//         }
//     })
//     return str[0, str.length - 1];
// }

$(document).ready(function() {
    var doctor_id = $('.get-id').data('id');
    var star_condition = get_star_condition();
    update_review_stats(doctor_id, star_condition);

    $('.filter-item').on('click', function() {
        var clickedItemId = $(this).attr('id');
        if (clickedItemId === 'all') {
            // Kiểm tra nút "Tất cả" đã được chọn hay chưa
            if ($(this).hasClass('checked')) {
            // Nếu đã được chọn, loại bỏ checked cho tất cả các phần tử khác
            $('.filter-item').removeClass('checked');
            } else {
            // Nếu chưa được chọn, thêm checked cho tất cả các phần tử
            $('.filter-item').addClass('checked');
            }
        } else {
            // Nếu click vào nút khác, tắt checked của nút "Tất cả" nếu có
            $('#all').removeClass('checked');
            
            $(this).toggleClass('checked');

        }
        star_condition = get_star_condition();
        update_review_stats(doctor_id, star_condition);
    });
});

