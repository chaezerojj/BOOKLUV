<template>
  <div class="wrap">
    <div class="top">
      <h1 class="title">게시판</h1>

      <button
        class="write"
        type="button"
        :disabled="!isAuthenticated"
        @click="goCreate"
        :title="!isAuthenticated ? '로그인 후 글을 작성할 수 있어요.' : ''"
      >
        글쓰기
      </button>
    </div>

    <!-- 필터/정렬 바 -->
    <div class="controls">
      <div class="left">
        <label class="ctrl">
          정렬
          <select v-model="sortKey">
            <option value="new">최신순</option>
            <option value="comments">댓글순</option>
          </select>
        </label>

        <label class="ctrl">
          NEW 기준(시간)
          <input v-model.number="newHours" type="number" min="1" max="168" />
        </label>

        <label class="ctrl">
          HOT 기준(댓글)
          <input v-model.number="hotComments" type="number" min="1" max="999" />
        </label>
      </div>

      <div class="right">
        <label class="toggle">
          <input type="checkbox" v-model="onlyHot" />
          HOT만 보기
        </label>

        <label class="toggle">
          <input type="checkbox" v-model="onlyNew" />
          NEW만 보기
        </label>
      </div>
    </div>

    <div v-if="store.loading">로딩중...</div>
    <div v-else-if="store.error">에러가 발생했어요.</div>

    <ul v-else class="list">
      <li v-for="b in visibleBoards" :key="b.id" class="item">
        <div class="main" @click="goDetail(b.id)">
          <div class="row1">
            <div class="t">
              {{ b.title }}

              <!-- 배지들 -->
              <span class="badges">
                <span v-if="isNew(b)" class="badge badge-new">NEW</span>
                <span v-if="isHot(b)" class="badge badge-hot">HOT</span>
                <span v-if="isTopByComments(b)" class="badge badge-top">TOP</span>
              </span>
            </div>

            <div class="cc">댓글 {{ b.comment_count ?? 0 }}</div>
          </div>

          <div class="row2">
            <span class="who">{{ b.user?.display_name ?? "Unknown" }}</span>
            <span class="time">{{ formatDate(b.created_at) }}</span>
          </div>

          <div class="preview">{{ b.content }}</div>
        </div>

        <!-- 내 글일 때만 보임 -->
        <div class="actions" v-if="isMine(b)">
          <button type="button" @click.stop="goUpdate(b.id)">수정</button>
          <button type="button" @click.stop="onDelete(b.id)">삭제</button>
        </div>
      </li>
    </ul>

    <p v-if="!store.loading && !store.error && visibleBoards.length === 0" class="empty">
      조건에 맞는 게시글이 없어요.
    </p>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useBoardStore } from "@/stores/board";
import { useAuthStore } from "@/stores/auth";

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

// -------------------------
// 프론트 필터/정렬/배지
// -------------------------
const sortKey = ref("new"); // 'new' | 'comments'
const newHours = ref(24); // NEW 기준: 최근 N시간
const hotComments = ref(5); // HOT 기준: 댓글 N개 이상
const onlyHot = ref(false);
const onlyNew = ref(false);

const createdMs = (b) => (b?.created_at ? new Date(b.created_at).getTime() : 0);
const commentCount = (b) => Number(b?.comment_count ?? 0);

const isNew = (b) => {
  const now = Date.now();
  const diff = now - createdMs(b);
  return diff >= 0 && diff <= newHours.value * 60 * 60 * 1000;
};

const isHot = (b) => commentCount(b) >= hotComments.value;

// 댓글 상위 3개 TOP 배지
const topCommentIds = computed(() => {
  const sorted = [...(store.boards ?? [])].sort((a, b) => commentCount(b) - commentCount(a));
  const top3 = sorted.slice(0, 3).filter((x) => commentCount(x) > 0); // 댓글 0이면 TOP 의미없어서 제외
  return new Set(top3.map((x) => x.id));
});
const isTopByComments = (b) => topCommentIds.value.has(b.id);

const visibleBoards = computed(() => {
  let arr = [...(store.boards ?? [])];

  // 필터
  if (onlyHot.value) arr = arr.filter((b) => isHot(b));
  if (onlyNew.value) arr = arr.filter((b) => isNew(b));

  // 정렬
  if (sortKey.value === "comments") {
    arr.sort((a, b) => {
      const diff = commentCount(b) - commentCount(a);
      if (diff !== 0) return diff;
      return createdMs(b) - createdMs(a); // 댓글 같으면 최신순
    });
  } else {
    arr.sort((a, b) => createdMs(b) - createdMs(a));
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
  align-items: center;
  margin-bottom: 12px;
}

.title {
  margin: 0;
}

.write {
  border: 1px solid #ddd;
  background: white;
  border-radius: 10px;
  padding: 10px 14px;
  cursor: pointer;
}
.write:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

/* 컨트롤 바 */
.controls {
  border: 1px solid #eee;
  border-radius: 14px;
  padding: 12px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}
.left, .right {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}
.ctrl {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 13px;
}
.ctrl select, .ctrl input {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 6px 10px;
}
.toggle {
  display: flex;
  gap: 6px;
  align-items: center;
  font-size: 13px;
  user-select: none;
}

/* 리스트 */
.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 12px;
}

.item {
  border: 1px solid #eee;
  border-radius: 14px;
  padding: 12px;
  display: grid;
  gap: 10px;
}

.main {
  cursor: pointer;
}

.row1 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.t {
  font-weight: 800;
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.badges {
  display: inline-flex;
  gap: 6px;
  align-items: center;
}
.badge {
  font-size: 11px;
  border: 1px solid #ddd;
  border-radius: 999px;
  padding: 2px 8px;
}
.badge-new { }
.badge-hot { }
.badge-top { }

.cc {
  font-size: 12px;
  opacity: 0.8;
}

.row2 {
  display: flex;
  gap: 10px;
  font-size: 12px;
  opacity: 0.8;
  margin-top: 6px;
}

.preview {
  margin-top: 10px;
  opacity: 0.9;
  white-space: pre-wrap;

  /* 길면 보기 좋게 살짝 자르기(원하면 제거 가능) */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.actions button {
  border: 1px solid #ddd;
  background: white;
  border-radius: 10px;
  padding: 8px 12px;
  cursor: pointer;
}

.empty {
  margin-top: 14px;
  opacity: 0.8;
  text-align: center;
}
</style>
