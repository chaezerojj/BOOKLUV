<template>
  <div class="ai-test-result">
    <h1>AI 설문 결과</h1>

    <div v-if="!result" class="empty">
      결과가 없어요. 테스트부터 진행해 주세요.
    </div>

    <div v-else class="result-container">
      <!-- 성향 분석 -->
      <section class="report">
        <h3>🎯 맞춤 성향 분석 리포트</h3>
        <p>{{ result.ai_reason }}</p>
      </section>

      <!-- 추천 도서 -->
      <section class="books">
        <h2>📚 추천 도서</h2>

        <div v-for="book in result.books" :key="book.id" class="result-book-box">
          <img :src="book.cover_url" alt="" />
          <div class="result-book-detail">
            <h3 class="title">{{ book.title }}</h3>
            <p class="meta">
              {{ book.author_name }} | {{ book.publisher }} | {{ book.category_name }}
            </p>

            <div class="reason">
              <b>추천 포인트:</b> {{ book.reason || "사용자님의 독서 성향에 부합하는 도서입니다." }}
            </div>

            <div class="actions">
              <button @click="goBookDetail(book.id)">책 상세로 이동</button>
              <button @click="goKluvTalkList(book.category_name)">관련 모임 보기</button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAiRecommendStore } from "@/stores/aiRecommend";

const router = useRouter();
const store = useAiRecommendStore();

const result = computed(() => store.result);

const goBookDetail = (bookId) => {
  // ⚠️ 여기 route name은 네 프로젝트 책 상세 라우트 name에 맞춰 바꿔줘
  router.push({ name: "book-detail", params: { bookId } });
};

const goKluvTalkList = (categoryName) => {
  // ⚠️ 모임 리스트 라우트 name에 맞춰 바꿔줘
  router.push({ name: "kluvtalk-list", query: { category: categoryName } });
};
</script>

<style scoped>
.ai-test-result {
  border: 1px solid black;
  margin: 1rem auto;
  padding: 2rem;
  text-align: center;
}

.result-container {
  max-width: 1000px;
  margin: 1.5rem auto 0;
  text-align: left;
}

.report {
  background: #f8faff;
  border-radius: 16px;
  padding: 18px;
  border: 1px solid #e0e8f5;
  margin-bottom: 24px;
}

.report h3 {
  margin: 0 0 10px;
}

.report p {
  margin: 0;
  line-height: 1.8;
}

.result-book-box {
  display: flex;
  gap: 18px;
  background: white;
  border-radius: 12px;
  padding: 18px;
  margin-bottom: 18px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.result-book-box img {
  width: 130px;
  height: 190px;
  object-fit: cover;
  border-radius: 8px;
}

.title {
  margin: 0 0 6px;
}

.meta {
  margin: 0 0 10px;
  color: #777;
  font-size: 14px;
}

.reason {
  background: #fdf6ec;
  padding: 10px 12px;
  border-radius: 8px;
  border-left: 4px solid #f39c12;
  color: #856404;
  margin-bottom: 10px;
}

.actions {
  display: flex;
  gap: 10px;
}

.actions button {
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 10px;
  padding: 10px 12px;
  cursor: pointer;
}

.empty {
  padding: 30px;
  font-weight: 700;
}
</style>
