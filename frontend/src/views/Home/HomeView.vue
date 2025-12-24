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
      <HomeHeroSlider />
      <HomeCardsSection />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import GlobalSearchBar from '@/components/search/GlobalSearchBar.vue'
import SearchResultsPanel from '@/components/search/results/SearchResultsPanel.vue'

import HomeCardsSection from '@/components/home/HomeCardsSection.vue'
import HomeHeroSlider from '@/components/home/HomeHeroSlider.vue'


const route = useRoute()
const hasQuery = computed(() => !!route.query.q && !!route.query.type)

const authStore = useAuthStore()

onMounted(() => {
  authStore.fetchMe()
})
</script>

<style scoped>
.home-container{
  margin: 1rem auto;
}

</style>