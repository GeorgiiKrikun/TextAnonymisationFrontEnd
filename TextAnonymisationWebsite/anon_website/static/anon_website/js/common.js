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

class BiMap {
    constructor() {
        this.forwardMap = new Map();
        this.reverseMap = new Map();
    }

    set(key, value) {
        if (this.forwardMap.has(key)) {
            const oldValue = this.forwardMap.get(key);
            this.reverseMap.delete(oldValue);
        }
        if (this.reverseMap.has(value)) {
            const oldKey = this.reverseMap.get(value);
            this.forwardMap.delete(oldKey);
        }
        this.forwardMap.set(key, value);
        this.reverseMap.set(value, key);
    }

    get(key) {
        return this.forwardMap.get(key);
    }

    getKey(value) {
        return this.reverseMap.get(value);
    }

    delete(key) {
        if (this.forwardMap.has(key)) {
            const value = this.forwardMap.get(key);
            this.forwardMap.delete(key);
            this.reverseMap.delete(value);
        }
    }

    deleteValue(value) {
        if (this.reverseMap.has(value)) {
            const key = this.reverseMap.get(value);
            this.reverseMap.delete(value);
            this.forwardMap.delete(key);
        }
    }

    has(key) {
        return this.forwardMap.has(key);
    }

    hasValue(value) {
        return this.reverseMap.has(value);
    }

    clear() {
        this.forwardMap.clear();
        this.reverseMap.clear();
    }
}