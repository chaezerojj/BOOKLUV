import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { http } from "@/api/http";

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null);
  const isLoading = ref(false);

  const isAuthenticated = computed(() => !!user.value);

  const fetchMe = async () => {
    isLoading.value = true;
    try {
      const res = await http.get("/api/auth/me/");
      user.value = res.data;
      return true;
    } catch (e) {
      user.value = null;
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  const logout = async () => {
    try {
      await http.post("/api/auth/logout/"); 
    } finally {
      user.value = null;
    }
  };

  const startKakaoLogin = () => {
    const clientId = import.meta.env.VITE_KAKAO_REST_API_KEY;
    const redirectUri = import.meta.env.VITE_KAKAO_REDIRECT_URI;

    const params = new URLSearchParams({
      response_type: "code",
      client_id: clientId,
      redirect_uri: redirectUri,
    });

    window.location.href = `https://kauth.kakao.com/oauth/authorize?${params.toString()}`;
  };

  return { user, isLoading, isAuthenticated, fetchMe, logout, startKakaoLogin };
});
