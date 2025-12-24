import axios from "axios";

let csrfToken = null;

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}


export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  withCredentials: true,
});

//  CSRF 토큰을 백엔드에서 받아서 메모리에 저장
export async function ensureCsrfToken() {
  if (csrfToken) return csrfToken;
  const res = await http.get("/api/v1/auth/csrf/");
  csrfToken = res.data?.csrfToken;
  return csrfToken;
}

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

// axios.defaults.withCredentials = true