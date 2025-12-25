<template>
  <div class="wrap">
    <div v-if="store.loading" class="state">로딩중...</div>
    <div v-else-if="store.error" class="state error">에러가 발생했어요.</div>

    <div v-else-if="store.board" class="card">
      <div class="header">
        <div class="head-left">
          <h1 class="title">{{ store.board.title }}</h1>
          <div class="meta">
            <span>작성자: {{ store.board.user?.display_name ?? "Unknown" }}</span>
            <span>·</span>
            <span>{{ formatDate(store.board.created_at) }}</span>
          </div>
        </div>

        <div class="header-actions" v-if="canEditBoard">
          <button class="btn" type="button" @click="onClickBoardEdit">
            수정
          </button>
          <button class="btn danger" type="button" @click="onClickBoardDelete">
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

.card {
  background: #fff;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 22px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.04);
}

.state {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
  font-size: 13px;
}

.state.error {
  background: #fff6f6;
  border-color: #ffe1e1;
}

.header {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: flex-start;
}

.title {
  margin: 0;
  font-size: 26px;
  letter-spacing: -0.2px;
}

.meta {
  display: flex;
  gap: 10px;
  font-size: 13px;
  opacity: 0.75;
  margin-top: 8px;
  flex-wrap: wrap;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.content {
  margin: 18px 0 8px;
  white-space: pre-wrap;
  padding: 16px;
  line-height: 1.8;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f1f1f1;
}

.line {
  margin-top: 2rem;
  border: 0;
  border-top: 1px solid #eee;
}

.btn {
  border: 1px solid #e3e3e3;
  background: #fff;
  border-radius: 12px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 13px;
}

.btn:hover {
  background: #fafafa;
}

.btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.btn.danger:hover {
  background: #fff6f6;
}

.content {
  margin: 14px 0 4px;
  white-space: pre-wrap;
  padding: 14px;
  line-height: 1.6;
}

.line {
  margin-top: 3rem;
  border: 0;
  border-top: 1px solid #eee;
}
</style>
