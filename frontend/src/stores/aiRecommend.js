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
      this.answers = {
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
      };
    },

    async submitQuiz() {
      this.loading = true;
      this.error = null;

      try {
        // 1. 헤더에서 Accept를 application/json으로 변경 (406 에러 해결 핵심)
        const res = await http.post(
          "/api/v1/recommendations/result/",
          this.answers,
          {
            headers: { Accept: "application/json" },
            // responseType: "text"는 삭제합니다. 기본값이 JSON입니다.
          }
        );

        // 2. 백엔드에서 보낸 JSON 데이터를 그대로 result에 할당
        // 백엔드가 { ai_reason: "...", books: [...] } 구조로 보내므로 바로 매핑됩니다.
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

// Helper: parse server-rendered HTML produced by Django `recommend/result.html`
// Returns { ai_reason, books: [{ id|null, cover_url, title, author_name, publisher, category_name, reason }] }
function parseRecommendationHtml(htmlString) {
  try {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlString, "text/html");

    // ai_reason: paragraph inside the top info box
    const aiReasonEl = doc.querySelector(
      '.container > div[style*="background"] p'
    );
    const ai_reason = aiReasonEl ? aiReasonEl.textContent.trim() : "";

    const books = [];
    // Each book block contains an <img> for the cover; use those images to locate book blocks
    const imgs = Array.from(doc.querySelectorAll(".container img"));

    imgs.forEach((img) => {
      // prefer a surrounding container that carries the book id
      const bookDiv = img.closest(".reco-book") || img.parentElement;
      const title = bookDiv.querySelector("h3")?.textContent?.trim() || "";
      const meta = bookDiv.querySelector("p")?.textContent || "";
      const [author_name = "", publisher = "", category_name = ""] = meta
        .split("|")
        .map((s) => s.trim());

      let reason = "";
      const reasonP = bookDiv.querySelector(
        'div[style*="background: #fdf6ec"] p'
      );
      if (reasonP) {
        reason = reasonP.textContent.replace("추천 포인트:", "").trim();
      }

      // try to read a numeric id from data-book-id if present
      let id = null;
      try {
        const idAttr =
          bookDiv.getAttribute && bookDiv.getAttribute("data-book-id");
        if (idAttr) {
          const n = Number(String(idAttr).trim());
          if (!Number.isNaN(n)) id = n;
        }
      } catch (e) {
        /* ignore */
      }

      books.push({
        id,
        cover_url: img.src || "",
        title,
        author_name,
        publisher,
        category_name,
        reason,
      });
    });

    return { ai_reason, books };
  } catch (e) {
    return { ai_reason: "", books: [] };
  }
}
