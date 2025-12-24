import { defineStore } from "pinia";
import { http } from "@/api/http";

export const useBookDetailStore = defineStore("bookDetail", {
  state: () => ({
    loading: false,
    error: null,
    book: null,
    meetings: [],
  }),

  actions: {
    async fetchBookDetail(bookId) {
      this.loading = true;
      this.error = null;

      try {
        // trailing slash
        const res = await http.get(`/api/v1/books/${bookId}/`);

        // 응답 형태가 2가지여도 대응
        const data = res.data;

        if (data && data.book) {
          this.book = data.book;
          this.meetings = data.meetings ?? [];
        } else {
          this.book = data;            // book 단일 객체로 오는 경우
          this.meetings = data?.meetings ?? [];
        }
      } catch (err) {
        this.error = err;
        this.book = null;
        this.meetings = [];
      } finally {
        this.loading = false;
      }
    },
  },
});
