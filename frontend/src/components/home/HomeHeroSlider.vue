<template>
  <div class="hero-slider">
    <!-- LCP 프리뷰(정적 첫 이미지) : CSS 건드리지 않고 inline style로만 오버레이 처리 -->
    <RouterLink
      :to="slides[0].to"
      class="slide-link"
      aria-hidden="true"
      tabindex="-1"
      style="
        display: block;
        width: 100%;
        height: 500px;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0px 0px 8px rgba(161, 161, 161, 0.25);
        pointer-events: none;
      "
    >
      <img
        :src="slides[0].imageSrc"
        alt=""
        loading="eager"
        fetchpriority="high"
        decoding="async"
        style="width: 100%; height: 100%; display: block; object-fit: cover;"
      />
    </RouterLink>

    <!-- Swiper는 첫 페인트 이후에 렌더(정적 프리뷰가 LCP 가져가게) -->
    <Swiper
      v-if="ready"
      class="hero-swiper"
      :modules="modules"
      :loop="true"
      :autoplay="{ delay: 3500, disableOnInteraction: false }"
      :speed="650"
      @swiper="onSwiper"
      style="position: absolute; left: 0; right: 0; top: 1.5rem;"
    >
      <SwiperSlide v-for="(slide, idx) in slides" :key="slide.id">
        <RouterLink
          :to="slide.to"
          class="slide-link"
          :aria-label="`책 상세로 이동: ${slide.bookId}`"
        >
          <HomeHeroSlide
            :image-src="slide.imageSrc"
            :image-alt="slide.imageAlt"
            :priority="idx === 0"
          />
        </RouterLink>
      </SwiperSlide>
    </Swiper>

    <div class="nav" v-if="ready">
      <button class="nav-btn" type="button" @click="prev" aria-label="이전 슬라이드"><</button>
      <button class="nav-btn" type="button" @click="next" aria-label="다음 슬라이드">></button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { RouterLink } from "vue-router"
import { Swiper, SwiperSlide } from "swiper/vue"
import { Autoplay } from "swiper/modules"
import "swiper/css"

import HomeHeroSlide from "./HomeHeroSlide.vue"

const swiperRef = ref(null)
const onSwiper = (swiper) => (swiperRef.value = swiper)
const prev = () => swiperRef.value?.slidePrev()
const next = () => swiperRef.value?.slideNext()

const modules = [Autoplay]

const slide1 = "/slide1.webp";
import slide2 from "@/assets/images/slide2.webp"
import slide3 from "@/assets/images/slide3.webp"
import slide4 from "@/assets/images/slide4.webp"


const slides = [
  { id: 1, bookId: 14, imageSrc: slide1, imageAlt: "slide1" },
  { id: 2, bookId: 11, imageSrc: slide2, imageAlt: "slide2" },
  { id: 3, bookId: 25, imageSrc: slide3, imageAlt: "slide3" },
  { id: 4, bookId: 8, imageSrc: slide4, imageAlt: "slide4" },
].map((s) => ({
  ...s,
  to: { name: "book-detail", params: { id: String(s.bookId) } },
}))

// ✅ 정적 프리뷰를 먼저 페인트하고, 다음 프레임에 Swiper 렌더
const ready = ref(false)
onMounted(() => {
  requestAnimationFrame(() => {
    ready.value = true
  })
})
</script>

<style scoped>
.hero-slider {
  position: relative;
  padding: 1.5rem 0;
}

.hero-swiper {
  width: 100%;
  border-radius: 20px;
  box-shadow: 0px 0px 8px rgba(161, 161, 161, 0.25);
}

/* RouterLink가 슬라이드 전체를 감싸도록 */
.slide-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

/* 우측 하단 버튼 */
.nav {
  position: absolute;
  right: 18px;
  bottom: 18px;
  display: flex;
  gap: 10px;
  z-index: 10;
  padding-bottom: 2rem;
  padding-right: 1rem;
}

.nav-btn {
  width: 42px;
  height: 42px;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  font-size: 18px;
  background: rgba(255, 255, 255, 0.85);
}

.nav-btn:active {
  transform: scale(0.98);
}
</style>
