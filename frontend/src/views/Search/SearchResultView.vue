<template>
  <div>
    <h1>검색 결과</h1>
    <div v-if="searchType === 'book'">
      <BookResultsList :books="books" />
    </div>
    <div v-if="searchType === 'club'">
      <KluvTalkResultsList :clubs="clubs" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useBookStore } from '@/stores/bookStore.js';
import BookResultsList from '@/components/search/results/BookResultsList.vue';
import KluvTalkResultsList from '@/components/search/results/KluvTalkResultsList.vue';

const bookStore = useBookStore();

const books = computed(() => bookStore.books);
const clubs = computed(() => bookStore.clubs);
const searchType = computed(() => bookStore.searchType); // searchType을 store에서 가져옴
</script>

<style scoped>
  
</style>