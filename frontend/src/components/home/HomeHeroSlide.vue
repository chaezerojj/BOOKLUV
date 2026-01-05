<template>
  <div class="slide">
    <img ref="imgRef" :src="src" :alt="imageAlt" class="img" />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue"

const props = defineProps({
  imageSrc: { type: String, required: true },
  imageAlt: { type: String, default: "" },
  // 첫 슬라이드만 즉시 로드하기 위해서 옵션
  priority: { type: Boolean, default: false },
})

// 첫 장은 바로 src 세팅, 나머지는 빈 src로 시작해서 네트워크 요청 자체를 막음
const src = ref(props.priority ? props.imageSrc : "")

const imgRef = ref(null)
let io = null

onMounted(() => {
  if (props.priority) return
  if (!imgRef.value) return

  io = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) {
        src.value = props.imageSrc
        io?.disconnect()
        io = null
      }
    },
    { threshold: 0.1 }
  )

  io.observe(imgRef.value)
})

onBeforeUnmount(() => {
  io?.disconnect()
  io = null
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
