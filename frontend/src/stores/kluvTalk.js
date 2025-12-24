import { defineStore } from "pinia";
import { http } from "@/api/http";

export const useKluvTalkStore = defineStore('meeting', {
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
      this.loading = true
      this.error = null
      try {
        const res = await http.get(`/api/v1/room/${meetingId}`)
        this.meeting = res.data
      } catch (err) {
        this.error = err
        this.meeting = null
      } finally {
        this.loading = false
      }
    },

    async fetchQuiz(meetingId) {
      this.quizLoading = true
      this.quizError = null
      this.quizResult = null
      try {
        const res = await http.get(`/api/v1/quiz/${meetingId}`)
        this.quiz = res.data
      } catch (err){
        this.quizError = err
        this.quiz = null
      } finally {
        this.quizLoading = false
      }
    },

    async submitQuiz(meetingId, answer) {
      this.quizLoading = true
      this.quizError = null
      try {
        const res = await http.post(`/api/v1/quiz/${meetingId}`, { answer })
        this.quizResult = res.data
      } catch (err) {
        this.quizError = err
        this.quizResult = null
      } finally {
        this.quizLoading = false
      }
    },
  },
})