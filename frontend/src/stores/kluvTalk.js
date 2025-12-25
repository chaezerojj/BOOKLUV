// src/stores/kluvTalk.js
import { defineStore } from "pinia";
import { http } from "@/api/http";

function toAbsoluteUrl(maybeUrl) {
  if (!maybeUrl) return null;
  const url = String(maybeUrl).trim();
  if (!url) return null;

  // 이미 절대 URL이면 그대로
  if (/^https?:\/\//i.test(url)) return url;

  if (/^\/\//.test(url)) return `https:${url}`;

  // /media/... 같은 상대경로면 백엔드 origin 붙이기
  // VITE_API_BASE_URL = https://bookluv-production.up.railway.app
  const apiBase = import.meta.env.VITE_API_BASE_URL;
  try {
    const u = new URL(apiBase);
    const origin = `${u.protocol}//${u.host}`;
    // url이 "/media/.." 형태면 origin + url
    if (url.startsWith("/")) return `${origin}${url}`;
    // "media/.." 형태면 origin + "/" + url
    return `${origin}/${url}`;
  } catch {
    return url;
  }
}

function pickFirst(...candidates) {
  for (const v of candidates) {
    if (v == null) continue;
    const s = String(v).trim();
    if (s) return v;
  }
  return null;
}

const normalizeMeeting = (m) => {
  const members =
    m?.members ??
    m?.member_count ??
    m?.participants_count ??
    m?.participants ??
    null;

  const maxMembers =
    m?.max_members ?? m?.capacity ?? m?.maxParticipants ?? null;

  const startAt =
    m?.started_at ??
    m?.start_at ??
    m?.start_time ??
    m?.meeting_start ??
    m?.scheduled_at ??
    null;

  // cover_url 후보를 최대한 넓게 (리스트/상세/중첩 구조 대응)
  const rawCover = pickFirst(
    m?.cover_url,
    m?.image_url,
    m?.cover,
    m?.thumbnail,
    m?.thumb_url,
    m?.book_cover_url,
    m?.book?.cover_url,
    m?.book?.cover,
    m?.book?.image_url,
    m?.book?.thumbnail,
    m?.book_detail?.cover_url,
    m?.book_info?.cover_url
  );

  const rawCategory = pickFirst(
    m?.category_name,
    m?.category?.name,
    m?.category
  );

  const rawBookTitle = pickFirst(
    m?.book_title,
    m?.book?.title,
    m?.book_detail?.title,
    m?.book_info?.title
  );

  return {
    ...m,
    id: m?.id ?? m?.pk ?? m?.meeting_id ?? null,
    title: m?.title ?? m?.name ?? "",
    views: Number(m?.views ?? 0),

    host_name: m?.host_name ?? m?.leader_name ?? m?.owner_name ?? null,
    category_name: rawCategory,
    book_title: rawBookTitle,
    description: m?.description ?? null,

    // ✅ 이미지 URL은 절대경로로 보정
    cover_url: toAbsoluteUrl(rawCover),

    members: members != null ? Number(members) : null,
    max_members: maxMembers != null ? Number(maxMembers) : null,
    started_at: startAt,
  };
};

const pickList = (data) => {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  return [];
};

export const useKluvTalkStore = defineStore("meeting", {
  state: () => ({
    // detail
    loading: false,
    error: null,
    meeting: null,

    // quiz
    quizLoading: false,
    quizError: null,
    quiz: null,
    quizResult: null,

    // popular list for home
    popularLoading: false,
    popularError: null,
    popularMeetings: [], // 홈: 조회수 TOP
  }),

  actions: {
    async fetchKluvTalk(meetingId) {
      this.loading = true;
      this.error = null;
      try {
        const res = await http.get(`/api/v1/books/meetings/${meetingId}/`);
        this.meeting = normalizeMeeting(res.data);
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

    /**
     * TOP4 가져오되,
     * - 리스트 API가 cover_url을 안 주는 경우가 많아서
     * - cover_url 없는 애들만 상세 API로 한 번 더 채움 (take=4라 부담 거의 없음)
     */
    async fetchPopularMeetings(take = 4) {
      this.popularLoading = true;
      this.popularError = null;

      try {
        const res = await http.get(`/api/v1/books/meetings/`, {
          params: {
            ordering: "-views",
            page_size: take,
            limit: take,
          },
          headers: { Accept: "application/json" },
        });

        const list = pickList(res.data).map(normalizeMeeting);
        list.sort((a, b) => (b.views ?? 0) - (a.views ?? 0));

        const top = list.slice(0, take);

        // cover_url 없는 것만 상세 조회로 보강
        const needFill = top.filter((m) => !m.cover_url && m.id != null);

        if (needFill.length > 0) {
          const results = await Promise.allSettled(
            needFill.map((m) => http.get(`/api/v1/books/meetings/${m.id}/`))
          );

          const coverMap = new Map(); // id -> cover_url
          results.forEach((r) => {
            if (r.status !== "fulfilled") return;
            const detail = normalizeMeeting(r.value.data);
            if (detail?.id != null && detail.cover_url) {
              coverMap.set(detail.id, detail.cover_url);
            }
          });

          // top 배열에 반영
          for (const m of top) {
            if (!m.cover_url && coverMap.has(m.id)) {
              m.cover_url = coverMap.get(m.id);
            }
          }
        }

        this.popularMeetings = top;
      } catch (err) {
        this.popularError = err;
        this.popularMeetings = [];
      } finally {
        this.popularLoading = false;
      }
    },
  },
});
