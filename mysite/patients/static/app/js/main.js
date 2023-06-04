var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

$(document).ready(function(){
    var id = parseInt($(".get").data('id'));
    console.log(id)
    if (id > -1){
        var i = id.toString()
        $('#patient-name').val(12)
    }
    $("#book-submit").on('click', function(){
        var data = {
            'csrfmiddlewaretoken' : csrftoken,
            'form_data': $('#book-form').serialize(),
            'date_book': $('#date_book').val(),
            'doctor_id': 3,
            'patient_id': 21,
            'time_book': $(document).find('input[name="time"]:checked').val(),
        }
        console.log(data)
        $.ajax({
            type: 'POST',
            url: '/patient/book/',
            data: data,
            success: function(response){
                console.log(response)
                if (response['status'] == 'success'){
                    alert('Appointment booked successfully')
                }
                else{
                    alert('Appointment booking failed')
                }
            },
            failure: function(xhr, textStatus, errorThrown){
                alert('Appointment booking failed')
            }
        })
    });
});
document.getElementById("book-form").addEventListener("keydown", function(event) {
    if (event.keyCode === 13) { // Kiểm tra nếu phím Enter được nhấn
      event.preventDefault(); // Ngăn chặn hành động mặc định (submit form)
    }
});