// src/stores/kluvTalk.js
import { defineStore } from "pinia";
import { http } from "@/api/http";

function cleanUrl(v) {
  if (v == null) return null;
  const s = String(v).trim();
  if (!s) return null;
  if (s.toLowerCase() === "null" || s.toLowerCase() === "none") return null;
  return s;
}

function pickFirst(...candidates) {
  for (const c of candidates) {
    const v = cleanUrl(c);
    if (v) return v;
  }
  return null;
}

function toAbsoluteUrl(maybeUrl) {
  const url = cleanUrl(maybeUrl);
  if (!url) return null;

  if (/^https?:\/\//i.test(url)) return url;
  if (/^\/\//.test(url)) return `https:${url}`;

  const apiBase = import.meta.env.VITE_API_BASE_URL;
  try {
    const u = new URL(apiBase);
    const origin = `${u.protocol}//${u.host}`;
    if (url.startsWith("/")) return `${origin}${url}`;
    return `${origin}/${url}`;
  } catch {
    return url;
  }
}

const normalizeMeeting = (m) => {
  const members =
    m?.members ??
    m?.member_count ??
    m?.memberCount ??
    m?.participants_count ??
    m?.participantsCount ??
    m?.participants ??
    null;

  const maxMembers =
    m?.max_members ??
    m?.maxMembers ??
    m?.capacity ??
    m?.maxParticipants ??
    null;

  const startAt =
    m?.started_at ??
    m?.startedAt ??
    m?.start_at ??
    m?.startAt ??
    m?.start_time ??
    m?.startTime ??
    m?.meeting_start ??
    m?.meetingStart ??
    m?.scheduled_at ??
    m?.scheduledAt ??
    null;

  // cover 후보(※ 백에서 안 내려오면 결국 null)
  const rawCover = pickFirst(
    m?.cover_url,
    m?.coverUrl,
    m?.image_url,
    m?.imageUrl,
    m?.thumbnail,
    m?.thumb_url,
    m?.thumbUrl,
    m?.book_cover_url,
    m?.bookCoverUrl,
    m?.book?.cover_url,
    m?.book?.coverUrl
  );

  const rawCategory = pickFirst(
    m?.category_name,
    m?.categoryName,
    m?.category?.name,
    m?.category
  );

  const rawBookTitle = pickFirst(
    m?.book_title,
    m?.bookTitle,
    m?.book?.title
  );

  return {
    ...m,
    id: m?.id ?? m?.pk ?? m?.meeting_id ?? m?.meetingId ?? null,
    title: m?.title ?? m?.name ?? "",
    views: Number(m?.views ?? m?.view_count ?? m?.viewCount ?? 0),

    // ✅ leader_name / host_name 둘 다 대응
    leader_name:
      m?.leader_name ?? m?.leaderName ?? m?.host_name ?? m?.hostName ?? null,
    host_name:
      m?.host_name ?? m?.hostName ?? m?.leader_name ?? m?.leaderName ?? null,

    category_name: rawCategory,
    book_title: rawBookTitle,
    description: m?.description ?? null,

    cover_url: toAbsoluteUrl(rawCover),

    members: members != null ? Number(members) : null,
    max_members: maxMembers != null ? Number(maxMembers) : null,
    started_at: startAt,

    // ✅ 최신순 정렬용 (백이 created_at을 안주면 id로 대체)
    created_at: m?.created_at ?? m?.createdAt ?? null,
  };
};

const pickList = (data) => {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  return [];
};

export const useKluvTalkStore = defineStore("meeting", {
  state: () => ({
    loading: false,
    error: null,
    meeting: null,

    quizLoading: false,
    quizError: null,
    quiz: null,
    quizResult: null,

    // ✅ 리스트(전체)용
    listLoading: false,
    listError: null,
    meetings: [],

    // ✅ 인기(top N)용
    popularLoading: false,
    popularError: null,
    popularMeetings: [],
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
        const res = await http.post(`/api/v1/books/meetings/${meetingId}/quiz/`, {
          answer,
        });
        this.quizResult = res.data;
      } catch (err) {
        this.quizError = err;
        this.quizResult = null;
      } finally {
        this.quizLoading = false;
      }
    },

    /**
     * ✅ 리스트 페이지용: "전체" 받아오기
     * - 백 meeting_list_api는 limit 없으면 전부 내려줌(현재 코드 기준)
     * - 정렬은 프론트에서 할 거라서 여기서는 그냥 가져와서 normalize만
     */
    async fetchMeetingsAll() {
      this.listLoading = true;
      this.listError = null;
      try {
        const res = await http.get(`/api/v1/books/meetings/`, {
          headers: { Accept: "application/json" },
        });
        this.meetings = pickList(res.data).map(normalizeMeeting);
      } catch (err) {
        this.listError = err;
        this.meetings = [];
      } finally {
        this.listLoading = false;
      }
    },

    /**
     * ✅ 홈/상단 섹션용: TOP N만
     * ⚠️ 기존 cover 보강(detail 폭탄) 로직 제거 (500 원인 + 어차피 cover 안 내려옴)
     */
    async fetchPopularMeetings(take = 12) {
      this.popularLoading = true;
      this.popularError = null;

      try {
        const res = await http.get(`/api/v1/books/meetings/`, {
          params: { limit: take, sort: "views" }, // ✅ 백이 받는 파라미터에 맞춤
          headers: { Accept: "application/json" },
        });

        const list = pickList(res.data).map(normalizeMeeting);
        list.sort((a, b) => (b.views ?? 0) - (a.views ?? 0));

        this.popularMeetings = list.slice(0, take);
      } catch (err) {
        this.popularError = err;
        this.popularMeetings = [];
      } finally {
        this.popularLoading = false;
      }
    },
  },
});
