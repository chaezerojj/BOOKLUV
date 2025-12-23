<template>
  <div class="wrap">
    <header class="page-head">
      <h1 class="page-title">글 수정</h1>
      <p class="page-desc">내용을 수정하고 저장해 주세요.</p>
    </header>

    <div class="card">
      <div v-if="store.loading" class="state">로딩중...</div>
      <div v-else-if="store.error" class="state error">에러가 발생했어요.</div>

      <BoardForm
        v-else
        v-model:title="title"
        v-model:content="content"
        :loading="store.loading"
        submitText="저장"
        @submit="onSubmit"
        @cancel="goDetail"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useBoardStore } from "@/stores/board";
import { useAuthStore } from "@/stores/auth";
import BoardForm from "@/components/board/BoardForm.vue";

const store = useBoardStore();
const auth = useAuthStore();

const route = useRoute();
const router = useRouter();

const id = Number(route.params.id);
const title = ref("");
const content = ref("");

const goDetail = () => router.push({ name: "board-detail", params: { id } });

onMounted(async () => {
  if (!auth.isAuthenticated) {
    alert("로그인 후 수정할 수 있어요.");
    return router.replace({ name: "login" });
  }

  await store.fetchBoard(id);

  const ownerId = store.board?.user?.id ?? null;
  if (!ownerId || ownerId !== auth.user?.id) {
    alert("작성자만 수정할 수 있어요.");
    return goDetail();
  }

  title.value = store.board?.title ?? "";
  content.value = store.board?.content ?? "";
});

const onSubmit = async ({ title, content }) => {
  if (!auth.isAuthenticated) return alert("로그인 후 수정할 수 있어요.");
  const ownerId = store.board?.user?.id ?? null;
  if (!ownerId || ownerId !== auth.user?.id) return alert("작성자만 수정할 수 있어요.");

  await store.updateBoard(id, { title, content });
  goDetail();
};
</script>

<style scoped>
.wrap {
  width: min(900px, 92%);
  margin: 2rem auto;
}

.page-head {
  margin-bottom: 14px;
}

.page-title {
  margin: 0;
  font-size: 22px;
  letter-spacing: -0.2px;
}

.page-desc {
  margin: 6px 0 0;
  font-size: 13px;
  opacity: 0.7;
}

.card {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
}

.state {
  padding: 14px;
  border-radius: 12px;
  background: #fafafa;
  border: 1px solid #eee;
  font-size: 13px;
}
.state.error {
  background: #fff6f6;
  border-color: #ffe1e1;
}
</style>
