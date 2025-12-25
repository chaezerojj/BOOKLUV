<template>
  <div class="container">
    <h1>모임 퀴즈</h1>

    <div v-if="store.quizLoading">로딩중...</div>
    <div v-else-if="store.quizError">에러가 발생했어요.</div>

    <div v-else-if="store.quiz" class="card">
      <h2 class="q">{{ store.quiz.question }}</h2>

      <!-- ✅ locked면 아예 못 풀게 -->
      <div v-if="isLocked" class="lockedBox">
        <p class="no">
          3번 모두 틀려서 참여가 불가합니다.
        </p>
        <RouterLink class="btn ghost" :to="{ name: 'kluvtalk-detail', params: { id: meetingId } }">
          모임 상세로 돌아가기
        </RouterLink>
      </div>

      <template v-else>
        <!-- ✅ 남은 기회(제출 전에도 보여줌: GET에서 attempts_left 내려오므로) -->
        <div class="attempts" v-if="attemptsLeft !== null">
          남은 기회: <b>{{ attemptsLeft }}</b> / {{ MAX_ATTEMPTS }}
        </div>

        <!-- ✅ 제출 결과 -->
        <div v-if="store.quizResult" class="resultBox">
          <p v-if="store.quizResult.result" class="ok">
            정답! 모임 참여가 완료되었습니다.
          </p>
          <template v-else>
            <p class="no">틀렸습니다.</p>
            <p class="leftMsg" v-if="attemptsLeft !== null">
              기회가 <b>{{ attemptsLeft }}</b>번 남았습니다.
            </p>

            <!-- ✅ 기회 남으면 다시 풀기 버튼 -->
            <button
              v-if="attemptsLeft > 0"
              class="btn ghost"
              type="button"
              @click="retry"
            >
              다시 풀기
            </button>

            <!-- ✅ 0이면 곧 locked될 거라 안내 -->
            <p v-else class="no">
              시도 횟수를 모두 소진했습니다. 참여가 불가합니다.
            </p>
          </template>
        </div>

        <!-- ✅ 입력 폼: 정답 맞추면 숨김 / (틀렸어도 retry 누르기 전이면 숨김) -->
        <form v-if="canTry" class="form" @submit.prevent="onSubmit">
          <input v-model.trim="answer" class="input" placeholder="정답 입력" required />
          <button class="btn" type="submit" :disabled="submitting">
            {{ submitting ? "제출 중..." : "제출" }}
          </button>
        </form>

        <RouterLink class="link" :to="{ name: 'kluvtalk-detail', params: { id: meetingId } }">
          모임 정보로 돌아가기
        </RouterLink>
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useKluvTalkStore } from "@/stores/kluvTalk";

const route = useRoute();
const store = useKluvTalkStore();

const MAX_ATTEMPTS = 3;
const answer = ref("");
const submitting = ref(false);

const meetingId = computed(() => Number(route.params.id));

const load = async () => {
  if (!Number.isFinite(meetingId.value)) return;
  store.quizResult = null;      // 페이지 들어올 때만 초기화
  await store.fetchQuiz(meetingId.value);
  answer.value = "";
};

const attemptsLeft = computed(() => {
  // ✅ 제출 후엔 quizResult, 제출 전/새로고침엔 quiz(GET)에서
  const r = store.quizResult?.attempts_left;
  if (typeof r === "number") return r;

  const g = store.quiz?.attempts_left;
  if (typeof g === "number") return g;

  return null;
});

const isLocked = computed(() => {
  const r = store.quizResult?.locked;
  if (typeof r === "boolean") return r;

  const g = store.quiz?.locked;
  if (typeof g === "boolean") return g;

  return attemptsLeft.value === 0; // 안전장치
});

const canTry = computed(() => {
  if (!store.quiz) return false;
  if (isLocked.value) return false;

  // 이미 참여 완료(joined)면 더 안 풀게
  if (store.quiz?.joined) return false;
  if (store.quizResult?.result) return false;

  // ✅ 제출 결과가 없으면 바로 풀 수 있음
  if (!store.quizResult) return true;

  // ✅ 틀린 상태면 "다시 풀기" 눌러서 quizResult를 지운 뒤에 풀게 함
  return false;
});

const retry = () => {
  store.quizResult = null; // ✅ 결과 화면 닫고 입력폼 다시 열기
  answer.value = "";
};

const onSubmit = async () => {
  if (!Number.isFinite(meetingId.value)) return;
  if (!answer.value) return;

  submitting.value = true;
  try {
    await store.submitQuiz(meetingId.value, answer.value);
    answer.value = "";
  } finally {
    submitting.value = false;
  }
};

onMounted(load);
watch(() => route.params.id, load);
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 16px;
}

.card {
  background: #fff;
  padding: 18px;
  border-radius: 12px;
  border: 1px solid #eee;
}

.q {
  margin-top: 0;
  font-weight: 900;
}

.attempts {
  margin: 10px 0 14px;
  font-size: 13px;
  color: #666;
}

.resultBox, .lockedBox {
  margin: 12px 0;
  padding: 12px 14px;
  border-radius: 12px;
  background: #fafafa;
  border: 1px solid #eee;
}

.leftMsg {
  margin: 8px 0 0;
  font-size: 13px;
  color: #444;
}

.form {
  margin-top: 10px;
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

.btn.ghost {
  background: #fff;
  color: #2d6cdf;
  border: 1px solid #cfe0ff;
}

.btn:disabled {
  opacity: .6;
  cursor: not-allowed;
}

.link {
  display: inline-block;
  margin-top: 12px;
  color: #2d6cdf;
}

.ok {
  color: #0a8f3d;
  font-weight: 900;
}

.no {
  color: #d33;
  font-weight: 900;
}
</style>
