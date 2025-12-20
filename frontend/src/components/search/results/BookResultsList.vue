<template>
  <div class="grid">
    <div v-for="book in books" :key="book.id" class="card">
      <img v-if="book.cover_url" class="cover" :src="book.cover_url" :alt="book.title" />

      <div class="body">
        <h5 class="title">{{ book.title }}</h5>
        <p class="meta"><b>Author:</b> {{ book.author_name || 'Unknown' }}</p>
        <p class="meta"><b>Category:</b> {{ book.category_name || 'Unknown' }}</p>
        <p class="desc">{{ book.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  books: { type: Array, default: () => [] },
})
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 16px;
}

@media (max-width: 1200px) {
  .grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (max-width: 768px) {
  .grid { grid-template-columns: repeat(1, minmax(0, 1fr)); }
}

.card {
  border: 1px solid #eee;
  border-radius: 12px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,.06);
}

.cover {
  width: 100%;
  height: 220px;
  object-fit: cover;
  background: #f7f7f7;
}

.body {
  padding: 12px;
}

.title {
  margin: 0 0 8px;
  font-size: 16px;
}

.meta {
  margin: 2px 0;
  font-size: 14px;
}

.desc {
  margin-top: 8px;
  font-size: 13px;
  color: #777;

  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
