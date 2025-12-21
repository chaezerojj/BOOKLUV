<template>
  <div class="list">
    <div v-for="talk in kluvTalks" :key="talk.id" class="row">
      <div class="title">{{ talk.title }}</div>
      <div class="sub">
        <span v-if="talk.host_name">주최자: {{ talk.host_name }}</span>
        <span v-if="talk.category_name"> · 카테고리: {{ talk.category_name }}</span>
      </div>
      <div v-if="talk.description" class="desc">{{ talk.description }}</div>
    </div>
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
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 14px;
  background: #fff;
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
