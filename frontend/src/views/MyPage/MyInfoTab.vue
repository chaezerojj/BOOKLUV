<template>
  <section class="info-wrap">
    <h2 class="title">회원 정보 수정</h2>

    <form class="form" @submit.prevent="onSubmit">
      <div class="field">
        <label>닉네임</label>
        <input
          type="text"
          v-model.trim="nickname"
          placeholder="닉네임을 입력하세요"
        />
      </div>

      <div class="field">
        <label>이메일</label>
        <input type="text" :value="email" readonly />
      </div>

      <div class="field">
        <label>가입일</label>
        <input type="text" :value="joinedAt" readonly />
      </div>

      <button class="submit" type="submit" :disabled="saving">
        {{ saving ? "저장중..." : "수정하기" }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">저장 완료!</p>
    </form>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();

const saving = ref(false);
const error = ref("");
const success = ref(false);

const nickname = ref("");

const email = computed(() => auth.user?.email ?? "-");
const joinedAt = computed(() => {
  const raw = auth.user?.date_joined;
  if (!raw) return "-";
  const d = new Date(raw);
  return isNaN(d.getTime()) ? String(raw) : d.toLocaleString();
});

watch(
  () => auth.user,
  (u) => {
    if (u?.nickname !== undefined) nickname.value = u.nickname ?? "";
  },
  { immediate: true }
);

onMounted(async () => {
  if (!auth.user) await auth.fetchMe();
});

const onSubmit = async () => {
  error.value = "";
  success.value = false;

  try {
    saving.value = true;
    await auth.updateProfile({ nickname: nickname.value });
    success.value = true;
    setTimeout(() => (success.value = false), 1500);
  } catch (e) {
    error.value =
      e?.response?.data?.detail ||
      e?.response?.data?.message ||
      "저장에 실패했어요.";
  } finally {
    saving.value = false;
  }
};
</script>

<style scoped>
/* ✅ 바깥 박스는 MyPageLayout의 routerview 카드가 담당 -> 여긴 border 없음 */
.info-wrap {
  width: 100%;
  text-align: center;
}

.title {
  margin: 1.25rem;
  margin-bottom: 2.5rem;
  font-size: 18px;
  font-weight: 800;
}

.form {
  width: 400px;
  margin: 0 auto;
  display: grid;
  gap: 14px;
}

.field {
  display: grid;
  grid-template-columns: 70px 1fr;
  align-items: center;
  gap: 10px;
}

label {
  text-align: left;
  font-weight: 700;
  font-size: 14px;
}

input {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #d7d7d7;
  border-radius: 10px;
  outline: none;
  box-sizing: border-box;
}

input:focus {
  border-color: #323232;
}

input[readonly] {
  background: #f6f6f6;
  color: #666;
}

.submit {
  margin-top: 10px;
  height: 44px;
  border: none;
  border-radius: 12px;
  background: #ffefc2;
  box-shadow: 2px 2px 8px rgba(161, 161, 161, 0.25);
  color: #323232;
  cursor: pointer;
  font-weight: 800;
}

.submit:hover {
    background: #ffeab2;
}

.submit:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.error {
  margin: 0;
  color: #d33;
  font-size: 13px;
}

.success {
  margin: 0;
  color: #1a7f37;
  font-size: 13px;
  font-weight: 600;
}
</style>
