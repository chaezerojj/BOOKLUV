<template>
  <section class="home-cards-section">
    <div class="section-head">
      <h2 class="section-title">🔥 지금 인기있는 KluvTalk</h2>
      <RouterLink class="more" :to="{ name: 'kluvtalk-list' }">전체 보기 →</RouterLink>
    </div>

    <div v-if="store.popularLoading" class="state">불러오는 중...</div>
    <div v-else-if="store.popularError" class="state error">인기 모임을 불러오지 못했어요.</div>

    <div v-else class="cards-row">
      <RouterLink
        v-for="m in store.popularMeetings"
        :key="m.id"
        class="card"
        :to="{ name: 'kluvtalk-detail', params: { id: m.id } }"
      >
        <div class="thumb">
          <img v-if="m.cover_url" :src="m.cover_url" alt="" />
          <div v-else class="thumb-fallback">KluvTalk</div>

          <!-- ✅ 카테고리 뱃지 -->
          <div v-if="m.category_name" class="badge">
            {{ m.category_name }}
          </div>
        </div>

        <div class="body">
          <div class="title">{{ m.title }}</div>

          <div v-if="m.book_title" class="book">📚 {{ m.book_title }}</div>

          <!-- ✅ 정보 라인(있을 때만) -->
          <div class="info">
            <span v-if="m.host_name" class="chip">👑 {{ m.host_name }}</span>
            <span v-if="m.started_at" class="chip">🕒 {{ fmtDateTime(m.started_at) }}</span>
            <span v-if="m.members != null" class="chip">
              👥 {{ m.members }}<template v-if="m.max_members != null"> / {{ m.max_members }}</template>
            </span>
          </div>

          <div class="footer">
            <span class="views">👀 {{ m.views }}</span>
            <span class="go">자세히 보기 →</span>
          </div>
        </div>
      </RouterLink>

      <div v-if="(store.popularMeetings?.length ?? 0) === 0" class="empty">
        아직 인기 모임이 없어요.
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from "vue";
import { RouterLink } from "vue-router";
import { useKluvTalkStore } from "@/stores/kluvTalk";

const store = useKluvTalkStore();

function fmtDateTime(value) {
  // ISO 문자열/Date 모두 대응
  try {
    const d = new Date(value);
    if (Number.isNaN(d.getTime())) return String(value);
    return d.toLocaleString("ko-KR", {
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return String(value);
  }
}

onMounted(async () => {
  await store.fetchPopularMeetings(4);
});
</script>

<style scoped>
.home-cards-section {
  width: min(1200px, calc(100% - 32px));
  margin: 18px auto 30px;
}

.section-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin: 6px 0 12px;
}

.section-title {
  margin: 0;
  font-size: 18px;
  font-weight: 900;
}

.more {
  text-decoration: none;
  color: #1a73e8;
  font-weight: 800;
}

.state {
  padding: 14px;
  border: 1px solid #eee;
  border-radius: 14px;
  background: #fff;
}
.state.error {
  background: #fff5f5;
  border-color: #ffd6d6;
  color: #b42318;
}

/* ✅ 4개 한 줄 */
.cards-row {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}
@media (max-width: 1100px) {
  .cards-row { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 640px) {
  .cards-row { grid-template-columns: 1fr; }
}

.card {
  text-decoration: none;
  color: inherit;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 22px rgba(0, 0, 0, 0.06);
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 2px 8px 18px rgba(0, 0, 0, 0.12);
}

.thumb {
  position: relative;
  width: 100%;
  height: 220px; 
  background: #fafafa;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 14px;
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 12px;
}

.thumb-fallback {
  font-size: 13px;
  font-weight: 900;
  color: #888;
}

/* ✅ 카테고리 뱃지 */
.badge {
  position: absolute;
  left: 10px;
  top: 10px;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.75);
  color: #fff;
  font-size: 12px;
  font-weight: 800;
  backdrop-filter: blur(4px);
}

.body {
  padding: 12px 12px 14px;
}

.title {
  font-size: 14px;
  font-weight: 900;
  line-height: 1.25;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.book {
  font-size: 12px;
  color: #444;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ✅ 칩(시간/인원/리더) */
.info {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 10px;
}
.chip {
  font-size: 11px;
  color: #444;
  background: #f6f7f9;
  border: 1px solid #eef0f3;
  padding: 5px 8px;
  border-radius: 999px;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: #777;
}
.views {
  font-weight: 900;
}
.go {
  color: #1a73e8;
  font-weight: 800;
}

.empty {
  grid-column: 1 / -1;
  padding: 12px;
  border: 1px dashed #ddd;
  border-radius: 12px;
  color: #888;
  text-align: center;
  font-size: 13px;
}
</style>
