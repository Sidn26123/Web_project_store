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
    const patient_detail_nodes = document.querySelectorAll(".patient-thumbnail")
    patient_detail_nodes.forEach((node) =>{
        const patient_detail = document.querySelector(".patient-details");
        const overlay = document.querySelector(".overlay");
        node.addEventListener("click", ()=>{
            event.stopPropagation()
            patient_detail.classList.add("patient-details--visible");
            overlay.classList.add("overlay--visible");

        });
        //Nếu click ở overlay, ẩn đi 2 div
        overlay.addEventListener("click", ()=>{
            patient_detail.classList.remove("patient-details--visible");
            overlay.classList.remove("overlay--visible");
        });

    });

});
// document.querySelector(".patient-details").addEventListener('click', (event)=>{
//     event.stopPropagation();
// });
//stopPropagation chặn lại không thực hiện
if (document.querySelector(".patient-details")){
    document.querySelector(".patient-details").addEventListener('click', (event)=>{
        event.stopPropagation();
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
if (document.getElementById("search-submit-btn") != null){
    document.getElementById("search-submit-btn").addEventListener('click', function(event){
        event.preventDefault();
        let params = get_filter_params();
        let sorts = get_order_filter_params();
        let search_query = get_search_input();
        // var url = new URL(window.location.href) + "&" + params;
        //Nếu thêm dấu '/' ở đầu thì nó sẽ tự động lấy đây làm bắt đầu url, nếu khác thì nó sẽ thêm vào sau
        if (search_query !== ""){
            var url ='?' + params + "&"+ sorts + "&" + search_query;
        }
        else{
            var url ='?' + params + "&"+ sorts;
        }
        window.location.href = url;
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
$(document).on('click', '.search-filter__item', function(event) {
    event.preventDefault();
    
    var $checkbox = $(this).find('input[type="checkbox"]');
    if (!$checkbox.prop('checked')) {
        $(this).addClass('checkbox-custom-checked');
        $checkbox.prop('checked', true);
    } else {
        $(this).removeClass('checkbox-custom-checked');
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

