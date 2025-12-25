<template>
  <div class="ai-test">

    <form class="test-container" @submit.prevent="onSubmit">
      <h1>🔎 AI 취향 설문조사</h1>
      <!-- q1 -->
      <div class="q">
        <label class="q-label">1. 책을 읽는 가장 큰 목적은?</label>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q1" value="A" v-model="answers.q1" required />
            <span> 재미있게 몰입하고 싶어서</span>
          </label>
          <label class="opt">
            <input type="radio" name="q1" value="B" v-model="answers.q1" />
            <span> 생각의 폭을 넓히고 싶어서</span>
          </label>
          <label class="opt">
            <input type="radio" name="q1" value="C" v-model="answers.q1" />
            <span> 현실에 바로 써먹을 인사이트</span>
          </label>
          <label class="opt">
            <input type="radio" name="q1" value="D" v-model="answers.q1" />
            <span> 위로나 공감을 받고 싶어서</span>
          </label>
        </div>
      </div>

      <!-- q2 -->
      <div class="q">
        <label class="q-label">2. 더 끌리는 책은?</label>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q2" value="A" v-model="answers.q2" required />
            <span> 요즘 많이 회자되는 신간</span>
          </label>
          <label class="opt">
            <input type="radio" name="q2" value="B" v-model="answers.q2" />
            <span> 시간이 지나도 읽히는 고전</span>
          </label>
          <label class="opt">
            <input type="radio" name="q2" value="C" v-model="answers.q2" />
            <span> 신간이든 고전이든 상관없다</span>
          </label>
        </div>
      </div>

      <!-- q3 -->
      <div class="q">
        <label class="q-label">3. 책을 고를 때 가장 먼저 보는 건?</label>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q3" value="A" v-model="answers.q3" required />
            <span> 줄거리와 소재</span>
          </label>
          <label class="opt">
            <input type="radio" name="q3" value="B" v-model="answers.q3" />
            <span> 주제와 메시지</span>
          </label>
          <label class="opt">
            <input type="radio" name="q3" value="C" v-model="answers.q3" />
            <span> 추천·평점</span>
          </label>
          <label class="opt">
            <input type="radio" name="q3" value="D" v-model="answers.q3" />
            <span> 저자</span>
          </label>
        </div>
      </div>

      <!-- q4 -->
      <div class="q">
        <label class="q-label">4. 가장 선호하는 장르는?</label>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q4" value="novel" v-model="answers.q4" required />
            <span> 소설</span>
          </label>
          <label class="opt">
            <input type="radio" name="q4" value="essay" v-model="answers.q4" />
            <span> 에세이</span>
          </label>
          <label class="opt">
            <input type="radio" name="q4" value="self_help" v-model="answers.q4" />
            <span> 자기계발</span>
          </label>
          <label class="opt">
            <input type="radio" name="q4" value="humanities" v-model="answers.q4" />
            <span> 인문학</span>
          </label>
          <label class="opt">
            <input type="radio" name="q4" value="art" v-model="answers.q4" />
            <span> 예술</span>
          </label>
        </div>
      </div>

      <!-- q5 -->
      <div class="q">
        <label class="q-label">5. 책의 분위기는 어떤 게 좋아?</label>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q5" value="A" v-model="answers.q5" required />
            <span> 따뜻하고 편안한</span>
          </label>
          <label class="opt">
            <input type="radio" name="q5" value="B" v-model="answers.q5" />
            <span> 현실적이고 날카로운</span>
          </label>
          <label class="opt">
            <input type="radio" name="q5" value="C" v-model="answers.q5" />
            <span> 묵직하고 깊은</span>
          </label>
          <label class="opt">
            <input type="radio" name="q5" value="D" v-model="answers.q5" />
            <span> 가볍고 유쾌한</span>
          </label>
        </div>
      </div>

      <!-- q6 -->
      <div class="q">
        <label class="q-label">6. 읽을 때 더 중요한 요소는?</label>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q6" value="A" v-model="answers.q6" required />
            <span> 스토리 전개와 몰입감</span>
          </label>
          <label class="opt">
            <input type="radio" name="q6" value="B" v-model="answers.q6" />
            <span> 문장과 표현의 아름다움</span>
          </label>
          <label class="opt">
            <input type="radio" name="q6" value="C" v-model="answers.q6" />
            <span> 배울 점과 정리된 구조</span>
          </label>
          <label class="opt">
            <input type="radio" name="q6" value="D" v-model="answers.q6" />
            <span> 감정선과 공감</span>
          </label>
        </div>
      </div>

      <!-- q7 -->
      <div class="q">
        <label class="q-label">7. 책 한 권 분량에 대한 선호는?</label>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q7" value="A" v-model="answers.q7" required />
            <span> 짧고 빠르게 읽히는 책</span>
          </label>
          <label class="opt">
            <input type="radio" name="q7" value="B" v-model="answers.q7" />
            <span> 적당한 분량이면 좋다</span>
          </label>
          <label class="opt">
            <input type="radio" name="q7" value="C" v-model="answers.q7" />
            <span> 길어도 완성도 있으면 OK</span>
          </label>
        </div>
      </div>

      <!-- q8 -->
      <div class="q">
        <label class="q-label">8. 독서 스타일은?</label>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q8" value="A" v-model="answers.q8" required />
            <span> 한 번 시작하면 몰아서 읽는다</span>
          </label>
          <label class="opt">
            <input type="radio" name="q8" value="B" v-model="answers.q8" />
            <span> 틈틈이 나눠 읽는다</span>
          </label>
          <label class="opt">
            <input type="radio" name="q8" value="C" v-model="answers.q8" />
            <span> 필요한 부분만 골라 읽는다</span>
          </label>
        </div>
      </div>

      <!-- q9 -->
      <div class="q">
        <label class="q-label">9. 책을 다 읽고 나면 보통?</label>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q9" value="A" v-model="answers.q9" required />
            <span> 여운이 남는 게 좋다</span>
          </label>
          <label class="opt">
            <input type="radio" name="q9" value="B" v-model="answers.q9" />
            <span> 생각을 정리하게 된다</span>
          </label>
          <label class="opt">
            <input type="radio" name="q9" value="C" v-model="answers.q9" />
            <span> 실천해보고 싶어진다</span>
          </label>
          <label class="opt">
            <input type="radio" name="q9" value="D" v-model="answers.q9" />
            <span> 바로 다음 책을 찾는다</span>
          </label>
        </div>
      </div>

      <!-- q10 -->
      <div class="q">
        <label class="q-label">10. 지금 나에게 더 필요한 책은?</label>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q10" value="A" v-model="answers.q10" required />
            <span> 마음을 가볍게 해주는 책</span>
          </label>
          <label class="opt">
            <input type="radio" name="q10" value="B" v-model="answers.q10" />
            <span> 생각할 거리를 던지는 책</span>
          </label>
          <label class="opt">
            <input type="radio" name="q10" value="C" v-model="answers.q10" />
            <span> 현실에 도움 되는 책</span>
          </label>
          <label class="opt">
            <input type="radio" name="q10" value="D" v-model="answers.q10" />
            <span> 새로운 세계를 보여주는 책</span>
          </label>
        </div>
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
  margin: 1rem auto;
  padding: 2rem;
  text-align: center;
}

