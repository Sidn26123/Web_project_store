$(document).ready(function(){
    var condition = "all";
    patient_info(condition);
    $('.condition-choose-box').click(function(){
        condition = $(this).attr('id');
        patient_info(condition);
    });
});

function patient_info(condition){
    var id = $('.get-id').data('id');
    $.ajax({
        url: '/doctor/get-patient/',
        type: 'GET',
        data: {
            'id': id,
            'condition': condition,
            
        },
        success: function(data) {
            data = JSON.parse(data.patients);
            for (var i =0; i < data.length; i++){
                var template = $('#patient-info-template').clone();

                var id_str = data[i]['id'].toString();
                var id_before = "";
                if (i > 0){
                    id_before = data[i-1]['id'].toString();

                }
                template.find('.patient-id').parent().parent().removeClass(id_before);
                template.find('.patient-id').parent().parent().addClass(id_str);
                template.find('img').prop('src', data[i]['image'])
                template.find('.patient-name').text(data[i]['patient_name']);
                template.find('.patient-phone').text(data[i]['phone']);
                template.find('.patient-age').text(data[i]['age']);
                template.find('.address').text(data[i]['address']);
                template.find('.last-time').text(data[i]['last_time']);
                template.find('.email').text(data[i]['email']);
                template.find('.phone').text(data[i]['phone']);
                template.find('.blood-group').text(data[i]['blood-group']);
                $('#patient-info-wrapper').append(template);
            }
        }
    })
}

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
//                 page.push(items[i]); }

//             return page;
//         },

//         totalPages: function(items, perPage) {
//             // determine total number of pages
//             return Math.ceil(items.length / perPage);
//         },

//         createBtns: function(totalPages, currentPage) {
//             // create buttons to manipulate current page
//             var pagination = $('<div class="pagination" />');

//             // add a "first" button
//             pagination.append('<span class="pagination-button">&laquo;</span>');

//             // add pages inbetween
//             for (var i=1; i <= totalPages; i++) {
//                 // truncate list when too large
//                 if (totalPages > 5 && currentPage !== i) {
//                     // if on first two pages
//                     if (currentPage === 1 || currentPage === 2) {
//                         // show first 5 pages
//                         if (i > 5) continue;
//                     // if on last two pages
//                     } else if (currentPage === totalPages || currentPage === totalPages - 1) {
//                         // show last 5 pages
//                         if (i < totalPages - 4) continue;
//                     // otherwise show 5 pages w/ current in middle
//                     } else {
//                         if (i < currentPage - 2 || i > currentPage + 2) {
//                             continue; }
//                     }
//                 }

//                 // markup for page button
//                 var pageBtn = $('<span class="pagination-button page-num" />');

//                 // add active class for current page
//                 if (i == currentPage) {
//                     pageBtn.addClass('active'); }

//                 // set text to the page number
//                 pageBtn.text(i);

//                 // add button to the container
//                 pagination.append(pageBtn);
//             }

//             // add a "last" button
//             pagination.append($('<span class="pagination-button">&raquo;</span>'));

//             return pagination;
//         },

//         createPage: function(items, currentPage, perPage) {
//             // remove pagination from the page
//             $('.pagination').remove();

//             // set context for the items
//             var container = items.parent(),
//                 // detach items from the page and cast as array
//                 items = items.detach().toArray(),
//                 // get start position and select items for page
//                 startPos = this.startPos(currentPage - 1, perPage),
//                 page = this.getPage(items, startPos, perPage);

//             // loop items and readd to page
//             $.each(page, function(){
//                 // prevent empty items that return as Window
//                 if (this.window === undefined) {
//                     container.append($(this)); }
//             });

//             // prep pagination buttons and add to page
//             var totalPages = this.totalPages(items, perPage),
//                 pageButtons = this.createBtns(totalPages, currentPage);

//             container.after(pageButtons);
//         }
//     };

//     // stuff it all into a jQuery method!
//     $.fn.paginate = function(perPage) {
//         var items = $(this);

//         // default perPage to 5
//         if (isNaN(perPage) || perPage === undefined) {
//             perPage = 5; }

//         // don't fire if fewer items than perPage
//         if (items.length <= perPage) {
//             return true; }

//         // ensure items stay in the same DOM position
//         if (items.length !== items.parent()[0].children.length) {
//             items.wrapAll('<div class="pagination-items" />');
//         }

//         // paginate the items starting at page 1
//         paginate.createPage(items, 1, perPage);

//         // handle click events on the buttons
//         $(document).on('click', '.pagination-button', function(e) {
//             // get current page from active button
//             var currentPage = parseInt($('.pagination-button.active').text(), 10),
//                 newPage = currentPage,
//                 totalPages = paginate.totalPages(items, perPage),
//                 target = $(e.target);

//             // get numbered page
//             newPage = parseInt(target.text(), 10);
//             if (target.text() == '«') newPage = 1;
//             if (target.text() == '»') newPage = totalPages;

//             // ensure newPage is in available range
//             if (newPage > 0 && newPage <= totalPages) {
//                 paginate.createPage(items, newPage, perPage); }
//         });
//     };

// })(jQuery);

// /* This part is just for the demo,
// not actually part of the plugin */
// $('.article-loop').paginate(2);

function get_star_condition(){
    var star_condition = ""
    var star_node = $('.filter-item.checked');
    star_node.each(function(){
        if ($(this).attr('id') != 'all'){
            star_condition += $(this).attr('id')[0] + ',';
        }
    });
    return star_condition[0, star_condition.length - 1];
}

function update_review_stats(doctor_id, star_condition){
    $.ajax({
        url: '/doctor/get-review-data/',
        type: 'GET',
        data: {
            'doctor-id': doctor_id,
            'star-condition': star_condition,
        },
        success: function(data) {
            var star = JSON.parse(data['star_detail'])
            var star_avg = JSON.parse(data['star_avg'])
            var reviews = JSON.parse(data['reviews'])
            console.log(star_avg['avg']);
            $('#rate-point').text(star_avg['avg']);
            $('#amount-rate').text(star_avg['count']);
            $('#5-star').text(star['5']);
            $('#4-star').text(star['4']);
            $('#3-star').text(star['3']);
            $('#2-star').text(star['2']);
            $('#1-star').text(star['1']);
            $('#review-area').empty();
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
    var doctor_id = $('.get-id').data('id');
    var star_condition = get_star_condition();
    update_review_stats(doctor_id, star_condition);
    $('.filter-item').click(function(){
        console.log($(this));
        star_condition = get_star_condition();
        update_review_stats(doctor_id, star_condition);
    });
});

function update_star_condition(node){
    if (node.hasClass('checked') && node.attr('id') == 'all'){
        node.parent().find('check').removeClass('checked');
    }
}

