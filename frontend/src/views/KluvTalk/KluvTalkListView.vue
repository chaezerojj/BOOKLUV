<template>
  <div class="page">
    <GlobalSearchBar />

    <section class="hero">
      <h2 class="headline">지금 인기있는 KluvTalk!</h2>
      <p class="sub">나에게 맞는 모임을 함께 찾아보아요 👀</p>

      <div class="controls">
        <label class="ctrl">
          정렬
          <select v-model="sortKey">
            <option value="latest">최신순</option>
            <option value="views">조회순</option>
          </select>
        </label>
      </div>

      <div v-if="store.listLoading" class="state">불러오는 중...</div>
      <div v-else-if="store.listError" class="state error">에러가 발생했어요.</div>

      <div v-else class="cardsWrap">
        <div class="cards">
          <RouterLink v-for="m in visibleMeetings" :key="m.id" class="card"
            :to="{ name: 'kluvtalk-detail', params: { id: m.id } }">
            <div class="cardTop">
              <div class="badge">👀 {{ m.views ?? 0 }}</div>
              <div class="title">{{ m.title }}</div>
              <div class="meta">
                <span v-if="m.book_title">📚 {{ m.book_title }}</span>
                <span v-if="m.category_name"> · {{ m.category_name }}</span>
              </div>
            </div>

            <div class="cardBottom">
              <div class="line">
                <span class="k">리더</span>
                <span class="v">{{ m.leader_name ?? m.host_name ?? '-' }}</span>
              </div>
              <div class="line">
                <span class="k">참여</span>
                <span class="v">{{ m.joined_count ?? 0 }} / {{ m.members ?? '-' }}</span>
              </div>

              <p class="desc">{{ m.description || '설명이 없습니다.' }}</p>
            </div>
          </RouterLink>
        </div>

        <div v-if="sortedMeetings.length === 0" class="empty">
          아직 추천할 모임이 없어요.
        </div>

        <div v-else class="moreBox">
          <div v-if="hasMore" class="moreHint">아래로 스크롤하면 더 나와요…</div>
          <div v-else class="moreHint end">마지막 모임까지 다 봤어요 🙂</div>
          <div ref="sentinel" class="sentinel"></div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, computed, watch } from "vue";
import GlobalSearchBar from "@/components/search/GlobalSearchBar.vue";
import { useKluvTalkStore } from "@/stores/kluvTalk";

const store = useKluvTalkStore();

const sortKey = ref("views"); // 기본: 조회순

const sortedMeetings = computed(() => {
  const list = [...(store.meetings ?? [])];

  if (sortKey.value === "views") {
    return list.sort((a, b) => (Number(b.views) || 0) - (Number(a.views) || 0));
  }

  // 최신순(모임 생성 최신순): created_at 있으면 그걸로, 없으면 id로 대체
  const getCreatedTime = (m) => {
    const raw = m.created_at;
    const t = raw ? new Date(raw).getTime() : NaN;
    if (Number.isFinite(t)) return t;
    return Number(m.id) || 0;
  };

  return list.sort((a, b) => getCreatedTime(b) - getCreatedTime(a));
});

// 무한 스크롤
const BATCH = 12;
const visibleCount = ref(BATCH);

const visibleMeetings = computed(() => sortedMeetings.value.slice(0, visibleCount.value));
const hasMore = computed(() => visibleCount.value < sortedMeetings.value.length);

function loadMore() {
  if (!hasMore.value) return;
  visibleCount.value = Math.min(visibleCount.value + BATCH, sortedMeetings.value.length);
}

watch(sortKey, () => {
  visibleCount.value = BATCH; // 정렬 바뀌면 처음부터 다시
});

// IntersectionObserver
const sentinel = ref(null);
let io = null;

function setupObserver() {
  if (!sentinel.value) return;
  if (io) io.disconnect();

  io = new IntersectionObserver(
    (entries) => {
      if (entries[0]?.isIntersecting) loadMore();
    },
    { root: null, rootMargin: "300px 0px", threshold: 0 }
  );

  io.observe(sentinel.value);
}

onMounted(async () => {
  await store.fetchMeetingsAll(); // ✅ 전체 가져오기
  setupObserver();
});

onBeforeUnmount(() => {
  if (io) io.disconnect();
});
</script>

<style scoped>
.page {
  width: 100%;
  padding-bottom: 40px;
}

.hero {
  max-width: 1100px;
  margin: 24px auto 0;
  padding: 0 16px;
}

.headline {
  margin: 18px 0 6px;
  font-size: 26px;
  font-weight: 900;
  letter-spacing: -0.02em;
  text-align: left;
}

.sub {
  margin: 0 0 18px;
  color: #666;
  text-align: left;
}

.controls {
  display: flex;
  justify-content: flex-end;
  margin: 0 0 12px;
}

.ctrl {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #666;
}

.ctrl select {
  border: 1px solid #e6e6e6;
  border-radius: 10px;
  padding: 8px 10px;
  background: #fff;
  font-weight: 800;
  color: #222;
}

.state {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 14px;
  padding: 14px;
}

.state.error {
  border-color: #ffd2d2;
  background: #fff7f7;
}

.cardsWrap {
  margin-top: 2.5rem;
}

.cards {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

@media (max-width: 980px) {
  .cards {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 620px) {
  .cards {
    grid-template-columns: 1fr;
  }
}

.card {
  text-decoration: none;
  color: inherit;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 26px rgba(0, 0, 0, 0.06);
}

.cardTop {
  padding: 14px 14px 10px;
  border-bottom: 1px solid #f3f3f3;
  background: linear-gradient(180deg, #fff7e0, #ffffff);
}

.badge {
  display: inline-block;
  font-size: 12px;
  font-weight: 900;
  padding: 6px 10px;
  border-radius: 999px;
  background: #fff2c2;
  border: 1px solid #ffe08a;
}

.title {
  margin-top: 10px;
  font-size: 16px;
  font-weight: 900;
  line-height: 1.35;
}

.meta {
  margin-top: 8px;
  font-size: 13px;
  color: #666;
}

.cardBottom {
  padding: 12px 14px 14px;
}

.line {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  margin-bottom: 6px;
}

.k {
  color: #777;
}

.v {
  font-weight: 800;
  color: #222;
}

.desc {
  margin: 10px 0 0;
  color: #666;
  font-size: 13px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.empty {
  padding: 18px;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 14px;
  text-align: center;
  color: #777;
}

.moreBox {
  margin-top: 18px;
  display: grid;
  gap: 10px;
  justify-items: center;
}

.moreHint {
  font-size: 12px;
  color: #888;
}

.moreHint.end {
  color: #777;
  font-weight: 900;
}

.sentinel {
  width: 100%;
  height: 1px;
}

.cta {
  max-width: 1100px;
  margin: 18px auto 0;
  padding: 0 16px;
}

.ctaLink {
  display: block;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 18px;
  padding: 18px;
  text-decoration: none;
  color: #1f2328;
  font-weight: 900;
  text-align: center;
}

.ctaLink:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 26px rgba(0, 0, 0, 0.05);
}
</style>
