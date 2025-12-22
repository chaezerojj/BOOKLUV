<template>
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
</template>


<script setup>
defineProps({
  books: { type: Array, required: true },
})
</script>

<style scoped>
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
  height: 180px;
  object-fit: cover;
  border-radius: 10px;
}

.title {
  font-size: 16px;
  margin: 8px 0;
}

.meta {
  font-size: 12px;
  color: #666;
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