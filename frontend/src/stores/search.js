import { defineStore } from 'pinia'
import axios from 'axios'

export const useSearchStore = defineStore('search', {
  state: () => ({
    loading: false,
    error: null,
    books: [],
    kluvTalks: [],
  }),

  actions: {
    async search({ type, q }) {
      const keyword = (q ?? '').trim()

      if (!keyword) {
        this.books = []
        this.kluvTalks = []
        this.error = null
        return
      }

      this.loading = true
      this.error = null

      try {
        const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

        if (type === 'book') {
          const res = await axios.get(`${API_URL}/api/v1/books/`, {
            params: { q: keyword },
          })
          // 무조건 배열이 옴 (Response(serializer.data))
          this.books = res.data
          this.kluvTalks = []
        } else {
          // 모임 구현안된 상태라 요청 막아둠
          this.kluvTalks = []
          this.books = []
          this.error = new Error('모임 검색은 아직 준비 중이에요.')
        }
      } catch (e) {
        this.error = e
        this.books = []
        this.kluvTalks = []
      } finally {
        this.loading = false
      }
    },
  },
})
