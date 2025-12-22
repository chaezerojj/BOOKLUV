<template>
  <div class="ai-test-result">
    <div v-if="!result" class="empty">
      결과가 없어요. 테스트부터 진행해 주세요.
    </div>

    <div v-else class="result-container">
      <div class="result-inner">
        <section class="report">
          <h3 class="report-text">🎯 맞춤 성향 분석 리포트</h3>
          <p>{{ result.ai_reason }}</p>
        </section>

        <section class="books">
          <h2>📚 추천 도서</h2>

          <div v-for="book in result.books" :key="book.id" class="result-book-box">
            <img class="book-img" :src="book.cover_url" alt="" />
            <div class="result-book-detail">
              <h3 class="title">{{ book.title }}</h3>
              <p class="meta">
                {{ book.author_name }} | {{ book.publisher }} | {{ book.category_name }}
              </p>

              <div class="reason">
                <b>추천 포인트:</b> {{ book.reason || "사용자님의 독서 성향에 부합하는 도서입니다." }}
              </div>

              <div class="actions">
                <RouterLink class="btn-link" :to="{ name: 'book-detail', params: { id: book.id } }">
                  책 상세로 이동
                </RouterLink>
                <RouterLink class="btn-link" :to="{ name: 'kluvtalk-list', query: { category: book.category_name } }">
                  관련 모임 보기
                </RouterLink>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>


<script setup>
import { computed } from "vue";
import { useAiRecommendStore } from "@/stores/aiRecommend";

const store = useAiRecommendStore();
const result = computed(() => store.result);
</script>


<style scoped>
.ai-test-result {
  display: flex;
  margin: 1rem auto;
  margin-top: 3rem;
  width: 100%;
}

.result-container {
  width: 1300px;
  border-radius: 20px;
  background-color: #fff;
}

.result-inner {
  margin: 3rem;
  margin-left: 4rem;
  text-align: center;
}

.report {
  margin-bottom: 3rem;
}

.report-text {
  font-weight: 700;
  font-size: 25px;
}

.result-book-box {
  display: flex;
  text-align: center;
  justify-content: center;
}

.book-img {
  margin: 1rem;
  border: 10px solid #fff;
  border-radius: 20px;
  box-shadow: 2px 2px 8px rgba(161, 161, 161, 0.25);
}

.result-book-detail {
  margin: 2rem;
  text-align: left;
  width: 600px;
  line-height: 2rem;
}

.actions {
  margin-top: 1.5rem;
  display: flex;
  gap: 10px;
}

/* RouterLink용 버튼 스타일 */
.btn-link {
  display: inline-block;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 10px;
  padding: 10px 12px;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  font-size: 14px;
}

.btn-link:hover {
  transform: translateY(-1px);
  box-shadow: 2px 2px 12px rgba(161, 161, 161, 0.25);
}
</style>
