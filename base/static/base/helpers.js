function removeSpecialChars(id){
    let input = document.querySelector(`input#${id}`);
    let content_unformatted = input.value;
    let content_formatted = content_unformatted.normalize("NFD").replace(/[\u0300-\u036f]/g,"").toUpperCase();
    content_formatted = content_formatted.replace(/[^A-Z\s]/g,"");
    input.value = content_formatted;
}

function verifyMatch(matching_id,target_id,submit_id){
    let input_matching = document.querySelector(`input#${matching_id}`);
    let input_target = document.querySelector(`input#${target_id}`);
    let submit_button = document.querySelector(`button#submit_button`)
    if (input_matching.value != input_target.value){
        input_matching.className = "form-control border border-danger";
        submit_button.disabled = true;
    }else
    {
        input_matching.className = "form-control";
        submit_button.disabled = false;
    }
}