<template>
  <div class="home">
    <!-- 검색바 -->
    <section class="home__search">
      <GlobalSearchBar />
    </section>

    <!-- 검색 결과 패널(검색했을 때만) -->
    <section v-if="hasQuery" class="home__results">
      <SearchResultsPanel />
    </section>

    <div class="home-container">
      <!-- 큰 배너 -->
      <HomeHeroSection />
      <!-- 카드 2개 -->
      <HomeCardsSection />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import GlobalSearchBar from '@/components/search/GlobalSearchBar.vue'
import SearchResultsPanel from '@/components/search/results/SearchResultsPanel.vue'

import HomeCardsSection from '@/components/home/HomeCardsSection.vue'
import HomeHeroSection from '@/components/home/HomeHeroSection.vue'


const route = useRoute()
const hasQuery = computed(() => !!route.query.q && !!route.query.type)
</script>

<style scoped>
.home-container{
  margin: 1rem auto;
}

</style>