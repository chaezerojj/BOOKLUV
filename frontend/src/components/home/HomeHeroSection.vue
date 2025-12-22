<template>
  <div class="hero-slider">
    <Swiper
      class="hero-swiper"
      :modules="modules"
      :loop="true"
      :autoplay="{
        delay: 3500,
        disableOnInteraction: false
      }"
      :speed="650"
      @swiper="onSwiper"
    >
      <SwiperSlide v-for="slide in slides" :key="slide.id">
        <HomeHeroSlide
          :image-src="slide.imageSrc"
          :image-alt="slide.imageAlt"
          :title="slide.title"
          :to="slide.to"
          :button-text="slide.buttonText"
        />
      </SwiperSlide>
    </Swiper>

    <!-- 오른쪽 아래 커스텀 버튼 -->
    <div class="nav">
      <button class="nav-btn" type="button" @click="prev">←</button>
      <button class="nav-btn" type="button" @click="next">→</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"

// Swiper
import { Swiper, SwiperSlide } from "swiper/vue"
import { Autoplay } from "swiper/modules"
import "swiper/css"

// Slide UI 컴포넌트
import HomeHeroSlide from "./HomeHeroSlide.vue"

// Swiper 인스턴스 잡기
const swiperRef = ref(null)
const onSwiper = (swiper) => {
  swiperRef.value = swiper
}

const prev = () => swiperRef.value?.slidePrev()
const next = () => swiperRef.value?.slideNext()

const modules = [Autoplay]

// ✅ 5개 슬라이드 데이터
// 이미지 경로는 지금처럼 assets를 쓰면 import로 안전하게 가져오는 걸 추천!
import bookAndCup from "@/assets/images/book_and_cup.png"
// 아래는 예시: 나머지 4개 이미지도 만들어서 import 하세요
import hero2 from "@/assets/images/hero2.png"
import hero3 from "@/assets/images/hero3.png"
import hero4 from "@/assets/images/hero4.png"
import hero5 from "@/assets/images/hero5.png"

const slides = [
  {
    id: 1,
    imageSrc: bookAndCup,
    imageAlt: "book-and-cup-img",
    title: "지금 유저들은 어떤 책으로 대화를 나누고 있을까요?",
    to: { name: "kluvtalk-list" },
    buttonText: "알아보러가기",
  },
  {
    id: 2,
    imageSrc: hero2,
    imageAlt: "hero2",
    title: "오늘의 추천 모임을 확인해보세요!",
    to: { name: "meeting-list" }, // 네 라우트명에 맞게 수정
    buttonText: "보러가기",
  },
  {
    id: 3,
    imageSrc: hero3,
    imageAlt: "hero3",
    title: "AI 테스트로 취향에 맞는 책을 찾아봐요",
    to: { name: "ai-test" },
    buttonText: "테스트하기",
  },
  {
    id: 4,
    imageSrc: hero4,
    imageAlt: "hero4",
    title: "지금 인기있는 책 TOP을 확인해요",
    to: { name: "book-list" },
    buttonText: "확인하기",
  },
  {
    id: 5,
    imageSrc: hero5,
    imageAlt: "hero5",
    title: "새로운 대화를 만들고 사람들을 만나보세요",
    to: { name: "board-list" },
    buttonText: "둘러보기",
  },
]
</script>

<style scoped>
.hero-slider {
  position: relative;
}

/* Swiper가 컨텐츠 높이를 잡도록 */
.hero-swiper {
  width: 100%;
}

/* 오른쪽 아래 네비 버튼 */
.nav {
  position: absolute;
  right: 18px;
  bottom: 18px;
  display: flex;
  gap: 10px;
  z-index: 10;
}

.nav-btn {
  width: 42px;
  height: 42px;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  font-size: 18px;
  background: rgba(255, 255, 255, 0.8);
}

.nav-btn:active {
  transform: scale(0.98);
}
</style>
