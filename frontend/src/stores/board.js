import { defineStore } from "pinia";
import { boardAPI } from "@/api/board";
import router from "@/router";

function handleApiError(e, fallbackMsg = "요청에 실패했어요.") {
  const status = e?.response?.status;

  if (status === 401) {
    alert("로그인 후 이용할 수 있어요.");
    router.push({ name: "login" });
    return;
  }
  if (status === 403) {
    alert("권한이 없습니다.");
    return;
  }

  // 서버가 detail 내려주면 그걸 우선
  const detail = e?.response?.data?.detail;
  alert(detail || fallbackMsg);
}

export const useBoardStore = defineStore("board", {
  state: () => ({
    loading: false,
    error: null,
    boards: [],
    board: null,
    comments: [],
  }),

  actions: {
    async fetchBoards() {
      this.loading = true;
      this.error = null;
      try {
        const res = await boardAPI.list();
        this.boards = res.data;
      } catch (e) {
        this.error = e;
        handleApiError(e, "게시글 목록을 불러오지 못했어요.");
      } finally {
        this.loading = false;
      }
    },

    async fetchBoard(id) {
      this.loading = true;
      this.error = null;
      try {
        const res = await boardAPI.detail(id);
        this.board = res.data;
        this.comments = res.data.comments ?? [];
      } catch (e) {
        this.error = e;
        this.board = null;
        this.comments = [];
        handleApiError(e, "게시글을 불러오지 못했어요.");
      } finally {
        this.loading = false;
      }
    },

    async createBoard(payload) {
      this.loading = true;
      this.error = null;
      try {
        const res = await boardAPI.create(payload);
        return res.data;
      } catch (e) {
        this.error = e;
        handleApiError(e, "게시글 저장에 실패했어요.");
        throw e;
      } finally {
        this.loading = false;
      }
    },

    async updateBoard(id, payload) {
      this.loading = true;
      this.error = null;
      try {
        const res = await boardAPI.update(id, payload);
        this.board = res.data;
        this.comments = res.data.comments ?? [];
        return res.data;
      } catch (e) {
        this.error = e;
        handleApiError(e, "게시글 수정에 실패했어요.");
        throw e;
      } finally {
        this.loading = false;
      }
    },

    async deleteBoard(id) {
      this.loading = true;
      this.error = null;
      try {
        await boardAPI.remove(id);
      } catch (e) {
        this.error = e;
        handleApiError(e, "게시글 삭제에 실패했어요.");
        throw e;
      } finally {
        this.loading = false;
      }
    },

    async createComment(boardId, payload) {
      try {
        const res = await boardAPI.commentCreate(boardId, payload);
        this.comments.push(res.data);
        return res.data;
      } catch (e) {
        handleApiError(e, "댓글 작성에 실패했어요.");
        throw e;
      }
    },

    async updateComment(boardId, commentId, payload) {
      try {
        const res = await boardAPI.commentUpdate(boardId, commentId, payload);
        this.comments = this.comments.map((c) => (c.id === commentId ? res.data : c));
        return res.data;
      } catch (e) {
        handleApiError(e, "댓글 수정에 실패했어요.");
        throw e;
      }
    },

    async deleteComment(boardId, commentId) {
      try {
        await boardAPI.commentRemove(boardId, commentId);
        this.comments = this.comments.filter((c) => c.id !== commentId);
      } catch (e) {
        handleApiError(e, "댓글 삭제에 실패했어요.");
        throw e;
      }
    },
  },
});
