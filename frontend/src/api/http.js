import axios from "axios";

let csrfToken = null;


export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
});

// CSRF 토큰을 백엔드에서 받아서 메모리에 저장
export async function ensureCsrfToken(force = false) {
  if (csrfToken && !force) return csrfToken;

  const res = await http.get("/api/v1/auth/csrf/"); // 너가 만든 csrf 엔드포인트
  csrfToken = res.data?.csrfToken;
  return csrfToken;
}

http.interceptors.request.use(async (config) => {
  const method = (config.method || "get").toLowerCase();
  const unsafe = ["post", "put", "patch", "delete"].includes(method);

  if (unsafe) {
    const token = await ensureCsrfToken();
    if (token) {
      config.headers = config.headers || {};
      config.headers["X-CSRFToken"] = token;
    }
  }
  return config;
});

// axios.defaults.withCredentials = true