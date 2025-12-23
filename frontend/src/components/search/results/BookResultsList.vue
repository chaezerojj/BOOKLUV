<template>
  <div class="book-results-list">
    <div class="book-result-text">"{{ keyword }}" <span>에 대한 검색 결과입니다.</span></div>
    <div class="grid">
      <RouterLink v-for="book in books" :key="book.id" class="card"
        :to="{ name: 'book-detail', params: { id: book.id } }">
        <img v-if="book.cover_url" :src="book.cover_url" class="cover" />
        <div class="body">
          <h3 class="title">{{ book.title }}</h3>
          <p class="meta">저자: {{ book.author_name ?? 'Unknown' }}</p>
          <p class="meta">카테고리: {{ book.category_name ?? 'Unknown' }}</p>
          <p class="desc">{{ book.description }}</p>
        </div>
      </RouterLink>
    </div>
  </div>
</template>


<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

defineProps({
  books: { type: Array, required: true },
})

const route = useRoute()

const keyword = computed(() => {
  const q = route.query.q
  return (q ?? "").toString().trim()
})
</script>

<style scoped>
.book-results-list {
  margin: 2rem auto;
}

.book-result-text {
  margin: 2rem;
  font-weight: 700;
}

.book-result-text span {
  font-weight: 500;
}

.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.card {
  display: block;
  background: #fff;
  border-radius: 12px;
  padding: 12px;
  text-decoration: none;
  color: inherit;
}

.cover {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 10px;
}

.title {
  font-size: 16px;
  margin: 8px 0;
}

.meta {
  font-size: 12px;
  font-weight: 600;
  margin: 2px 0;
}

.desc {
  font-size: 12px;
  color: #444;
  margin-top: 6px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
</style>