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
import { computed, onMounted, defineAsyncComponent } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";

import GlobalSearchBar from "@/components/search/GlobalSearchBar.vue";
import HomeCardsSection from "@/components/home/HomeCardsSection.vue";
import HomeHeroSlider from "@/components/home/HomeHeroSlider.vue";

// 검색 결과 패널은 "검색했을 때만" 로드
const SearchResultsPanel = defineAsyncComponent(() =>
  import("@/components/search/results/SearchResultsPanel.vue")
);

const route = useRoute();
const hasQuery = computed(() => !!route.query.q && !!route.query.type);

const authStore = useAuthStore();

onMounted(() => {
  // store에 meLoaded 같은 플래그가 있으면 조건 걸어주기
  if (!authStore.me) authStore.fetchMe();
});
</script>

<style scoped>
.home-container{
  margin: 1rem auto;
}

</style>