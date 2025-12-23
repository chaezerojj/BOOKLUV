import { http } from "@/api/http";

export const boardAPI = {
  list() {
    return http.get("/api/v1/board/");
  },
  detail(id) {
    return http.get(`/api/v1/board/${id}/`);
  },
  create(payload) {
    return http.post("/api/v1/board/", payload);
  },
  update(id, payload) {
    return http.patch(`/api/v1/board/${id}/`, payload);
  },
  remove(id) {
    return http.delete(`/api/v1/board/${id}/`);
  },

  commentList(boardId) {
    return http.get(`/api/v1/board/${boardId}/comments/`);
  },
  commentCreate(boardId, payload) {
    return http.post(`/api/v1/board/${boardId}/comments/`, payload);
  },
  commentUpdate(boardId, commentId, payload) {
    return http.patch(`/api/v1/board/${boardId}/comments/${commentId}/`, payload);
  },
  commentRemove(boardId, commentId) {
    return http.delete(`/api/v1/board/${boardId}/comments/${commentId}/`);
  },
};
