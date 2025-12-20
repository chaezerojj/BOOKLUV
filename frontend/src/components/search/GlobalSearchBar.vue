<template>
  <div class="global-search-bar">
    <form class="bar" @submit.prevent="onSubmit">
      <!-- ? 드롭다운 책/모임 카테고리 -->
      <SearchTypeSelect v-model="type" class="search-type-dropdown" />
      <input v-model="q" class="input" type="text" :placeholder="placeholder" />
      <button class="btn" type="submit">검색</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import SearchTypeSelect from './SearchTypeSelect.vue'

const props = defineProps({
  placeholder: { type: String, default: '검색어를 입력하세요...' },
  // 결과페이지에서 재사용 시 쿼리 동기화용(선택)
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
.global-search-bar {
  display: flex;
  text-align: center;
  align-items: center;
  margin: 0 auto;
}

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
