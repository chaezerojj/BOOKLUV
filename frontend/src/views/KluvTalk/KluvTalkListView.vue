<template>
  <div class="page">
    <GlobalSearchBar />

    <section class="hero">
      <h2 class="headline">지금 인기있는 KluvTalk!</h2>
      <p class="sub">조회수가 높은 모임을 먼저 보여드려요 👀</p>

      <div v-if="store.listLoading" class="state">불러오는 중...</div>
      <div v-else-if="store.listError" class="state error">에러가 발생했어요.</div>

      <div v-else class="cards">
        <RouterLink
          v-for="m in store.popularMeetings"
          :key="m.id"
          class="card"
          :to="{ name: 'kluvtalk-detail', params: { id: m.id } }"
        >
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
              <span class="v">{{ m.leader_name ?? '-' }}</span>
            </div>
            <div class="line">
              <span class="k">참여</span>
              <span class="v">{{ m.joined_count ?? 0 }} / {{ m.members ?? '-' }}</span>
            </div>

            <p class="desc">{{ m.description || '설명이 없습니다.' }}</p>
          </div>
        </RouterLink>

        <div v-if="store.popularMeetings.length === 0" class="empty">
          아직 추천할 모임이 없어요.
        </div>
      </div>
    </section>

    <section class="cta">
      <RouterLink :to="{ name: 'kluvtalk-create' }" class="ctaLink">
        원하는 KluvTalk이 없나요? 지금 KluvTalk 만들러 가기 ➡️
      </RouterLink>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import GlobalSearchBar from "@/components/search/GlobalSearchBar.vue";
import { useKluvTalkStore } from "@/stores/kluvTalk";

const store = useKluvTalkStore();

onMounted(() => {
  store.fetchPopularMeetings(12); // 상위 12개
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

.cards {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

@media (max-width: 980px) {
  .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 620px) {
  .cards { grid-template-columns: 1fr; }
}

.card {
  text-decoration: none;
  color: inherit;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(0,0,0,0.03);
  display: flex;
  flex-direction: column;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 26px rgba(0,0,0,0.06);
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
.k { color: #777; }
.v { font-weight: 800; color: #222; }

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
  grid-column: 1 / -1;
  padding: 18px;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 14px;
  text-align: center;
  color: #777;
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
  box-shadow: 0 10px 26px rgba(0,0,0,0.05);
}
</style>
