
const decodeJson = (res) => res.json();

export const setAuthToken = (token) =>
    localStorage.setItem("authToken", token);

export const getAuthToken = () =>
    localStorage.getItem("authToken");

export const clearAuthToken = () =>
    localStorage.removeItem("authToken");
/**
 * Create HTTP request headers with json as
 * content type and access token read from local storage,
 * if present.
 */
const authorizedRequestHeaders = () => {
    let headers = {
        "Content-Type": "application/json",
    };

    const authToken = getAuthToken();
    if (authToken) {
        headers["Authorization"] = `Token ${authToken}`;
    }

    return headers;
};


export const get = (url) => fetch(url, {
    headers: authorizedRequestHeaders(),
}).then(decodeJson);


export const post = (url, data) => fetch(url, {
    headers: authorizedRequestHeaders(),
    method: "POST",
}).then(decodeJson);


