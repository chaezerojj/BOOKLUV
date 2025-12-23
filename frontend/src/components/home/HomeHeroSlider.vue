<template>
  <div class="hero-slider">
    <Swiper
      class="hero-swiper"
      :modules="modules"
      :loop="true"
      :autoplay="{ delay: 3500, disableOnInteraction: false }"
      :speed="650"
      @swiper="onSwiper"
    >
      <SwiperSlide v-for="slide in slides" :key="slide.id">
        <RouterLink :to="slide.to" class="slide-link" :aria-label="`책 상세로 이동: ${slide.bookId}`">
          <HomeHeroSlide :image-src="slide.imageSrc" :image-alt="slide.imageAlt" />
        </RouterLink>
      </SwiperSlide>
    </Swiper>

    <div class="nav">
      <button class="nav-btn" type="button" @click="prev" aria-label="이전 슬라이드"><</button>
      <button class="nav-btn" type="button" @click="next" aria-label="다음 슬라이드">></button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
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

import slide1 from "@/assets/images/slide1.png"
import slide2 from "@/assets/images/slide2.png"
import slide3 from "@/assets/images/slide3.png"
import slide4 from "@/assets/images/slide4.png"

const slides = [
  { id: 1, bookId: 14, imageSrc: slide1, imageAlt: "slide1" },
  { id: 2, bookId: 11, imageSrc: slide2, imageAlt: "slide2" },
  { id: 3, bookId: 25, imageSrc: slide3, imageAlt: "slide3" },
  { id: 4, bookId: 8, imageSrc: slide4, imageAlt: "slide4" },
].map((s) => ({
  ...s,
  to: { name: "book-detail", params: { id: String(s.bookId) } },
}))
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
