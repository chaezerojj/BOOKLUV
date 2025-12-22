import { defineStore } from "pinia";
import { http } from "@/api/http";

export const useAiRecommendStore = defineStore("aiRecommend", {
  state: () => ({
    loading: false,
    error: null,

    // 퀴즈 답변(화면 이동해도 유지하려고 store에 둠)
    answers: {
      q1: "",
      q2: "",
      q3: "",
      q4: "",
      q5: "",
      q6: "",
      q7: "",
      q8: "",
      q9: "",
      q10: "",
    },

    // 결과(JSON)
    result: null, // { ai_reason, books: [...] }
  }),

  actions: {
    setAnswer(key, value) {
      this.answers[key] = value;
    },

    reset() {
      this.error = null;
      this.result = null;
      this.answers = { q1:"", q2:"", q3:"", q4:"", q5:"", q6:"", q7:"", q8:"", q9:"", q10:"" };
    },

    async submitQuiz() {
      this.loading = true;
      this.error = null;

      try {
        const res = await http.post("/api/v1/recommend/api/result/", this.answers);
        this.result = res.data;
        return res.data;
      } catch (err) {
        this.error = err;
        this.result = null;
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
});
