import axios from "axios";

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  withCredentials: true,
});

http.interceptors.request.use((config) => {
  const method = (config.method || "get").toLowerCase();
  const unsafe = ["post", "put", "patch", "delete"].includes(method);

  if (unsafe) {
    const csrftoken = getCookie("csrftoken");
    if (csrftoken) {
      config.headers = config.headers || {};
      config.headers["X-CSRFToken"] = csrftoken;
    }
  }
  return config;
});
