<template>
    <section class="comments">
        <h3>댓글 ({{ comments.length }})</h3>

        <form class="comment-form" @submit.prevent="onCreate">
            <input v-model="newComment" :disabled="!isAuthenticated"
                :placeholder="isAuthenticated ? '댓글을 입력하세요' : '로그인 후 댓글을 작성할 수 있어요'" maxlength="200" />
            <button type="submit" :disabled="!isAuthenticated || !newComment.trim()">등록</button>
        </form>

        <ul class="comment-list">
            <li v-for="c in comments" :key="c.id" class="comment-item">
                <div class="row">
                    <div class="who">{{ c.user?.display_name ?? "Unknown" }}</div>
                    <div class="time">{{ formatDate(c.created_at) }}</div>
                </div>

                <div v-if="editingId !== c.id" class="text">
                    {{ c.content }}
                </div>

                <div v-else class="editbox">
                    <input v-model="editingText" maxlength="200" />
                    <div class="edit-actions">
                        <button type="button" @click="onUpdate(c.id)" :disabled="!canEditComment(c)">
                            저장
                        </button>
                        <button type="button" @click="cancelEdit">취소</button>
                    </div>
                </div>

                <div class="actions" v-if="editingId !== c.id && canEditComment(c)">
                    <button type="button" @click="startEdit(c)">수정</button>
                    <button type="button" @click="onDelete(c.id)">삭제</button>
                </div>
            </li>
        </ul>

        <div class="bottom">
            <button type="button" @click="$emit('goList')">목록</button>
        </div>
    </section>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useAuthStore } from "@/stores/auth";

const props = defineProps({
    boardId: { type: Number, required: true },
    comments: { type: Array, default: () => [] },
    // 댓글 액션은 부모가 store로 수행
    onCreateComment: { type: Function, required: true },
    onUpdateComment: { type: Function, required: true },
    onDeleteComment: { type: Function, required: true },
});

defineEmits(["goList"]);

const auth = useAuthStore();
const isAuthenticated = computed(() => auth.isAuthenticated);
const myUserId = computed(() => auth.user?.id ?? null);

const formatDate = (iso) => (iso ? new Date(iso).toLocaleString() : "");

// 댓글 작성
const newComment = ref("");
const onCreate = async () => {
    if (!isAuthenticated.value) return alert("로그인 후 댓글을 작성할 수 있어요.");
    if (!newComment.value.trim()) return;

    try {
        await props.onCreateComment(props.boardId, { content: newComment.value.trim() });
        newComment.value = "";
    } catch {
        alert("댓글 작성에 실패했어요.");
    }
};

// 댓글 수정/삭제 권한
const canEditComment = (c) => {
    const ownerId = c?.user?.id ?? null;
    return isAuthenticated.value && ownerId && ownerId === myUserId.value;
};

const commentActionHint = (c) => {
    if (!isAuthenticated.value) return "로그인 후 이용할 수 있어요.";
    if (!canEditComment(c)) return "작성자만 수정/삭제할 수 있어요.";
    return "";
};

// 인라인 수정 상태
const editingId = ref(null);
const editingText = ref("");

watch(
    () => props.comments,
    () => {
        // 댓글 목록이 갱신되면 편집 상태가 꼬이지 않게 초기화
        editingId.value = null;
        editingText.value = "";
    }
);

const startEdit = (c) => {
    if (!isAuthenticated.value) return alert("로그인 후 수정할 수 있어요.");
    if (!canEditComment(c)) return alert("댓글 작성자만 수정할 수 있어요.");
    editingId.value = c.id;
    editingText.value = c.content;
};

const cancelEdit = () => {
    editingId.value = null;
    editingText.value = "";
};

const onUpdate = async (commentId) => {
    const target = props.comments.find((x) => x.id === commentId);
    if (!isAuthenticated.value) return alert("로그인 후 수정할 수 있어요.");
    if (!canEditComment(target)) return alert("댓글 작성자만 수정할 수 있어요.");

    await props.onUpdateComment(props.boardId, commentId, { content: editingText.value.trim() });
    cancelEdit();
};

const onDelete = async (commentId) => {
    const target = props.comments.find((x) => x.id === commentId);
    if (!isAuthenticated.value) return alert("로그인 후 삭제할 수 있어요.");
    if (!canEditComment(target)) return alert("댓글 작성자만 삭제할 수 있어요.");
    if (!confirm("댓글 삭제할까요?")) return;

    await props.onDeleteComment(props.boardId, commentId);
};
</script>

<style scoped>
.comments {}

.comment-form {
    display: flex;
    gap: 8px;
    margin: 10px 0 16px;
}

.comment-form input {
    flex: 1;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
}

.comment-form input:disabled {
    background: #f7f7f7;
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

.comment-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 10px;
}

.comment-item {
    border: 1px solid #eee;
    border-radius: 12px;
    padding: 12px;
}

.row {
    display: flex;
    gap: 10px;
    align-items: center;
    font-size: 12px;
    opacity: .85;
}

.who {
    font-weight: 700;
}

.text {
    margin: 8px 0;
    white-space: pre-wrap;
}

.actions {
    display: flex;
    gap: 8px;
}

.editbox {
    margin-top: 8px;
    display: grid;
    gap: 8px;
}

.editbox input {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
}

.edit-actions {
    display: flex;
    gap: 8px;
}

.bottom {
    margin-top: 16px;
}
</style>
