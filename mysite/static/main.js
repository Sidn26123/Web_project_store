function toggleActive(element) {
    element.classList.toggle("active");
}

document.addEventListener("DOMContentLoaded", (event)=>{
    //Lấy node back button
    const back_button = document.querySelector(".back-btn.back-btn--disable");
    //Kiểm tra node này có tồn tại hay không (chỉ tồn tại khi phân trang hiện tại là trang đầu do if else)
    if (back_button != null){
        //Nếu phân trang hiện tại là trang đầu, thêm listener click 
        back_button.addEventListener('click', function(event){
            //Ngăn lại các hành vi mặc định
            event.preventDefault();
            //Thêm class vào class hiện tại của node này
            back_button.parentNode.classList.add("button--disable");
            back_button.removeAttribute("href");
        });
    }
    const next_button = document.querySelector(".next-btn.next-btn--disable");
    if (next_button != null){
        next_button.addEventListener('click', (event)=>{
            event.preventDefault();
            next_button.parentNode.classList.add("button--disable");
            next_button.removeAttribute("href");
        });
    }

});
// //stopPropagation chặn lại không thực hiện
// if (document.querySelector(".patient-details")){
//     document.querySelector(".patient-details").addEventListener('click', (event)=>{
//         event.stopPropagation();
//     });
// }



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


const next_btn = document.querySelector(".next-btn.next-btn--active")
if (next_btn){ //Node này có 2 trường hợp, active nếu còn trang sau, disable nếu là trang cuối
    next_btn.addEventListener("click", function(event){
        event.preventDefault();
        const btn_node = document.getElementById('next-btn--actived');
        //Lấy số trang tiếp theo
        const pageResults = (parseInt(btn_node.dataset.pageResults)+1).toString();
        let page = "page";
        //Lấy url hiện tại
        let url = new URLSearchParams(window.location.origin);
        //Cập nhật hoặc thêm vào page = page_next_num trên url
        let url_paramaters = change_on_url(page, pageResults);
        //Phần sau ? là các query pamater, lấy từ hàm url_pa...
        let new_url = window.location.pathname + "?" + url_paramaters.toString();
        //Chuyển đến url mới
        window.location.href = new_url;
    });
}
if (document.getElementById("search-submit-btn") != null){  //Nếu có nút search
    //Tạo url cho query patient để hiển thị kết quả tìm kiếm
    document.getElementById("search-submit-btn").addEventListener('click', function(event){ //Thực hiện khi click vào submibutton
        event.preventDefault();
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
        window.location.href = url; //Chuyển đến url mới
    });
}


// document.getElementById("sort-choice").addEventListener('change', function(){
//     var selected_value = this.value;
//     const patient_data = document.getElementById('order-filter-select')
//     const patientData = patient_data.dataset.patientData;
//     if (selected_value == '0'){
//     };
// });

// var filter_item_chose = document.querySelectorAll(".items-container");
// filter_item_chose.forEach((items)=>{
//     items.addEventListener("click", (event)=>{
//         if (event.target.tagName.toLowerCase() === 'label') {
//             const parent = event.target.parentNode;
            
//             if (!event.target.checked){
//                 event.
//                 parent.classList.add('checkbox-custom-checked');
//             }
//             else{
//                 parent.classList.remove('checkbox-custom-checked');
//             }
        
//             // event.target.checked = !event.target.checked

//             // Thêm vào node cha đầu tiên của label đó
//         }
//             // if (event.target.firstElementChild.checked){
//             //     event.target.classList.add("item-chose");
//             // }
//             // else{
//             //     event.target.classList.remove("item-chose")
//             // }
//     });
// });

//Thay đổi trạng thái của các filter query item tương ứng khi click vào
$(document).on('click', '.search-filter__item', function(event) {
    event.preventDefault(); //Ngăn chặn sự kiện mặc định của thẻ
    var $checkbox = $(this).find('input[type="checkbox"]'); //Chọn tất cả node input có type là checkbox
    if (!$checkbox.prop('checked')) { //Nếu node checked = false
        $(this).addClass('checkbox-custom-checked'); //Thêm class vào node hiện tại click
        $checkbox.prop('checked', true); //Chuyển trạng thái checked của node input (con của this) thành true  
    } else {    //Nếu node đó đã được chọn
        $(this).removeClass('checkbox-custom-checked'); //Xóa class
        $checkbox.prop('checked', false);
    }
});

