<template>
  <div class="container">
    <!-- 결과 페이지에서도 검색바 유지 -->
    <GlobalSearchBar :syncWithRoute="true" />

    <SearchResultsPanel :type="type" :q="q" />
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSearchStore } from '@/stores/search'

import GlobalSearchBar from '@/components/search/GlobalSearchBar.vue'
import SearchResultsPanel from '@/components/search/results/SearchResultsPanel.vue'

const route = useRoute()
const store = useSearchStore()

const type = computed(() => (route.query.type === 'kluvtalk' ? 'kluvtalk' : 'book'))
const q = computed(() => (typeof route.query.q === 'string' ? route.query.q : ''))

watch(
  [type, q],
  async ([t, keyword]) => {
    await store.search({ type: t, q: keyword })
  },
  { immediate: true }
)

</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  /* padding: 30px 16px; */
}
.headline {
  margin-bottom: 14px;
}
</style>
