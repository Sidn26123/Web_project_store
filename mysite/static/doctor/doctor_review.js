$(document).ready(function(){
    var condition = "all";
    patient_info(condition);
    $('.condition-choose-box').click(function(){
        condition = $(this).attr('id');
        patient_info(condition);
    });
});