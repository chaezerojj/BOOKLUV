<template>
  <div class="container">
    <div v-if="store.loading">로딩중...</div>
    <div v-else-if="store.error">에러가 발생했어요.</div>

    <div v-else-if="store.meeting" class="card">
      <h1 class="title">{{ store.meeting.title }}</h1>

      <p><b>책 제목:</b> {{ store.meeting.book_title }}</p>
      <p><b>리더:</b> {{ store.meeting.leader_name ?? '-' }}</p>
      <p><b>멤버 수:</b> {{ store.meeting.members }}</p>
      <p><b>조회수:</b> {{ store.meeting.views }}</p>
      <p><b>설명:</b> {{ store.meeting.description }}</p>

      <RouterLink class="btn" :to="{ name: 'kluvtalk-quiz', params: { id: meetingId } }">
        퀴즈 풀고 참여하기
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useKluvTalkStore } from '@/stores/kluvTalk';

const route = useRoute()
const store = useKluvTalkStore()

const meetingId = computed(() => Number(route.params.id))

const load = async () => {
  if (!Number.isFinite(meetingId.value)) return
  await store.fetchKluvTalk(meetingId.value)
}

onMounted(load)
watch(() => route.params.id, load)
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 16px;
}

.card {
  background: #fff;
  padding: 16px;
  border-radius: 12px;
}

.title {
  margin: 0 0 12px;
}

.btn {
  display: inline-block;
  margin-top: 12px;
  padding: 10px 14px;
  border-radius: 10px;
  background: #2d6cdf;
  color: #fff;
  text-decoration: none;
}
</style>
