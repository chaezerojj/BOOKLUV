// src/stores/kluvTalk.js
import { defineStore } from "pinia";
import { http } from "@/api/http";

export const useKluvTalkStore = defineStore("meeting", {
  state: () => ({
    loading: false,
    error: null,
    meeting: null,

    quizLoading: false,
    quizError: null,
    quiz: null,
    quizResult: null,
  }),

  actions: {
    async fetchKluvTalk(meetingId) {
      this.loading = true;
      this.error = null;
      try {
        // 모임 상세 API 경로를 "meetings/<id>" 쪽으로 맞춤
        const res = await http.get(`/api/v1/books/meetings/${meetingId}/`);
        this.meeting = res.data;
      } catch (err) {
        this.error = err;
        this.meeting = null;
      } finally {
        this.loading = false;
      }
    },

    async fetchQuiz(meetingId) {
      this.quizLoading = true;
      this.quizError = null;
      this.quizResult = null;
      try {
        // 퀴즈도 백엔드 실제 경로에 맞춰야 함
        const res = await http.get(`/api/v1/books/meetings/${meetingId}/quiz/`);
        this.quiz = res.data;
      } catch (err) {
        this.quizError = err;
        this.quiz = null;
      } finally {
        this.quizLoading = false;
      }
    },

    async submitQuiz(meetingId, answer) {
      this.quizLoading = true;
      this.quizError = null;
      try {
        const res = await http.post(`/api/v1/books/meetings/${meetingId}/quiz/`, { answer });
        this.quizResult = res.data;
      } catch (err) {
        this.quizError = err;
        this.quizResult = null;
      } finally {
        this.quizLoading = false;
      }
    },
  },
});
