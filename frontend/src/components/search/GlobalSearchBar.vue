<template>
  <div class="container">
    <div>검색창 (전역)</div>
    <!-- SearchTypeSelect 컴포넌트를 삽입하여 카테고리 선택 -->
    <search-type-select @update-search-type="updateSearchType" />
    
    <div class="search-bar">
      <input 
        type="text" 
        v-model="query" 
        placeholder="검색어를 입력하세요..." 
        @keyup.enter="searchBooks"
      />
      <button @click="searchBooks">검색</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useBookStore } from '@/stores/bookStore.js';
import SearchTypeSelect from './SearchTypeSelect.vue';  // 드롭다운 컴포넌트 가져오기

const router = useRouter()

const query = ref('');  // 검색어
const searchType = ref('book');  // 'book' 또는 'club' (책/모임)

const bookStore = useBookStore();

// 검색창에서 검색을 실행하는 함수
const searchBooks = () => {
  bookStore.setSearchQuery(query.value);  // 검색어 설정
  bookStore.fetchBooks(searchType.value);  // 선택된 카테고리에 맞는 책 목록 갱신
  router.push({ name: 'search-result' });
};

// 검색 카테고리 타입을 업데이트하는 함수 (책/모임)
const updateSearchType = (type) => {
  searchType.value = type;
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.container div {
  border: 1px solid purple;
}

.search-bar {
  display: flex;
  align-items: center;
}
</style>
