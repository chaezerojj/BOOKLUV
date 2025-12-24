import { defineStore } from "pinia";
import { http } from "@/api/http"; // axios 인스턴스

const normalizeBook = (b) => ({
  ...b,
  id: b?.id ?? b?.pk ?? b?.book_id ?? null,
});

// ✅ 추가: 모임(kluvTalk) 정규화
const normalizeTalk = (t) => {
  const id = t?.id ?? t?.pk ?? t?.meeting_id ?? null;

  const hostName =
    t?.host_name ??
    t?.leader_name ??
    t?.leader_nickname ??
    t?.leader?.nickname ??
    t?.leader?.name ??
    t?.leader_id?.nickname ??
    t?.leader_id?.name ??
    null;

  const categoryName =
    t?.category_name ??
    t?.category?.name ??
    t?.book?.category_name ??
    t?.book?.category?.name ??
    t?.book_id?.category_id?.name ??
    null;

  const bookTitle =
    t?.book_title ??
    t?.book?.title ??
    t?.book_id?.title ??
    null;

  return {
    ...t,
    id,
    title: t?.title ?? t?.name ?? t?.meeting_title ?? "(제목 없음)",
    host_name: hostName,
    category_name: categoryName,
    book_title: bookTitle,
    description: t?.description ?? t?.content ?? "",
  };
};

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
