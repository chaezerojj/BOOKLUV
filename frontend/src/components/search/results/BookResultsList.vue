<template>
  <div class="grid">
    <template v-for="book in books" :key="getBookId(book) ?? book.title">
      <!-- id 있을 때만 RouterLink -->
      <RouterLink
        v-if="getBookId(book)"
        class="card"
        :to="{ name: 'book-detail', params: { id: getBookId(book) } }"
      >
        <img v-if="book.cover_url" :src="book.cover_url" class="cover" />
        <div class="body">
          <h3 class="title">{{ book.title }}</h3>
          <p class="meta">저자: {{ book.author_name ?? 'Unknown' }}</p>
          <p class="meta">카테고리: {{ book.category_name ?? 'Unknown' }}</p>
          <p class="desc">{{ book.description }}</p>
        </div>
      </RouterLink>

      <!-- id 없으면 링크 없이 카드만 -->
      <div v-else class="card disabled" title="상세로 이동할 수 없는 데이터(id 없음)">
        <div class="body">
          <h3 class="title">{{ book.title }}</h3>
          <p class="meta">저자: {{ book.author_name ?? 'Unknown' }}</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
defineProps({
  books: { type: Array, required: true },
});

const getBookId = (book) => {
  return book?.id ?? book?.pk ?? book?.book_id ?? null;
};
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