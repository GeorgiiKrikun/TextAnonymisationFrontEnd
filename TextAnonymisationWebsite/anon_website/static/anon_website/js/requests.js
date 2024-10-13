async function send_get_request_tasts( )  {
    const myHeaders = new Headers(); 
    myHeaders.append("Authorization", "Token f5c40137f2af0d3b7462eb20a131f7526ad9e3f1");
    response = await fetch('http://127.0.0.1:8000/api/v1/tasks/', {method: 'GET', headers: myHeaders});
    console.log(response.json());
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function get_headers() {
    const headers = new Headers();
    headers.append("Authorization", "Token f5c40137f2af0d3b7462eb20a131f7526ad9e3f1");
    return headers;
}

async function try_post_request()  {
    const myHeaders = get_headers(); 
    console.log(myHeaders);

    const text = document.getElementById('comment').value;
    console.log(text);
    const blob = new Blob([text], { type: 'text/plain' });
    const file = new File([blob], "example.txt", { type: 'text/plain' });

    const lang = 0;
    const task_type = "PR";

    // Create FormData and append the file
    const formData = new FormData();
    formData.append("file", file);
    formData.append("lang", lang);
    formData.append("task_type", task_type);

    const response = await fetch('http://127.0.0.1:8000/api/v1/tasks/', {
        method: 'POST',
        headers: myHeaders,
        body: formData
    });

    const posted_task_response = await response.json();
    console.log(posted_task_response);
    const ptr_id = posted_task_response.id;
    console.log(ptr_id);
    get_task_result(ptr_id);
}

function set_comment(comment) {
    document.getElementById('comment').value = comment;
}

async function get_task_result(id) {
    const myHeaders = get_headers();
    while (true) { // poll until the task is completed      
        await sleep(5000); 
        const response = await fetch('http://127.0.0.1:8000/api/v1/tasks/' + id + '/', 
            {method: 'GET', headers: myHeaders});
        parsed_response = await response.json();
        if (parsed_response.completed) {
            file_id = parsed_response.output_file.id;
            const file_response = await fetch('http://127.0.0.1:8000/api/v1/files/' + file_id + '/download/', 
                {method: 'GET', headers: myHeaders});
            console.log(file_response);
            const file_data = await file_response.text();
            console.log(file_data);
            set_comment(file_data);
            break;
        }
    }
}
