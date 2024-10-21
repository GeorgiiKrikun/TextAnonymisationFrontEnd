function get_realated_elements(button) {
    const div = button.parentElement.parentElement;
    return get_div_structure(div);
}

function get_div_structure(div) {
    const fileInput = div.querySelector('#fileInput');
    const language = div.querySelector('#language');
    const checkbox = div.querySelector('#anonymise');
    const submit = div.querySelector('#submit');
    const download = div.querySelector('#download');
    return {
        div: div,
        fileInput: fileInput,
        language: language,
        checkbox: checkbox,
        submit: submit,
        download : download
    }
}

function get_anonymise_task(elements) {
    if (elements.checkbox.checked) {
        task = "ID";
    } else {
        task = "PR";        
    }
    return task;
}

function append_new_input(div) {
    new_element = original_node.cloneNode(true);
    structure = get_div_structure(new_element);
    structure.div.id = parseInt(div.id, 10) + 1;
    div.parentElement.appendChild(new_element);
}

function get_realated_elements(button) {
    const div = button.parentElement.parentElement;
    return get_data_structure(div);
}

function get_data_structure(div) {
    const filename = div.querySelector('#filename').textContent;
    const file_id = div.querySelector('#file_id').value;
    const downloadElement = div.querySelector('#download');
    return {
        filename: filename,
        file_id: file_id,
        downloadElement: downloadElement
    }
}

async function retrieve_file(button) {
    elements = get_realated_elements(button);
    const myHeaders = get_headers();
    console.log(elements.file_id);
    const file_response = await fetch(get_base_link() + 'files/' + elements.file_id + '/download/', 
    {method: 'GET', headers: myHeaders});

    const file_data = await file_response.arrayBuffer();
    const blob = new Blob([file_data], { type: 'application/octet-stream' });
    elements.downloadElement.href = URL.createObjectURL(blob);
    elements.downloadElement.download = elements.filename;
    elements.downloadElement.click();
}
