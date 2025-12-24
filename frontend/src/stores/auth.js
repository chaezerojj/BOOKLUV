import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { http } from "@/api/http";

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null);
  const isLoading = ref(false);
  const isReady = ref(false); // 네비바 깜빡임 방지용(선택)

  const isAuthenticated = computed(() => !!user.value);

  // 세션 로그인 확인 (/me)
  const fetchMe = async () => {
    isLoading.value = true;
    try {
      const res = await http.get("/api/v1/auth/me/");
      user.value = res.data; // { email, kakao_id ... } 형태
      return true;
    } catch (e) {
      user.value = null;
      return false;
    } finally {
      isLoading.value = false;
      isReady.value = true;
    }
  };

  // 카카오 로그인 시작 (프론트에서 카카오 authorize로 보내는 역할)
  const startKakaoLogin = () => {
    const clientId = import.meta.env.VITE_KAKAO_REST_API_KEY;
    const redirectUri = import.meta.env.VITE_KAKAO_REDIRECT_URI; 
    // 여기 redirectUri는 "백엔드 callback" (예: http://localhost:8000/api/auth/callback/)
    console.log("BASE:", http.defaults.baseURL);

    const params = new URLSearchParams({
      response_type: "code",
      client_id: clientId,
      redirect_uri: redirectUri,
    });

    window.location.href = `https://kauth.kakao.com/oauth/authorize?${params.toString()}`;
  };

const logout = async () => {
  await http.post("/api/v1/auth/logout/");
  user.value = null;
  isReady.value = true;
};

// 회원정보수정
const updateProfile = async (payload) => {
  const res = await http.patch("/api/v1/auth/me/", payload);
  user.value = res.data;
  return res.data;
};

  return {
    user,
    isLoading,
    isReady,
    isAuthenticated,
    fetchMe,
    startKakaoLogin,
    logout,
    updateProfile,
  };
});
