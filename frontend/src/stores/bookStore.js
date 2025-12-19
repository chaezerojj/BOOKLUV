import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';

export const useBookStore = defineStore('bookStore', () => {
  const API_URL = 'http://localhost:8000/api/v1';  // Django 백엔드 API 기본 URL 설정
  
  const books = ref([]);  // 책 목록 상태
  const clubs = ref([]);  // 모임 목록 상태
  const searchQuery = ref('');  // 검색어 상태

  // 책 목록을 가져오는 액션
  const fetchBooks = async (searchType) => {
    try {
      const response = await axios.get(`${API_URL}/`, {
        params: {
          q: searchQuery.value,
          type: searchType,  // 선택된 카테고리 (책/모임)
        },
      });

      if (searchType === 'book') {
        books.value = response.data.books;  // 책 목록 저장
      } else if (searchType === 'club') {
        clubs.value = response.data.clubs;  // 모임 목록 저장
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // 검색어를 설정하는 액션
  const setSearchQuery = (query) => {
    searchQuery.value = query;
  };

  return {
    books,
    clubs,
    searchQuery,
    fetchBooks,
    setSearchQuery,
  };
}, { persist: true });
