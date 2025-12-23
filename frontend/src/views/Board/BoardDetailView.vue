<template>
  <div class="wrap">
    <div v-if="store.loading">로딩중...</div>
    <div v-else-if="store.error">에러가 발생했어요.</div>

    <div v-else-if="store.board">
      <div class="header">
        <div>
          <h1 class="title">{{ store.board.title }}</h1>
          <div class="meta">
            <span>작성자: {{ store.board.user?.display_name ?? "Unknown" }}</span>
            <span>{{ formatDate(store.board.created_at) }}</span>
          </div>
        </div>

        <div class="header-actions">
          <button type="button" :disabled="!canEditBoard" @click="onClickBoardEdit" :title="boardActionHint">
            수정
          </button>
          <button type="button" :disabled="!canEditBoard" @click="onClickBoardDelete" :title="boardActionHint">
            삭제
          </button>
        </div>
      </div>

      <div class="content">{{ store.board.content }}</div>

      <hr class="line" />

      <BoardComments :boardId="boardId" :comments="store.comments" :onCreateComment="store.createComment"
        :onUpdateComment="store.updateComment" :onDeleteComment="store.deleteComment" @goList="goList" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useBoardStore } from "@/stores/board";
import { useAuthStore } from "@/stores/auth";
import BoardComments from "@/components/board/BoardComments.vue";

const store = useBoardStore();
const auth = useAuthStore();

const route = useRoute();
const router = useRouter();
const boardId = ref(Number(route.params.id));

watch(
  () => route.params.id,
  (v) => {
    boardId.value = Number(v);
    store.fetchBoard(boardId.value);
  }
);

onMounted(() => {
  store.fetchBoard(boardId.value);
});

const formatDate = (iso) => (iso ? new Date(iso).toLocaleString() : "");

const isAuthenticated = computed(() => auth.isAuthenticated);
const myUserId = computed(() => auth.user?.id ?? null);

const isBoardOwner = computed(() => {
  const ownerId = store.board?.user?.id ?? null;
  return !!ownerId && ownerId === myUserId.value;
});

const canEditBoard = computed(() => isAuthenticated.value && isBoardOwner.value);
const boardActionHint = computed(() => {
  if (!isAuthenticated.value) return "로그인 후 이용할 수 있어요.";
  if (!isBoardOwner.value) return "작성자만 수정/삭제할 수 있어요.";
  return "";
});

const goList = () => router.push({ name: "board" });

// 게시글 액션
const onClickBoardEdit = () => {
  if (!isAuthenticated.value) return alert("로그인 후 수정할 수 있어요.");
  if (!isBoardOwner.value) return alert("작성자만 수정할 수 있어요.");
  router.push({ name: "board-update", params: { id: boardId.value } });
};

const onClickBoardDelete = async () => {
  if (!isAuthenticated.value) return alert("로그인 후 삭제할 수 있어요.");
  if (!isBoardOwner.value) return alert("작성자만 삭제할 수 있어요.");
  if (!confirm("삭제할까요?")) return;

  await store.deleteBoard(boardId.value);
  goList();
};
</script>

<style scoped>
.wrap {
  width: min(900px, 92%);
  margin: 2rem auto;
}

.header {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: flex-start;
}

.title {
  margin: 0;
}

.meta {
  display: flex;
  gap: 10px;
  font-size: 12px;
  opacity: .8;
  margin-top: 6px;
}

.header-actions {
  display: flex;
  gap: 8px;
}

button {
  border: 1px solid #ddd;
  background: white;
  border-radius: 10px;
  padding: 8px 12px;
  cursor: pointer;
}

button:disabled {
  opacity: .45;
  cursor: not-allowed;
}

.content {
  margin: 1rem 0;
  white-space: pre-wrap;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 14px;
}

.line {
  margin: 1.5rem 0;
  border: 0;
  border-top: 1px solid #eee;
}
</style>
