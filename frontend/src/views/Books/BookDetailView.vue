<template>
  <GlobalSearchBar class="global-search" />
  <div class="book-detail">
    <div class="detail-container">
      <div v-if="store.loading">로딩중...</div>
      <div v-else-if="store.error">에러가 발생했어요.</div>

      <div v-else-if="store.book" class="wrap">
        <div class="book">
          <img v-if="store.book.cover_url" :src="store.book.cover_url" class="cover" />
          <div class="info">
            <h1 class="title">{{ store.book.title }}</h1>
            <p>{{ store.book.author_name ?? 'Unknown' }} 저자 |
              {{ store.book.publisher ?? '-' }} | {{ store.book.category_name ?? 'Unknown' }}</p>
            <p class="desc">{{ store.book.description }}</p>
          </div>
        </div>


        <section class="meetings">
          <hr class="line" />
          <h2>이 책과 관련된 모임 ({{ store.meetings.length }})</h2>

          <div v-if="store.meetings.length === 0" class="empty">
            등록된 모임이 없습니다.
          </div>

          <ul v-else class="list">
            <li v-for="m in store.meetings" :key="m.id" class="item">
              <div class="m-left">
                <div class="m-title">{{ m.title }}</div>
                <div class="m-meta">
                  <span class="meta-badge">👥 {{ m.members ?? '-' }}</span>
                  <span class="meta-badge">👁️ {{ m.views ?? 0 }}</span>
                </div>
                <div class="m-desc">{{ m.description }}</div>
              </div>

              <div class="m-right">
                <RouterLink class="btn small" :to="{ name: 'kluvtalk-detail', params: { id: m.id } }">
                  자세히 보기
                </RouterLink>
              </div>
            </li>
          </ul>

          <RouterLink :to="{ name: 'kluvtalk-create', query: { bookId: store.book.id } }"
            class="create-kluvtalk btn primary">
            이 책으로 모임 만들기
          </RouterLink>
        </section>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useBookDetailStore } from '@/stores/bookDetail'
import GlobalSearchBar from '@/components/search/GlobalSearchBar.vue'

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
.book-detail {
  margin: 0 auto;
  padding: 1rem;
  padding-top: 3rem;
}

.detail-container {
  background: #fff;
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 16px;
}

.book {
  display: flex;
  gap: 16px;
  width: 880px;
  padding: 3rem;
  padding-bottom: 1rem;
}

.cover {
  width: 240px;
  height: 320px;
  object-fit: cover;
  border-radius: 3px;
}

.info {
  margin: 1rem;
  flex: 1;
}

.info p {
  font-weight: 400;
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
  width: 1000px;
  justify-content: center;
  margin-bottom: 2rem;
}

.meetings {
  padding: 2.5rem;
}

.meetings h2 {
  padding-left: 0.5rem;
}

.meetings div {
  padding-left: 0.5rem;
}

.list {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.item {
  display: grid;
  grid-template-columns: 1fr 120px;
  gap: 16px;
  align-items: center;
  background: linear-gradient(180deg, #fff 0%, #fbfdff 100%);
  padding: 16px;
  border-radius: 14px;
  border: 1px solid #eef5ff;
  box-shadow: 0 6px 18px rgba(38, 86, 196, 0.04);
}

.m-left {
  min-width: 0;
}

.m-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.btn {
  align-self: center;
  padding: 10px 14px;
  border-radius: 10px;
  background: #2d6cdf;
  color: #fff;
  text-decoration: none;
  font-weight: 800;
  box-shadow: 0 4px 12px rgba(45, 108, 223, 0.12);
}

.btn.small {
  padding: 8px 12px;
  font-size: 13px;
}

.create-kluvtalk.btn.primary {
  display: inline-block;
  margin-top: 18px;
  padding: 12px 18px;
  border-radius: 12px;
  background: linear-gradient(90deg, #ffd86a, #ffb74d);
  color: #111;
  font-weight: 900;
  border: 1px solid rgba(0, 0, 0, 0.03);
}

.m-title {
  font-weight: 800;
  margin-bottom: 8px;
  font-size: 16px;
}

.m-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.meta-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #f4f8ff;
  color: #2754b6;
  padding: 6px 10px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 13px;
  border: 1px solid #e6f0ff;
}

.m-desc {
  font-size: 14px;
  color: #333;
  line-height: 1.5;
}

@media (max-width: 720px) {
  .item {
    grid-template-columns: 1fr;
  }

  .m-right {
    justify-content: flex-start;
  }

  .create-kluvtalk.btn.primary {
    width: 100%;
    text-align: center;
  }
}

.empty {
  color: #777;
  padding: 12px 0;
}
</style>