// var navbar_item = document.querySelector(".navbar-item-list");
// var navbar_items = navbar_item.querySelectorAll(".navbar-item-list__item")
// navbar_items.forEach(item => {
//     item.addEventListener("click", (event)=>{
//         event.preventDefault()
//         navbar_items.forEach(item =>{
//             item.classList.remove("navbar-item--active")
//         });
//         event.target.parentNode.classList.add("navbar-item--active");
//         window.location.href = "/a/"
//     });
// });

//Ajax cho hiển thị active patient

//Hiển thị thông tin patient khi click vào thumbnail
$(document).ready(function(){
    $(document).on('click', '.patient-thumbnail', function(event) {
        event.stopPropagation() //Nganws chặn sự kiện mở rộng (event click không tác động vào thẻ cha, vì nếu click vào thì sẽ đảo lại status choose nên cần chặn ở thunbmail click tràn ra thẻ chả)
        var p_id = $(this).data('id-patient'); //Lấy id của patient hiện tại
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
});


//Bỏ hiển thị nếu click vào overlay
$(document).on('click', '.overlay', function(event) {
    // Nếu người dùng nhấp vào overlay thì loại bỏ class patient-details--visible và overlay--visible
    $(event.target).removeClass('overlay--visible'); //event.target để hiển thị cái hiện tại (h không cần thiết vì đã build 1 overlay riêng không trong vòng for)
});



//Hiện form khi click vào nút thêm mới
$(document).ready(function(){
    var is_change = false;
    var origin_html = $(".patient-details.d-col-flex").html();
    $(document).on('click', '.edit-profile-btn', function(event) {
        var id = $('.overlay').data('id');
        get_data_patient_to_form(id);
        $('.patient-details.d-col-flex').addClass('hidden'); //Ẩn patient details
        $('.patient-details.d-col-flex.forms').removeClass('hidden'); //Ẩn patient details
        $('.patient-details.d-col-flex.forms').addClass('display'); //Hiện form chỉnh sửa
        
        var form = $('.patient-details.forms');

        form.on('change', 'input', function(){ //Nếu có thay đổi trong formƯ
            is_change = true;
        });

        $('.save-btn').on('click', function(event) { //Save
            if (is_change){ //Kiểm tra xem có thay đổi gì không
                $('.id-text').prop('value', id);
                form.submit();
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
});
//In list class của element được click
// $(document).ready(function() {
//     $("body").on("click", function(event) {
//         var classes = $(event.target).attr("class").split(" ");
//         console.log(classes);
//     });
// });
// $(document).ready(function(){
//     var is_change = false;
//     var origin_html = $(".patient-details.d-col-flex").html();
//     $('.edit-profile-btn').on('click', function(){ //Click vào nút edit
//         $('.patient-details.d-col-flex').addClass('hidden');
//         $('.patient-details.d-col-flex.forms').addClass('display'); //Hiện form chỉnh sửa
//         var forms = $('.patient-details.d-col-flex.forms');
//         $('.patient-details.d-col-flex.forms').on('change', 'input', function(){ //Nếu có thay đổi trong form
//             is_change = true;
//         });
//         $('.patient-details.d-col-flex.forms').on('click', 'save-btn', function(){ //Save
//             if (is_change){ //Kiểm tra có change không, nếu có thì sumbit form lên server
//                 forms.submit();
//             }
//             else{ //Không có thì hiển thị lại thông tin ban đầu
//                 // $('.patient-details.d-col-flex').html(origin_html);
//                 $('.patient-details.d-col-flex').removeClass('hidden');
//                 $('.patient-details.d-col-flex.forms').removeClass('display');
//             }
//         });
//         $('.patient-details.d-col-flex.forms').on('click', '.close-form-btn', function(){ //Close form
//             if (is_change){ //kiểm tra có thay đổi trên form k
//                 $('.confirm-form').addClass('display')
//                 $('.confirm-save-btn').on('click', function(){
//                     forms.submit();
//                 });
//                 $('.confirm-close-btn').on('click', function(){
//                     $('.confirm-form').removeClass('display')
//                 });
//                 $('.confirm-out-btn').on('click', function(){
//                     $('.confirm-form').removeClass('display')
//                     $('.patient-details.d-col-flex').hide();
//                     $('.patient-details.d-col-flex.forms').hide();
//                 });
//             }
//             else{
//                 $('.patient-details.d-col-flex').show();
//                 $('.patient-details.d-col-flex.forms').hide();
//             }
//         });
//     });
//     $('.delete-btn').on('click', function(){
//         var id = $('.overlay').data('id'); //Lấy id của patient hiện tại
//         $('.confirm-delete-form').show()
//         $('.confirm-delete-form').on('click', '.confirm-delete-form__save-btn', function(event) {
//             $.ajax({
//                 url: "/ad/delete-patient",
//                 data: {
//                     'id':id,
//                 },
//                 success: function(){
//                     $('.alert.alert-success').show() //Gửi thành công thì hiển thị thông báo
//                 }
//             });
//         }); //Lưu và thoát form
//         $('.confirm-delete-form').on('click', '.confirm-delete-form__cancel-btn', function(event) {
//             $('.confirm-delete-form').hide();
//         });
//         $('.confirm-delete-form').on('click', '.confirm-delete-form__close-btn', function(event) {
//             $('.confirm-delete-form').hide();
//         });
//         // $.ajax({
//         //     url: "/ad/delete-patient",
//         //     data: {
//         //         'id':id,
//         //     },
//         //     success: function(){
//         //         $('.alert.alert-success').show() //Gửi thành công thì hiển thị thông báo
//         //     }
//         // });
//     });
// });

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
            $('.name-text').prop('value', patient_name).trigger('change');
            $('.address-text').prop('value', patient_address).trigger('change');
            $('.phone-text').prop('value', patient_phone).trigger('change');
            $('.account-status').prop('checked', patient_account_status).trigger('change');
        }
    });

}

function change_active_status(status){
    if (status == true){
        $('.page-item.active').text('Đang hoạt động');
    }
    else{
        $('.page-item.active').text('Đã khóa');
    }
}




//Download file csv với những patient được chọn
$(document).ready(function(){
    $(document).on('click', '.table-tr', function(){
        $(this).find(".row-choose").prop("checked", !$(this).find(".row-choose").prop("checked"));
        var chose = $('.row-choose:checked');   //Select toàn bộ checkbox có row
        var id_list = [];
        for (var i =0; i < chose.length; i++){
            var id = $(chose[i]).closest('tr').find('.patient-thumbnail').data('id-patient'); //Đẩy id của tất cả những checkbox được chọn
            // var p_id =  $(chose[i]).data('id-patient')
            id_list[i] = id;
        }
        // console.log($(chose[0])s.data('id-patient'))
        $.ajax({
            type: "GET",
            url: "/ad/get-data-patients",
            data:{
                'id': JSON.stringify(id_list) //Chuyển đổi list thành json string dể đưa lên url
            },
            success: function(response){
                // print(response) //Dòng code này gọi tính năng in cảu trình duyệt
                $('.export-file-btn').on('click', function(){
                    var downloadLink = document.createElement("a");
                    downloadLink.href = window.URL.createObjectURL(new Blob([response])); //tạo url với tham số là 1 đối tượng blob(large-object-binary đối tượng nhị phân lớn như file, media... ở đây là response)
                    downloadLink.setAttribute("download", "mydata.csv");
                    document.body.appendChild(downloadLink);
                    downloadLink.click();
                });
            }
        });
        // update_chose_item_in_filter(id_list);
        console.log(id_list)
    });
});

// $(".table-tr").on('click', function(){
    // $(this).find(".row-choose").prop("checked", !$(this).find(".row-choose").prop("checked"));
// });

//Toggle hiện thị export menu
$('.export-file-b').on('click', function() {
    $(".export-file-menu").toggleClass("display");
});




$(document).ready(function(){
    $(document).on('click', '.add-patient-btn', function(){
        var is_change = false;
        var original_form = $('.add-patient-form').html();
        $('.add-patient-form').show();
        $('.add-patient-form').on('change', 'input', function(event) {
            console.log('change')
            is_change = true;
        });
        var form = $('.add-patient-form');
        form.on('click', '.add-patient-form-submit-btn', function(event) {
            form.submit()
        });
        $('.add-patient-form').on('click', '.add-patient-form-cancel-btn', function(event) {
            console.log(is_change)
            if (is_change){
                $('.confirm-cancel-add-patient-form').show();
                $('.confirm-cancel-add-patient-form').on('click', '.add-patient-form-cancel-btn', function(event) {
                    $('.confirm-cancel-add-patient-form').hide();
                });
                $('.confirm-cancel-add-patient-form').on('click', '.confirm-cancel-add-patient-form-btn .leave-btn', function(event) {
                    $('.confirm-cancel-add-patient-form').hide();
                    $('.add-patient-form').html(original_form);
                    $('.add-patient-form').hide();
                    is_change = false;
                });
                $('.confirm-cancel-add-patient-form').on('click', '.confirm-cancel-add-patient-form-btn .stay-btn', function(event) {
                    $('.confirm-cancel-add-patient-form').hide();
                });
            }
            else{
                $('.add-patient-form').html(original_form);
                $('.add-patient-form').hide();
            }
        });
    });
});


//Toggle hiện thị menu chọn filter lọc
$(document).ready(function(){
    $(document).on('click', '.province-expand-btn', function(){
        $(this).closest('.search-filter__items').find('.items-container.patient-province').toggle();
    });
});


// function update_chose_item_in_filter(id_list){
//     var item_chose_div = createElement("div");
//     item_chose_div.addClass("items-chose-display-area");
//     for (var i =0; i< id_list.length; i++){
//         var item_div_container = createElement("div");
//         item_div_container.addClass("item-chose");
//         var item_name = createElement("div");
//         item_name.addClass("item-chose-name d-row-flex");
//         var delete_btn = createElement("i");
//         delete_btn.addClass("fa-regular fa-circle-xmark close-btn delete-item-chose-btn");
//         item_div_container.append(item_name);
//         item_div_container.append(delete_btn);
//     $.ajax({
//         url: '/ad/get-name-list-chosen-item',
//         data: {
//             'id_list': JSON.stringify(id_list)
//         },
//         success: function(data){

//             }
//         }
//     });     
// }

$(document).ready(function(){
    $(document).on('click', '.search-filter__item', function(){
        $('.items-chose-display-area').empty()
        var id_list = [];
        var inner_text = [];
        var id_list_s = $('.search-filter .search-filter__item-checkbox:checked');
        console.log(id_list_s.length)
        id_list_s.each(function(){
            var id = $(this).attr("id");
            id_list.push(id);
            var label_text = $('label[for="'+id+'"]').text();
            inner_text.push(label_text);
        });
        for (var i = 0; i < id_list.length; i++){
            var item_div_container = $("<div>");
            item_div_container.addClass("item-chose d-row-flex");
            var item_name = $("<div>");
            item_name.addClass("item-chose-name");
            item_name.text(inner_text[i]);
            var delete_btn = $("<i>");
            delete_btn.addClass("fa-regular fa-circle-xmark close-btn item-chose-delete-btn");
            delete_btn.attr('id', id_list[i]);
            item_div_container.append(item_name);
            item_div_container.append(delete_btn);
            $('.items-chose-display-area').append(item_div_container);
        }
    });
    $(document).on('click', '.item-chose-delete-btn', function(){
        var id = $(this).attr('id'); //Lấy id của item đã chọn
        console.log(id)
        console.log($('#man-gender:checked'))
        $('#'+id).prop('checked', false);
        console.log($('#'+id).prop('checked'))
        $(this).closest('.item-chose').remove(); //Xóa item đã chọn
    });
});

