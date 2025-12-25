<template>
  <div class="cards">
    <RouterLink
      v-for="talk in kluvTalks"
      :key="talk.id"
      class="card"
      :to="{ name: 'kluvtalk-detail', params: { id: talk.id } }"
    >
      <div class="cardTop">
        <!-- 조회수 필드가 있다면 표시 (없으면 숨김) -->
        <div v-if="talk.views !== undefined && talk.views !== null" class="badge">
          👀 {{ talk.views ?? 0 }}
        </div>

        <div class="title">{{ talk.title }}</div>

        <div class="meta">
          <span v-if="talk.book_title">📚 {{ talk.book_title }}</span>
          <span v-if="talk.category_name"> · {{ talk.category_name }}</span>
        </div>
      </div>

      <div class="cardBottom">
        <div class="line">
          <span class="k">주최자</span>
          <span class="v">{{ talk.host_name ?? talk.leader_name ?? '-' }}</span>
        </div>

        <!-- 참여/정원 필드가 있다면 표시 (없으면 숨김) -->
        <div
          v-if="talk.joined_count !== undefined || talk.members !== undefined"
          class="line"
        >
          <span class="k">참여</span>
          <span class="v">{{ talk.joined_count ?? 0 }} / {{ talk.members ?? '-' }}</span>
        </div>

        <p class="desc">{{ talk.description || '설명이 없습니다.' }}</p>
      </div>
    </RouterLink>

    <div v-if="kluvTalks.length === 0" class="empty">
      검색 결과가 없어요.
    </div>
  </div>
</template>

<script setup>
defineProps({
  kluvTalks: { type: Array, default: () => [] },
})
</script>

<style scoped>
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
  transition: transform .15s ease, box-shadow .15s ease;
  margin-top: 2rem;
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
</style>
