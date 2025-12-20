<template>
  <form class="bar" @submit.prevent="onSubmit">
    <SearchTypeSelect v-model="type" />

    <input
      v-model="q"
      class="input"
      type="text"
      :placeholder="placeholder"
    />

    <button class="btn" type="submit">검색</button>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import SearchTypeSelect from './SearchTypeSelect.vue'

const props = defineProps({
  placeholder: { type: String, default: '검색어를 입력하세요...' },
  // ✅ 결과페이지에서 재사용 시 쿼리 동기화용(선택)
  syncWithRoute: { type: Boolean, default: false },
})

const router = useRouter()
const route = useRoute()

const type = ref('book')
const q = ref('')

// 결과 페이지에서 검색바도 같이 쓰고 싶으면 syncWithRoute=true로 사용
watch(
  () => route.query,
  (query) => {
    if (!props.syncWithRoute) return
    type.value = (query.type === 'kluvtalk' ? 'kluvtalk' : 'book')
    q.value = typeof query.q === 'string' ? query.q : ''
  },
  { immediate: true }
)

const onSubmit = () => {
  const keyword = q.value.trim()
  router.push({
    name: 'search',
    query: {
      type: type.value,
      q: keyword,
    },
  })
}
</script>

<style scoped>
.bar {
  display: flex;
  gap: 10px;
  align-items: center;
  width: 500px;
}

.input {
  flex: 1;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.btn {
  height: 40px;
  padding: 0 14px;
  border: none;
  border-radius: 8px;
  background: #0d6efd;
  color: white;
  cursor: pointer;
}
</style>
