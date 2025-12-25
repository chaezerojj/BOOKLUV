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
        // POST to backend recommendations endpoint which returns server-rendered HTML
        // Use API path under /api/v1 so it hits the Django view included at api/v1/recommendations/
        const res = await http.post(
          "/api/v1/recommendations/result/",
          this.answers,
          { headers: { Accept: "text/html" }, responseType: "text" }
        );

        const html = res.data;
        const parsed = parseRecommendationHtml(html);
        this.result = parsed;
        return parsed;
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
      const bookDiv = img.parentElement;
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

      books.push({
        id: null,
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
