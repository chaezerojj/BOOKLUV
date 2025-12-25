<template>
  <div class="wrap">
    <div class="card">
      <div class="head">
        <h1 class="title">KluvTalk 만들기</h1>
        <p class="sub">책 기반 독서 모임을 생성하고 퀴즈를 등록해요.</p>
      </div>

      <!-- ✅ 선택된 책(고정) 안내 + 책 정보 -->
      <div class="bookBox">
        <div class="bookCover">
          <img
            v-if="book?.cover_url && !coverBroken"
            :src="book.cover_url"
            class="cover"
            alt="book cover"
            loading="lazy"
            @error="coverBroken = true"
          />
          <div v-else class="coverFallback">No Cover</div>
        </div>

        <div class="bookInfo">
          <div class="bookBadge">선택된 책</div>

          <div v-if="bookLoading" class="bookState">책 정보를 불러오는 중...</div>
          <div v-else-if="bookError" class="bookState errorText">{{ bookError }}</div>

          <template v-else>
            <div class="bookTitle">{{ book?.title || `Book #${bookId}` }}</div>
            <div class="bookMeta">
              <span v-if="book?.author_name">✍️ {{ book.author_name }}</span>
              <span v-if="book?.category_name"> · {{ book.category_name }}</span>
            </div>

            <div class="bookHint">
              현재 페이지는 <b>bookId={{ bookId }}</b> ({{ book?.title || "선택된 책" }})로
              <b>모임을 생성</b>하는 페이지예요.
            </div>
          </template>
        </div>
      </div>

      <!-- ✅ 생성 폼 -->
      <form class="form" @submit.prevent="onSubmit">
        <section class="sec">
          <h3 class="secTitle">모임 정보</h3>

          <label class="field">
            <span class="label">모임 제목</span>
            <input
              v-model.trim="form.title"
              class="input"
              type="text"
              maxlength="50"
              placeholder="모임 제목을 입력해주세요."
            />
            <span v-if="errors.title" class="err">{{ errors.title }}</span>
          </label>

          <label class="field">
            <span class="label">설명 (최대 200자)</span>
            <textarea
              v-model.trim="form.description"
              class="textarea"
              maxlength="200"
              placeholder="모임 설명을 입력해주세요."
            ></textarea>
            <div class="hint">{{ form.description.length }} / 200</div>
            <span v-if="errors.description" class="err">{{ errors.description }}</span>
          </label>

          <div class="row">
            <label class="field">
              <span class="label">인원 (2~10)</span>
              <input v-model.number="form.members" class="input" type="number" min="2" max="10" />
              <span v-if="errors.members" class="err">{{ errors.members }}</span>
            </label>
          </div>

          <div class="row">
            <label class="field">
              <span class="label">시작 시간</span>
              <input v-model="form.started_at" class="input" type="datetime-local" />
            </label>

            <label class="field">
              <span class="label">종료 시간</span>
              <input v-model="form.finished_at" class="input" type="datetime-local" />
            </label>
          </div>

          <span v-if="errors.time" class="err">{{ errors.time }}</span>
        </section>

        <section class="sec">
          <h3 class="secTitle">퀴즈 정보</h3>

          <label class="field">
            <span class="label">질문</span>
            <input
              v-model.trim="form.quiz.question"
              class="input"
              type="text"
              maxlength="50"
              placeholder="퀴즈 질문을 입력하세요"
            />
          </label>

          <label class="field">
            <span class="label">정답</span>
            <input
              v-model.trim="form.quiz.answer"
              class="input"
              type="text"
              maxlength="50"
              placeholder="정답을 입력하세요"
            />
          </label>
        </section>

        <div v-if="submitError" class="state error">{{ submitError }}</div>

        <div class="actions">
          <button class="btn primary" type="submit" :disabled="submitting || bookLoading">
            {{ submitting ? "생성 중..." : "모임 만들기" }}
          </button>

          <RouterLink class="btn" :to="{ name: 'kluvtalk-list' }">취소</RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { http } from "@/api/http";

const route = useRoute();
const router = useRouter();

