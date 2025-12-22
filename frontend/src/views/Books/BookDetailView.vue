<template>
  <div class="container">
    <div v-if="store.loading">로딩중...</div>
    <div v-else-if="store.error">에러가 발생했어요.</div>

    <div v-else-if="store.book" class="wrap">
      <div class="book">
        <img v-if="store.book.cover_url" :src="store.book.cover_url" class="cover" />
        <div class="info">
          <h1 class="title">{{ store.book.title }}</h1>
          <p>저자: {{ store.book.author_name ?? 'Unknown' }}</p>
          <p>카테고리: {{ store.book.category_name ?? 'Unknown' }}</p>
          <p>출판사: {{ store.book.publisher ?? '-' }}</p>
          <p class="desc">{{ store.book.description }}</p>
        </div>
      </div>

      <hr class="line" />

      <section class="meetings">
        <h2>이 책과 관련된 모임 ({{ store.meetings.length }})</h2>

        <div v-if="store.meetings.length === 0" class="empty">
          등록된 모임이 없습니다.
        </div>

        <ul v-else class="list">
          <li v-for="m in store.meetings" :key="m.id" class="item">
            <div>
              <div class="m-title">{{ m.title }}</div>
              <div class="m-meta">멤버 수: {{ m.members }} · 조회수: {{ m.views }}</div>
              <div class="m-desc">{{ m.description }}</div>
            </div>

            <RouterLink class="btn" :to="{ name: 'kluvtalk-detail', params: { id: m.id } }">
              자세히 보기
            </RouterLink>
          </li>
        </ul>
      </section>
    </div>
  </div>
</template>


<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useBookDetailStore } from '@/stores/bookDetail'

const route = useRoute()
const store = useBookDetailStore()

const load = async () => {
  const id = Number(route.params.id)
  if (!Number.isFinite(id)) return
  await store.fetchBookDetail(id)
}

onMounted(load)
watch(() => route.params.id, load)
</script>


<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px 16px;
}

.book {
  display: flex;
  gap: 16px;
}

.cover {
  width: 240px;
  height: 320px;
  object-fit: cover;
  border-radius: 12px;
  background: #eee;
}

.info {
  flex: 1;
}

.title {
  margin: 0 0 8px;
}

.desc {
  margin-top: 10px;
  color: #444;
  line-height: 1.6;
  white-space: pre-wrap;
}

.line {
  margin: 22px 0;
}

.list {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.item {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  background: #fff;
  padding: 14px;
  border-radius: 12px;
}

.btn {
  align-self: center;
  padding: 8px 12px;
  border-radius: 10px;
  background: #2d6cdf;
  color: #fff;
  text-decoration: none;
}

.m-title {
  font-weight: 700;
  margin-bottom: 6px;
}

.m-meta {
  font-size: 12px;
  color: #666;
  margin-bottom: 6px;
}

.m-desc {
  font-size: 13px;
  color: #444;
}

.empty {
  color: #777;
  padding: 12px 0;
}
</style>
