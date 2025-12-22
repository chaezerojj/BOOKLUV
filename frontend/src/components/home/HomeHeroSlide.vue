<template>
  <div class="slide">
    <div class="left">
      <img :src="imageSrc" :alt="imageAlt" class="img" />
    </div>

    <div class="right">
      <p class="kicker" v-if="kicker">{{ kicker }}</p>
      <h2 class="title">{{ title }}</h2>
      <p class="desc" v-if="desc">{{ desc }}</p>

      <div class="cta">
        <span class="cta-text">{{ buttonText }}</span>
        <span class="arrow">➡️</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  imageSrc: { type: String, required: true },
  imageAlt: { type: String, default: "" },
  kicker: { type: String, default: "" }, // 작은 라벨
  title: { type: String, required: true },
  desc: { type: String, default: "" },
  buttonText: { type: String, default: "자세히보기" },
})
</script>

<style scoped>
.slide{
  height: 250px;
  display:flex;
  align-items:center;
  border-radius:15px;
  padding: 2rem;
  gap: 2rem;
}
.left{ flex: 0 0 auto; }
.img{ width: 300px; display:block; }
.right{
  flex:1;
  display:flex;
  flex-direction:column;
  align-items:flex-end;
  text-align:right;
  gap: .5rem;
}
.kicker{ font-size:14px; opacity:.8; margin:0; }
.title{ font-size:26px; font-weight:500; margin:0; }
.desc{ font-size:16px; opacity:.9; margin:0; max-width: 520px; }
.cta{
  margin-top: .5rem;
  display:flex; align-items:center; gap:.4rem;
  font-size:18px;
}
</style>
