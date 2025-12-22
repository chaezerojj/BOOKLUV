<template>
  <div class="ai-test">
    <h1>AI 취향 설문조사</h1>

    <form class="test-container" @submit.prevent="onSubmit">
      <!-- q1 -->
      <div class="q">
        <label>1) 책을 읽는 가장 큰 목적은?</label>
        <select v-model="answers.q1" required>
          <option value="">선택</option>
          <option value="A">재미있게 몰입하고 싶어서</option>
          <option value="B">생각의 폭을 넓히고 싶어서</option>
          <option value="C">현실에 바로 써먹을 인사이트</option>
          <option value="D">위로나 공감을 받고 싶어서</option>
        </select>
      </div>

      <!-- q2 -->
      <div class="q">
        <label>2) 더 끌리는 책은?</label>
        <select v-model="answers.q2" required>
          <option value="">선택</option>
          <option value="A">요즘 많이 회자되는 신간</option>
          <option value="B">시간이 지나도 읽히는 고전</option>
          <option value="C">상관없다</option>
        </select>
      </div>

      <!-- q3 -->
      <div class="q">
        <label>3) 책을 고를 때 가장 먼저 보는 건?</label>
        <select v-model="answers.q3" required>
          <option value="">선택</option>
          <option value="A">줄거리와 소재</option>
          <option value="B">주제와 메시지</option>
          <option value="C">추천·평점</option>
          <option value="D">저자</option>
        </select>
      </div>

      <!-- q4 -->
      <div class="q">
        <label>4) 가장 선호하는 장르는?</label>
        <select v-model="answers.q4" required>
          <option value="">선택</option>
          <option value="A">소설 / 에세이</option>
          <option value="B">자기계발 / 심리</option>
          <option value="C">인문 / 사회 / 철학</option>
          <option value="D">SF / 판타지 / 추리</option>
        </select>
      </div>

      <!-- q5 -->
      <div class="q">
        <label>5) 책의 분위기는 어떤 게 좋아?</label>
        <select v-model="answers.q5" required>
          <option value="">선택</option>
          <option value="A">따뜻하고 편안한</option>
          <option value="B">현실적이고 날카로운</option>
          <option value="C">묵직하고 깊은</option>
          <option value="D">가볍고 유쾌한</option>
        </select>
      </div>

      <!-- q6 -->
      <div class="q">
        <label>6) 읽을 때 더 중요한 요소는?</label>
        <select v-model="answers.q6" required>
          <option value="">선택</option>
          <option value="A">스토리 전개와 몰입감</option>
          <option value="B">문장과 표현의 아름다움</option>
          <option value="C">배울 점과 정리된 구조</option>
          <option value="D">감정선과 공감</option>
        </select>
      </div>

      <!-- q7 -->
      <div class="q">
        <label>7) 책 한 권 분량 선호는?</label>
        <select v-model="answers.q7" required>
          <option value="">선택</option>
          <option value="A">짧고 빠르게 읽히는 책</option>
          <option value="B">적당한 분량</option>
          <option value="C">길어도 OK</option>
        </select>
      </div>

      <!-- q8 -->
      <div class="q">
        <label>8) 독서 스타일은?</label>
        <select v-model="answers.q8" required>
          <option value="">선택</option>
          <option value="A">몰아서 읽는다</option>
          <option value="B">틈틈이 나눠 읽는다</option>
          <option value="C">필요한 부분만 골라 읽는다</option>
        </select>
      </div>

      <!-- q9 -->
      <div class="q">
        <label>9) 책을 다 읽고 나면 보통?</label>
        <select v-model="answers.q9" required>
          <option value="">선택</option>
          <option value="A">여운이 남는 게 좋다</option>
          <option value="B">생각을 정리하게 된다</option>
          <option value="C">실천해보고 싶어진다</option>
          <option value="D">바로 다음 책을 찾는다</option>
        </select>
      </div>

      <!-- q10 -->
      <div class="q">
        <label>10) 지금 나에게 더 필요한 책은?</label>
        <select v-model="answers.q10" required>
          <option value="">선택</option>
          <option value="A">마음을 가볍게 해주는 책</option>
          <option value="B">생각할 거리를 던지는 책</option>
          <option value="C">현실에 도움 되는 책</option>
          <option value="D">새로운 세계를 보여주는 책</option>
        </select>
      </div>

      <button class="submit" type="submit" :disabled="store.loading">
        {{ store.loading ? "분석 중..." : "테스트 결과 보기" }}
      </button>

      <p v-if="store.error" class="err">에러가 발생했어요. 콘솔을 확인해 주세요.</p>
    </form>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAiRecommendStore } from "@/stores/aiRecommend";

const router = useRouter();
const store = useAiRecommendStore();

// store.answers를 그대로 바인딩
const answers = computed(() => store.answers);

const onSubmit = async () => {
  try {
    await store.submitQuiz();
    router.push({ name: "ai-result" });
  } catch (e) {
    console.error(e);
  }
};
</script>

<style scoped>
.ai-test {
  border: 1px solid black;
  margin: 1rem auto;
  padding: 2rem;
  text-align: center;
}

.test-container {
  width: 720px;
  margin: 0 auto;
  display: grid;
  gap: 14px;
  text-align: left;
}

.q label {
  display: block;
  font-weight: 700;
  margin-bottom: 6px;
}

.q select {
  width: 100%;
  height: 40px;
  border-radius: 10px;
  border: 1px solid #ddd;
  padding: 0 10px;
}

.submit {
  margin-top: 12px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid #ddd;
  background: #fff;
  font-weight: 800;
  cursor: pointer;
}

.err {
  color: #d33;
  font-weight: 700;
}
</style>
