// src/stores/search.js
import { defineStore } from "pinia";
import { http } from "@/api/http";

const normalizeBook = (b) => ({
  ...b,
  id: b?.id ?? b?.pk ?? b?.book_id ?? null,
});

const normalizeTalk = (t) => ({
  ...t,
  id: t?.id ?? t?.pk ?? t?.meeting_id ?? null,
  title: t?.title ?? "",
  host_name: t?.host_name ?? t?.leader_name ?? t?.leader?.nickname ?? t?.leader?.name ?? "",
  category_name: t?.category_name ?? t?.category ?? "",
  book_title: t?.book_title ?? t?.book?.title ?? "",
  description: t?.description ?? "",
  members: t?.members ?? t?.joined_count ?? 0,
  views: t?.views ?? 0,
  started_at: t?.started_at ?? null,
  finished_at: t?.finished_at ?? null,
});

const isProbablyHtmlString = (data) => {
  if (typeof data !== "string") return false;
  const s = data.trim().toLowerCase();
  return s.startsWith("<!doctype html") || s.startsWith("<html") || s.includes("<head");
};

export const useSearchStore = defineStore("search", {
  state: () => ({
    loading: false,
    error: null,
    books: [],
    kluvTalks: [],
  }),

  actions: {
    async search({ type, q }) {
      const keyword = (q ?? "").trim();

      if (!keyword) {
        this.books = [];
        this.kluvTalks = [];
        this.error = null;
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        if (type === "book") {
          const res = await http.get("/api/v1/books/", {
            params: { q: keyword },
            headers: { Accept: "application/json" },
          });

          if (isProbablyHtmlString(res.data)) {
            throw new Error("책 검색 API가 JSON이 아니라 HTML을 반환했어요. (백엔드 라우팅 확인 필요)");
          }

          const list = Array.isArray(res.data)
            ? res.data
            : Array.isArray(res.data?.results)
            ? res.data.results
            : [];

          this.books = list.map(normalizeBook);
          this.kluvTalks = [];
        } else if (type === "kluvtalk") {
          // ✅ 너 프로젝트에서 모임 검색이 이미 되는 endpoint로 맞춰서 사용
          const res = await http.get("/api/v1/books/meetings/", {
            params: { q: keyword },
            headers: { Accept: "application/json" },
          });

          if (isProbablyHtmlString(res.data)) {
            throw new Error("모임 검색 API가 JSON이 아니라 HTML을 반환했어요. (백엔드 라우팅 확인 필요)");
          }

          const list = Array.isArray(res.data)
            ? res.data
            : Array.isArray(res.data?.results)
            ? res.data.results
            : [];

          this.kluvTalks = list.map(normalizeTalk);
          this.books = [];
        } else {
          this.books = [];
          this.kluvTalks = [];
        }
      } catch (e) {
        this.error = e;
        this.books = [];
        this.kluvTalks = [];
      } finally {
        this.loading = false;
      }
    },
  },
});