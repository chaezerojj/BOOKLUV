<template>
  <div class="list">
    <RouterLink
      v-for="talk in kluvTalks"
      :key="talk.id"
      class="row"
      :to="{ name: 'kluvtalk-detail', params: { id: talk.id } }"
    >
      <div class="title">{{ talk.title }}</div>

      <div class="sub">
        <span v-if="talk.host_name">주최자: {{ talk.host_name }}</span>
        <span v-if="talk.category_name"> · 카테고리: {{ talk.category_name }}</span>
        <span v-if="talk.book_title"> · 책: {{ talk.book_title }}</span>
      </div>

      <div v-if="talk.description" class="desc">{{ talk.description }}</div>
    </RouterLink>
  </div>
</template>

<script setup>
defineProps({
  kluvTalks: { type: Array, default: () => [] },
})
</script>

<style scoped>
.list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.row {
  display: block;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 14px;
  background: #fff;
  text-decoration: none;
  color: inherit;
}
.row:hover {
  transform: translateY(-1px);
  box-shadow: 2px 2px 12px rgba(161, 161, 161, 0.18);
}
.title {
  font-size: 16px;
  font-weight: 700;
}
.sub {
  margin-top: 6px;
  font-size: 13px;
  color: #666;
}
.desc {
  margin-top: 10px;
  font-size: 14px;
  color: #777;
}
</style>
