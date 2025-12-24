<template>
  <div class="wrap">
    <h1>글 수정</h1>

    <div v-if="store.loading">로딩중...</div>
    <div v-else-if="store.error">에러가 발생했어요.</div>

    <BoardForm v-else v-model:title="title" v-model:content="content" :loading="store.loading" submitText="저장"
      @submit="onSubmit" @cancel="goDetail" />
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
</style>
