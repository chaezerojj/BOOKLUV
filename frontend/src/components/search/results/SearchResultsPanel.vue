<!-- SearchResultsPanel.vue -->
<template>
  <div class="panel">
    <div v-if="store.loading" class="info">검색 중...</div>

    <div v-else-if="store.error" class="info error">
      {{ store.error.message || '에러가 발생했어요.' }}
    </div>

    <SearchEmptyState
      v-else-if="items.length === 0"
      :q="q"
    />

    <BookResultsList
      v-else-if="type === 'book'"
      :books="items"
    />

    <KluvTalkResultsList
      v-else
      :kluvTalks="items"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSearchStore } from '@/stores/search'
import BookResultsList from './BookResultsList.vue'
import KluvTalkResultsList from './KluvTalkResultsList.vue'
import SearchEmptyState from './SearchEmptyState.vue'

const props = defineProps({
  type: { type: String, required: true },
  q: { type: String, required: true },
})

const store = useSearchStore()

const items = computed(() => {
  return props.type === 'book' ? store.books : store.kluvTalks
})
</script>
