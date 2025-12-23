<template>
  <div class="slide">
    <img :src="imageSrc" :alt="imageAlt" class="img" />
  </div>
</template>

<script setup>
defineProps({
  imageSrc: { type: String, required: true },
  imageAlt: { type: String, default: "" },
})
</script>

<style scoped>
/* 원하는 높이/모양 여기서 통일 */
.slide {
  height: 500px;
  border-radius: 15px;
  overflow: hidden; 
}

/* 슬라이드 꽉 채우기 */
.img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}
</style>
