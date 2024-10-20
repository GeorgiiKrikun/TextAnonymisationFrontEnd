function get_base_link() {
    return "http://127.0.0.1:8000/api/v1/";
}


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function stripSpaces(str) {
    return str.replace(/[\s\n\t]+/g, '');
}

function get_headers() {
    const headers = new Headers();
    token_element = document.getElementById('token');
    headers.append("Authorization", "Token " + stripSpaces(token_element.textContent));
    return headers;
}
