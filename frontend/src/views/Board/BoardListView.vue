<template>
  <div class="wrap">
    <div class="top">
      <div>
        <h1 class="title">게시판</h1>
        <p class="sub">최신 글을 확인하고 의견을 남겨보세요.</p>
      </div>

      <button
        class="btn write"
        type="button"
        :disabled="!isAuthenticated"
        @click="goCreate"
        :title="!isAuthenticated ? '로그인 후 글을 작성할 수 있어요.' : ''"
      >
        글쓰기
      </button>
    </div>

    <div class="controls">
      <SortDropdown
        v-model="sortKey"
        label="정렬"
        :options="sortOptions"
      />
    </div>

    <div v-if="store.loading" class="state">로딩중...</div>
    <div v-else-if="store.error" class="state error">에러가 발생했어요.</div>

    <ul v-else class="list">
      <li v-for="b in visibleBoards" :key="b.id" class="item">
        <div class="main" @click="goDetail(b.id)">
          <div class="row1">
            <div class="t">{{ b.title }}</div>
            <div class="stats">
              <span class="stat">댓글 {{ b.comment_count ?? 0 }}</span>
              <span class="dot">·</span>
              <span class="stat">조회 {{ viewCount(b) }}</span>
            </div>
          </div>

          <div class="row2">
            <span class="who">{{ b.user?.display_name ?? "Unknown" }}</span>
            <span class="dot">·</span>
            <span class="time">{{ formatDate(b.created_at) }}</span>
          </div>

          <div class="preview">{{ b.content }}</div>
        </div>

        <div class="actions" v-if="isMine(b)">
          <button class="btn" type="button" @click.stop="goUpdate(b.id)">수정</button>
          <button class="btn danger" type="button" @click.stop="onDelete(b.id)">삭제</button>
        </div>
      </li>
    </ul>

    <p v-if="!store.loading && !store.error && visibleBoards.length === 0" class="empty">
      게시글이 없어요.
    </p>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useBoardStore } from "@/stores/board";
import { useAuthStore } from "@/stores/auth";
import SortDropdown from "@/components/common/SortDropdown.vue";

const router = useRouter();
const store = useBoardStore();
const auth = useAuthStore();

onMounted(() => {
  store.fetchBoards();
});

const isAuthenticated = computed(() => auth.isAuthenticated);
const myUserId = computed(() => auth.user?.id ?? null);

const isMine = (b) => {
  const ownerId = b?.user?.id ?? null;
  return isAuthenticated.value && ownerId && ownerId === myUserId.value;
};

const goCreate = () => {
  if (!isAuthenticated.value) return alert("로그인 후 글을 작성할 수 있어요.");
  router.push({ name: "board-create" });
};
const goDetail = (id) => router.push({ name: "board-detail", params: { id } });
const goUpdate = (id) => router.push({ name: "board-update", params: { id } });

const onDelete = async (id) => {
  if (!confirm("삭제할까요?")) return;
  await store.deleteBoard(id);
  await store.fetchBoards();
};

const formatDate = (iso) => (iso ? new Date(iso).toLocaleString() : "");

const sortKey = ref("comments");
const sortOptions = [
  { value: "comments", label: "댓글순" },
  { value: "views", label: "조회수순" },
];

const createdMs = (b) => (b?.created_at ? new Date(b.created_at).getTime() : 0);
const commentCount = (b) => Number(b?.comment_count ?? 0);
const viewCount = (b) => Number(b?.view_count ?? b?.views ?? b?.hit ?? 0);

const visibleBoards = computed(() => {
  const arr = [...(store.boards ?? [])];

  if (sortKey.value === "views") {
    arr.sort((a, b) => {
      const diff = viewCount(b) - viewCount(a);
      if (diff !== 0) return diff;
      return createdMs(b) - createdMs(a);
    });
  } else {
    arr.sort((a, b) => {
      const diff = commentCount(b) - commentCount(a);
      if (diff !== 0) return diff;
      return createdMs(b) - createdMs(a);
    });
  }

  return arr;
});
</script>

<style scoped>
.wrap {
  width: min(900px, 92%);
  margin: 2rem auto;
}

.top {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 12px;
  margin-bottom: 12px;
}

.title {
  margin: 0;
  font-size: 22px;
  letter-spacing: -0.2px;
}

.sub {
  margin: 6px 0 0;
  font-size: 13px;
  opacity: 0.7;
}

.btn {
  border: 1px solid #e3e3e3;
  background: #fff;
  border-radius: 12px;
  padding: 10px 14px;
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

.controls {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 14px;
}

.state {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
  font-size: 13px;
}
.state.error {
  background: #fff6f6;
  border-color: #ffe1e1;
}

.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 12px;
}

.item {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 16px;
  padding: 14px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
  display: grid;
  gap: 10px;
}

.main {
  cursor: pointer;
}

.row1 {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
}

.t {
  font-weight: 800;
  letter-spacing: -0.2px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.stats {
  font-size: 12px;
  opacity: 0.8;
  white-space: nowrap;
}
.stat {
  font-weight: 600;
}
.dot {
  margin: 0 6px;
  opacity: 0.6;
}

.row2 {
  display: flex;
  align-items: center;
  gap: 0;
  font-size: 12px;
  opacity: 0.75;
}

.preview {
  margin-top: 8px;
  opacity: 0.9;
  white-space: pre-wrap;
  line-height: 1.55;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  padding-top: 6px;
  border-top: 1px solid #f0f0f0;
}

.empty {
  margin-top: 14px;
  opacity: 0.75;
  text-align: center;
}
</style>