/**
 * ✅ bookId가 "항상" 있다고 가정
 * - 권장: 라우터를 /kluvtalk/create/:bookId 처럼 path param으로 바꾸는게 제일 안전
 * - 현재는 query로 받는 구조이므로, bookId가 없으면 NaN -> null이 될 수 있음
 */
const bookId = computed(() => {
  const raw = route.query.bookId ?? route.query.book_id ?? route.query.bookid;
  return Number(raw);
});

const coverBroken = ref(false);

/** 책 정보 */
const book = ref(null);
const bookLoading = ref(false);
const bookError = ref("");

async function fetchBook(id) {
  bookLoading.value = true;
  bookError.value = "";
  book.value = null;
  coverBroken.value = false;

  try {
    // ✅ 너 백엔드: GET /api/v1/books/<book_id>/
    const res = await http.get(`/api/v1/books/${id}/`);
    book.value = res?.data?.book ?? null;
  } catch (e) {
    bookError.value =
      e?.response?.data?.detail || "책 정보를 불러오지 못했어요. (bookId 확인 필요)";
  } finally {
    bookLoading.value = false;
  }
}

/** bookId가 바뀌면 책 정보 다시 로드 */
watch(
  () => bookId.value,
  (id) => {
    // 여기서 id가 NaN이면 fetchBook이 깨지므로 방어
    if (!Number.isFinite(id) || id <= 0) {
      book.value = null;
      bookError.value = "bookId가 유효하지 않아요. 라우팅에서 bookId 전달을 확인해 주세요.";
      return;
    }
    fetchBook(id);
  },
  { immediate: true }
);

/** 폼 */
const submitting = ref(false);
const submitError = ref("");

const errors = reactive({
  title: "",
  description: "",
  members: "",
  time: "",
});

const form = reactive({
  title: "",
  description: "",
  members: 2,
  started_at: "",
  finished_at: "",
  quiz: {
    question: "",
    answer: "",
  },
});

function resetErrors() {
  errors.title = "";
  errors.description = "";
  errors.members = "";
  errors.time = "";
  submitError.value = "";
}

function toISOFromDatetimeLocal(dtLocal) {
  if (!dtLocal) return "";
  const d = new Date(dtLocal);
  return Number.isFinite(d.getTime()) ? d.toISOString() : "";
}

function validate() {
  resetErrors();

  if (!form.title.trim()) errors.title = "모임 제목을 입력해주세요.";
  if (form.description.length > 200) errors.description = "설명은 200자 이하여야 합니다.";

  if (!Number.isFinite(form.members) || form.members < 2 || form.members > 10) {
    errors.members = "인원은 2~10명이어야 합니다.";
  }

  const startIso = toISOFromDatetimeLocal(form.started_at);
  const endIso = toISOFromDatetimeLocal(form.finished_at);

  if (!startIso || !endIso) {
    errors.time = "시작/종료 시간을 입력해주세요.";
  } else {
    const s = new Date(startIso).getTime();
    const e = new Date(endIso).getTime();
    const now = Date.now();

    if (!(s < e)) errors.time = "시작 시간은 종료 시간보다 빨라야 합니다.";
    else if (s < now) errors.time = "시작 시간은 현재 이후여야 합니다.";
  }

  return !errors.title && !errors.description && !errors.members && !errors.time;
}

