<template>
  <div class="wrap">
    <div v-if="store.loading" class="state">로딩중...</div>
    <div v-else-if="store.error" class="state error">에러가 발생했어요.</div>

    <div v-else-if="store.meeting" class="card">
      <!-- ✅ 상단: 표지 + 헤더/메타 -->
      <div class="top">
        <div class="coverBox">
          <img
            v-if="coverSrc"
            :src="coverSrc"
            class="cover"
            alt="book cover"
            loading="lazy"
          />
          <div v-else class="coverFallback">No Cover</div>
        </div>

        <div class="head">
          <h1 class="title">{{ store.meeting.title }}</h1>
          <div class="meta">
            <span v-if="store.meeting.book_title">📚 {{ store.meeting.book_title }}</span>
            <span v-if="store.meeting.category_name"> · {{ store.meeting.category_name }}</span>
          </div>

          <!-- ✅ 정보 그리드(조금 더 컴팩트하게) -->
          <div class="grid">
            <div class="item">
              <div class="label">리더</div>
              <div class="value">{{ store.meeting.leader_name ?? '-' }}</div>
            </div>

            <div class="item">
              <div class="label">조회수</div>
              <div class="value">{{ store.meeting.views ?? 0 }}</div>
            </div>

            <div class="item">
              <div class="label">참여</div>
              <div class="value">
                {{ store.meeting.joined_count ?? 0 }} / {{ store.meeting.members ?? '-' }}
              </div>
            </div>

            <div class="item">
              <div class="label">시간</div>
              <div class="value">
                <span v-if="store.meeting.started_at">
                  {{ formatTime(store.meeting.started_at) }}
                </span>
                <span v-if="store.meeting.finished_at">
                  ~ {{ formatTime(store.meeting.finished_at) }}
                </span>
                <span v-if="!store.meeting.started_at">-</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ✅ 설명: 기본 높이 넉넉하게 -->
      <div class="descBox">
        <div class="label">설명</div>
        <p class="desc">
          {{ store.meeting.description || '설명이 없습니다.' }}
        </p>
      </div>

      <div class="actions">
        <RouterLink class="btn primary" :to="{ name: 'kluvtalk-quiz', params: { id: meetingId } }">
          퀴즈 풀고 참여하기
        </RouterLink>
        <RouterLink class="btn" :to="{ name: 'kluvtalk-list' }">
          목록으로
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useKluvTalkStore } from "@/stores/kluvTalk";

const route = useRoute();
const store = useKluvTalkStore();

const meetingId = computed(() => Number(route.params.id));

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

const coverSrc = computed(() => {
  const m = store.meeting;
  if (!m) return "";

  const raw = m.cover_url || m.book_cover_url || m.book_cover || m.book?.cover_url || "";
  if (!raw) return "";

  // 이미 절대 URL이면 그대로
  if (/^https?:\/\//i.test(raw)) return raw;

  // 상대경로면 백엔드 주소 붙이기
  return `${API_BASE}${raw.startsWith("/") ? "" : "/"}${raw}`;
});

const load = async () => {
  if (!Number.isFinite(meetingId.value)) return;
  await store.fetchKluvTalk(meetingId.value);
};

onMounted(load);
watch(() => route.params.id, load);

function formatTime(iso) {
  try {
    const d = new Date(iso);
    return d.toLocaleString([], {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return iso;
  }
}
</script>

<style scoped>
.wrap {
  max-width: 920px;
  margin: 0 auto;
  padding: 28px 16px;
}

.state {
  padding: 18px;
  background: #fff;
  border-radius: 14px;
  border: 1px solid #eee;
}
.state.error {
  border-color: #ffdddd;
  background: #fff7f7;
}

.card {
  background: #fff;
  border-radius: 18px;
  border: 1px solid #eee;
  padding: 22px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.04);
}

/* ✅ 표지 + 헤더 영역 */
.top {
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 18px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f1f1f1;
  margin-bottom: 16px;
}

@media (max-width: 720px) {
  .top {
    grid-template-columns: 1fr;
  }
  .coverBox {
    width: 180px;
    margin: 0 auto;
  }
}

.coverBox {
  width: 160px;
}

.cover {
  width: 100%;
  aspect-ratio: 3 / 4;
  object-fit: cover;
  border-radius: 14px;
  border: 1px solid #eee;
  background: #fafafa;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

.coverFallback {
  width: 100%;
  aspect-ratio: 3 / 4;
  border-radius: 14px;
  border: 1px dashed #ddd;
  background: #fafafa;
  display: grid;
  place-items: center;
  color: #999;
  font-weight: 800;
  font-size: 12px;
}

.head {
  min-width: 0;
}

.title {
  margin: 0;
  font-size: 26px;
  font-weight: 900;
  letter-spacing: -0.02em;
}

.meta {
  margin-top: 8px;
  color: #666;
  font-size: 14px;
}

/* ✅ 정보칸: 조금 줄이기 */
.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin: 14px 0 0;
}

.item {
  border: 1px solid #f1f1f1;
  border-radius: 12px;
  padding: 10px 12px; /* 기존보다 축소 */
  /* background: #fcfcfc; */
}

.label {
  font-size: 11px; /* 기존 12px -> 11px */
  color: #888;
  margin-bottom: 4px; /* 기존 6px -> 4px */
}

.value {
  font-size: 14px; /* 기존 15px -> 14px */
  font-weight: 800;
  color: #222;
}

/* ✅ 설명: 기본 높이 넉넉하게 */
.descBox {
  border: 1px solid #f1f1f1;
  border-radius: 14px;
  padding: 14px;
  background: #fffdf6;
  min-height: 160px; /* 👈 기본 높이 */
}

.desc {
  margin: 8px 0 0;
  line-height: 1.7;
  color: #333;
  white-space: pre-line; /* 줄바꿈 텍스트도 보기 좋게 */
}

.actions {
  margin-top: 18px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  display: inline-block;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid #e6e6e6;
  background: #fff;
  text-decoration: none;
  color: inherit;
  font-weight: 800;
  transition: transform .15s ease, box-shadow .15s ease;
}

.btn.primary {
  border-color: #ffe08a;
  background: #fff2c2;
}
.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}
</style>