.test-container {
  background-color: #fefefe;
  width: 1000px;
  margin: 0 auto;
  display: grid;
  gap: 14px;
  text-align: center;
  margin: 0 auto;
  margin-top: 3rem;
  padding: 2rem;
  padding-top: 3.5rem;
  box-shadow: 0px 0px 8px rgba(161, 161, 161, 0.1);
  border-radius: 5px;
}

.test-container h1 {
  text-align: center;
  padding: 1rem;
  padding-bottom: 3rem;
}

.q {
  text-align: center;
  padding: 2rem 6rem;
  padding-bottom: 4.5rem;
  /* background-color: #fff; */
}

.q label {
  display: block;
  font-weight: 700;
  margin-bottom: 6px;
}

.q-label {
  font-size: 24px;
  padding-bottom: 2.5rem;
  letter-spacing: -0.05rem;
}

.options {
  display: grid;
  gap: 10px;
}

.opt {
  letter-spacing: -0.03rem;
  margin: 0 auto;
  background-color: #ebebeb;
  width: 300px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 12px;
  border-radius: 12px;
  cursor: pointer;
  user-select: none;
  text-align: left;
  justify-content: center;
}

.opt input {
  margin: 0 1rem;
  width: 18px;
  height: 18px;
}

.opt span {
  padding: 0.1rem;
}

.submit {
  justify-self: center;
  margin-top: 12px;
  width: 330px;
  height: 60px;
  border-radius: 12px;
  border: 1px solid #ddd;
  background: #fff;
  font-weight: 600;
  cursor: pointer;
  font-size: 19px;
  letter-spacing: -0.06rem;
}

.err {
  color: #d33;
  font-weight: 700;
}
</style>
