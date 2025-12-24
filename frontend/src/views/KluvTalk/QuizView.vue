<template>
  <div class="container">
    <h1>모임 퀴즈</h1>

    <div v-if="store.quizLoading">로딩중...</div>
    <div v-else-if="store.quizError">에러가 발생했어요.</div>

    <div v-else>
      <!-- 아직 제출 전 -->
      <div v-if="!store.quizResult && store.quiz" class="card">
        <h2 class="q">{{ store.quiz.question }}</h2>

        <form @submit.prevent="onSubmit">
          <input v-model="answer" class="input" placeholder="정답 입력" required />
          <button class="btn" type="submit">제출</button>
        </form>

        <RouterLink class="link" :to="{ name: 'kluvtalk-detail', params: { id: meetingId } }">
          모임 정보로 돌아가기
        </RouterLink>
      </div>

      <!-- 제출 후 결과 -->
      <div v-else-if="store.quizResult" class="card">
        <h2 class="q">{{ store.quizResult.question }}</h2>
        <p>당신의 답: {{ store.quizResult.user_answer }}</p>
        <p>정답: {{ store.quizResult.answer }}</p>

        <p v-if="store.quizResult.result" class="ok">정답! 모임 참여가 완료되었습니다.</p>
        <p v-else class="no">틀렸습니다. 모임 참여가 불가합니다.</p>

        <RouterLink class="btn" :to="{ name: 'kluvtalk-detail', params: { id: meetingId } }">
          모임 정보로 돌아가기
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useKluvTalkStore } from '@/stores/kluvTalk'

const route = useRoute()
const store = useKluvTalkStore()
const answer = ref('')

const meetingId = computed(() => Number(route.params.id))

const load = async () => {
  if (!Number.isFinite(meetingId.value)) return
  await store.fetchQuiz(meetingId.value)
  answer.value = ''
}

const onSubmit = async () => {
  await store.submitQuiz(meetingId.value, answer.value)
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

.q {
  margin-top: 0;
}

.input {
  width: 100%;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #ddd;
  margin: 12px 0;
}

.btn {
  display: inline-block;
  padding: 10px 14px;
  border-radius: 10px;
  background: #2d6cdf;
  color: #fff;
  border: 0;
  cursor: pointer;
  text-decoration: none;
}

.link {
  display: inline-block;
  margin-top: 12px;
  color: #2d6cdf;
}

.ok {
  color: #0a8f3d;
  font-weight: 700;
}

.no {
  color: #d33;
  font-weight: 700;
}
</style>
