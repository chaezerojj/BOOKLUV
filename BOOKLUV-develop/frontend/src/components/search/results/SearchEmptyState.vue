<template>
  <div class="empty">
    <p class="muted">검색 결과가 없습니다.</p>
    <p v-if="q" class="hint">검색어: "{{ q }}"</p>
  </div>
</template>

<script setup>
defineProps({
  q: { type: String, default: '' },
})
</script>

<style scoped>
.empty {
  text-align: center;
  padding: 50px 0;
}
.muted {
  color: #888;
}
.hint {
  color: #aaa;
  margin-top: 6px;
  font-size: 14px;
}
</style>
