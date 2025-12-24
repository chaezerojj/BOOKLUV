<template>
  <div class="wrap">
    <h1>글쓰기</h1>

    <BoardForm v-model:title="title" v-model:content="content" :loading="store.loading" submitText="작성"
      :errorText="store.error ? '저장 실패' : ''" @submit="onSubmit" @cancel="goList" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useBoardStore } from "@/stores/board";
import { useAuthStore } from "@/stores/auth";
import BoardForm from "@/components/board/BoardForm.vue";

const store = useBoardStore();
const auth = useAuthStore();
const router = useRouter();

const title = ref("");
const content = ref("");

onMounted(() => {
  if (!auth.isAuthenticated) {
    alert("로그인 후 글을 작성할 수 있어요.");
    router.replace({ name: "login" });
  }
});

const goList = () => router.push({ name: "board" });

const onSubmit = async ({ title, content }) => {
  if (!auth.isAuthenticated) {
    alert("로그인 후 글을 작성할 수 있어요.");
    return router.push({ name: "login" });
  }
  const created = await store.createBoard({ title, content });
  router.push({ name: "board-detail", params: { id: created.id } });
};
</script>

<style scoped>
.wrap {
  width: min(900px, 92%);
  margin: 2rem auto;
}
</style>