async function onSubmit() {
  // bookId가 항상 있다고 가정하지만, 안전하게 체크는 유지
  if (!Number.isFinite(bookId.value) || bookId.value <= 0) {
    submitError.value = "bookId가 유효하지 않아요. 라우팅에서 bookId 전달을 확인해 주세요.";
    return;
  }

  if (!validate()) return;

  submitting.value = true;
  submitError.value = "";

  try {
    const payload = {
      book_id: bookId.value,
      title: form.title.trim(),
      description: form.description.trim(),
      members: form.members,
      started_at: toISOFromDatetimeLocal(form.started_at),
      finished_at: toISOFromDatetimeLocal(form.finished_at),
      quiz: {
        question: form.quiz.question.trim(),
        answer: form.quiz.answer.trim(),
      },
    };

    const res = await http.post("/api/v1/books/meetings/", payload);

    const newId = res?.data?.id;
    if (newId) {
      router.push({ name: "kluvtalk-detail", params: { id: newId } });
    } else {
      router.push({ name: "kluvtalk-list" });
    }
  } catch (e) {
    const msg =
      e?.response?.data?.detail ||
      (typeof e?.response?.data === "string" ? e.response.data : null) ||
      "모임 생성에 실패했어요.";
    submitError.value = msg;

    const data = e?.response?.data;
    if (data && typeof data === "object") {
      if (data.title) errors.title = String(data.title);
      if (data.description) errors.description = String(data.description);
      if (data.members) errors.members = String(data.members);
      if (data.time) errors.time = String(data.time);
    }
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.wrap {
  max-width: 920px;
  margin: 0 auto;
  padding: 28px 16px;
}

.card {
  background: #fff;
  border-radius: 18px;
  border: 1px solid #eee;
  margin-top: 2rem;
  padding: 22px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
}

.head {
  padding-bottom: 14px;
  border-bottom: 1px solid #f1f1f1;
  margin-bottom: 18px;
}

.title {
  margin: 0;
  font-size: 26px;
  font-weight: 900;
  letter-spacing: -0.02em;
}

.sub {
  margin: 8px 0 0;
  color: #666;
}

/* ✅ 선택된 책 영역 */
.bookBox {
  display: grid;
  grid-template-columns: 92px 1fr;
  gap: 12px;
  align-items: start;
  border: 1px solid #f1f1f1;
  background: #fffdf6;
  border-radius: 14px;
  padding: 12px;
  margin-bottom: 16px;
}

.bookCover {
  width: 92px;
}

.cover {
  width: 100%;
  aspect-ratio: 3 / 4;
  object-fit: cover;
  border-radius: 12px;
  border: 1px solid #eee;
  background: #fafafa;
}

.coverFallback {
  width: 100%;
  aspect-ratio: 3 / 4;
  border-radius: 12px;
  border: 1px dashed #ddd;
  background: #fff;
  display: grid;
  place-items: center;
  color: #999;
  font-weight: 900;
  font-size: 12px;
}

.bookInfo {
  min-width: 0;
}

.bookBadge {
  display: inline-block;
  font-size: 12px;
  font-weight: 900;
  padding: 6px 10px;
  border-radius: 999px;
  background: #fff2c2;
  border: 1px solid #ffe08a;
}

.bookTitle {
  margin-top: 8px;
  font-size: 16px;
  font-weight: 900;
  line-height: 1.35;
}

.bookMeta {
  margin-top: 6px;
  font-size: 13px;
  color: #666;
}

.bookHint {
  margin-top: 8px;
  font-size: 12px;
  color: #777;
  line-height: 1.4;
}

.bookState {
  margin-top: 8px;
  font-size: 13px;
  color: #666;
}

.errorText {
  color: #d33;
  font-weight: 900;
}

/* ✅ 폼 */
.form {
  display: grid;
  gap: 16px;
}

.sec {
  border: 1px solid #f1f1f1;
  border-radius: 14px;
  padding: 14px;
  background: #fcfcfc;
}

.secTitle {
  margin: 0 0 12px;
  font-size: 15px;
  font-weight: 900;
}

.field {
  display: grid;
  gap: 6px;
  margin-bottom: 12px;
}

.label {
  font-size: 12px;
  color: #666;
  font-weight: 800;
}

.input,
.textarea {
  border: 1px solid #e6e6e6;
  border-radius: 12px;
  padding: 10px 12px;
  font-size: 14px;
  background: #fff;
}

.textarea {
  font-family: Pretendard;
  min-height: 120px;
  resize: vertical;
}

.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

@media (max-width: 720px) {
  .row {
    grid-template-columns: 1fr;
  }
}

.hint {
  font-size: 12px;
  color: #888;
}

.err {
  font-size: 12px;
  color: #d33;
  font-weight: 800;
}

/* ✅ 상태 */
.state {
  padding: 12px 14px;
  background: #fff;
  border-radius: 14px;
  border: 1px solid #eee;
}

.state.error {
  border-color: #ffdddd;
  background: #fff7f7;
}

/* ✅ 버튼 */
.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid #e6e6e6;
  background: #fff;
  text-decoration: none;
  color: inherit;
  font-weight: 900;
  cursor: pointer;
}

.btn.primary {
  border-color: #ffe08a;
  background: #fff2c2;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
