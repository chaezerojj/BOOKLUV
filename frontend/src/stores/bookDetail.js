import { defineStore } from "pinia";
import http from '@/api/http';

export const useBookDetailStore = defineStore('bookDetail', {
  state: () => ({
    loading: false,
    error: null,
    book: null,
    meetings: [],
  }),
  actions: {
    async fetchBookDetail(bookId) {
      this.loading = true
      this.error = null
      try {
        const res = await http.get(`/api/v1/books/${bookId}`)
        this.book = res.data.book
        this.meetings = res.data.meetings
      } catch (err) {
        this.error = err
        this.book = null
        this.meetings = []
      } finally {
        this.loading = false
      }
    },
  },
})
