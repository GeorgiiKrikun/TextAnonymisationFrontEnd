let original_node = null;
document.addEventListener('DOMContentLoaded', function() {
    original_node = document.getElementsByClassName('file-upload-div')[0].cloneNode(true);    
});

let task_id_map = new BiMap();

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

async function anon_post_request(button) {
    elements = get_realated_elements(button);
    if (!elements.fileInput.files[0]) {
        alert("Please select a file first");
        return;
    }
    const headers = get_headers();
    elements.submit.disabled = true;
    elements.submit.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

    const file = elements.fileInput.files[0];
    const lang = elements.language.value;
    const task_type = get_anonymise_task(elements);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("lang", lang);
    formData.append("task_type", task_type);

    const response = await fetch(get_base_link() + 'tasks/', {
        method: 'POST',
        headers: headers,
        body: formData
    });

    const posted_task_response = await response.json();
    const ptr_id = posted_task_response.id;
    
    task_id_map.set(ptr_id, elements.div.id);
    append_new_input(elements.div);
    pollTaskStatus(ptr_id);
}

async function react_on_finished_task(task_id, file_id, filename) {
    const div_id = task_id_map.get(task_id);
    const div = document.getElementById(div_id);
    const elements = get_div_structure(div);
    const myHeaders = get_headers();

    const file_response = await fetch(get_base_link() + 'files/' + file_id + '/download/', 
        {method: 'GET', headers: myHeaders});
    
    const file_data = await file_response.arrayBuffer();
    const blob = new Blob([file_data], { type: 'application/octet-stream' });

    elements.download.href = URL.createObjectURL(blob);
    elements.download.download = filename;

    elements.download.style.display = elements.submit.style.display;
    elements.submit.style.display = "none";
}


async function pollTaskStatus(taskId, interval = 5000) {
    const myHeaders = get_headers();
    const poll = async () => {
        try {
            const response = await fetch(`${get_base_link()}tasks/${taskId}/`, {
                method: 'GET',
                headers: myHeaders
            });
            const result = await response.json();
            if (result.completed) {
                clearInterval(pollingInterval);
                const file_id = result.output_file.id;
                react_on_finished_task(taskId, file_id, result.output_file.name);
            } else {
                console.log(`Task ${taskId} still processing`);
            }
        } catch (error) {
            console.error('Error polling task status:', error);
        }
    };
    const pollingInterval = setInterval(poll, interval);
}
