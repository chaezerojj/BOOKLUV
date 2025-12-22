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
        <!-- ✅ 슬라이드 전체 클릭 -->
        <RouterLink :to="slide.to" class="slide-link">
          <HomeHeroSlide
            :image-src="slide.imageSrc"
            :image-alt="slide.imageAlt"
            :kicker="slide.kicker"
            :title="slide.title"
            :desc="slide.desc"
            :button-text="slide.buttonText"
          />
        </RouterLink>
      </SwiperSlide>
    </Swiper>

    <div class="nav">
      <button class="nav-btn" type="button" @click="prev" aria-label="이전">←</button>
      <button class="nav-btn" type="button" @click="next" aria-label="다음">→</button>
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

// swiper instance
const swiperRef = ref(null)
const onSwiper = (swiper) => (swiperRef.value = swiper)
const prev = () => swiperRef.value?.slidePrev()
const next = () => swiperRef.value?.slideNext()

const modules = [Autoplay]

// 이미지 import는 너 폴더에 맞게
import hero1 from "@/assets/images/book_and_cup.png"
import hero2 from "@/assets/images/book_and_cup.png"
import hero3 from "@/assets/images/book_and_cup.png"
import hero4 from "@/assets/images/book_and_cup.png"
import hero5 from "@/assets/images/book_and_cup.png"

const slides = [
  { id: 1, bookId: 1, imageSrc: hero1, imageAlt: "hero1", kicker: "🔥 인기", title: "지금 뜨는 책 1", desc: "설명 1", buttonText: "책 보러가기" },
  { id: 2, bookId: 2, imageSrc: hero2, imageAlt: "hero2", kicker: "✨ 추천", title: "지금 뜨는 책 2", desc: "설명 2", buttonText: "책 보러가기" },
  { id: 3, bookId: 3, imageSrc: hero3, imageAlt: "hero3", kicker: "📌 저장", title: "지금 뜨는 책 3", desc: "설명 3", buttonText: "책 보러가기" },
  { id: 4, bookId: 4, imageSrc: hero4, imageAlt: "hero4", kicker: "📚 신간", title: "지금 뜨는 책 4", desc: "설명 4", buttonText: "책 보러가기" },
  { id: 5, bookId: 5, imageSrc: hero5, imageAlt: "hero5", kicker: "💬 대화", title: "지금 뜨는 책 5", desc: "설명 5", buttonText: "책 보러가기" },
].map(s => ({
  ...s,
  // ✅ 네 라우터: /books/:id
  to: { name: "book-detail", params: { id: String(s.bookId) } },
}))
</script>

<style scoped>
.hero-slider { position: relative; }
.hero-swiper { width: 100%; }

.slide-link{
  border: 1px solid red;
  display:block;
  text-decoration:none;
  color: inherit;
}

.nav{
  position:absolute;
  right: 18px;
  bottom: 18px;
  display:flex;
  gap:10px;
  z-index:10;
}
.nav-btn{
  width:42px; height:42px;
  border-radius:999px;
  border:none;
  cursor:pointer;
  font-size:18px;
  background: rgba(255,255,255,0.85);
}
.nav-btn:active{ transform: scale(0.98); }
</style>
