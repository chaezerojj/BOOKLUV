<template>
  <div class="ai-test-result">
    <div v-if="!result" class="empty">
      결과가 없어요. 테스트부터 진행해 주세요.
    </div>

    <div v-else class="result-container">
      <div class="result-inner">

        <section class="books">
          <h2 class="recommend-main-text">💛 Bookluv가 추천하는 도서를 알려드릴게요!</h2>

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
                <span class="detail-text">🙌 상세 페이지에서 해당 책의 모임을 보실 수 있습니다.</span>
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
  margin-top: 5rem;
  width: 100%;
  justify-content: center;
}

.result-container {
  width: 1000px;
  border-radius: 20px;
  background-color: #ffffff;
}

.result-inner {
  margin: 3rem;
  margin-left: 4rem;
  padding: 0.5rem 1rem;
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
  border: 7px solid #fff;
  border-radius: 20px;
  box-shadow: 2px 2px 8px rgba(161, 161, 161, 0.25);
}

.result-book-detail {
  margin: 2rem;
  text-align: left;
  width: 600px;
  line-height: 2rem;
}

.title {
  font-size: 24px;
}

.meta {
  font-size: 18px;
}

.reason {
  font-size: 16px;
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
  font-size: 15px;
  font-weight: 700;
}

.btn-link:hover {
  transform: translateY(-1px);
  box-shadow: 2px 2px 12px rgba(161, 161, 161, 0.25);
}

.detail-text {
  margin-top: 0.6rem;
  margin-left: 0.6rem;
  font-size: 14px;
  font-weight: 700;
}
</style>
