import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/Home/HomeView.vue";

import AiRecommendView from "@/views/AI/AiRecommendView.vue";
import AiTestView from "@/views/AI/AiTestView.vue";
import AiTestResultView from "@/views/AI/AiTestResultView.vue";

import LoginView from "@/views/Auth/LoginView.vue";
import SignUpView from "@/views/Auth/SignUpView.vue";

import KluvTalkListView from "@/views/KluvTalk/KluvTalkListView.vue";
import KluvTalkDetailView from "@/views/KluvTalk/KluvTalkDetailView.vue";
import KluvTalkCreateView from "@/views/KluvTalk/KluvTalkCreateView.vue";

import BoardListView from "@/views/Board/BoardListView.vue";
import BoardCreateView from "@/views/Board/BoardCreateView.vue";
import BoardDetailView from "@/views/Board/BoardDetailView.vue";
import BookDetailView from "@/views/Books/BookDetailView.vue";
import Notification from "@/views/MyPage/Notification.vue";
import BoardUpdateView from "@/views/Board/BoardUpdateView.vue";
import SearchResultView from "@/views/Search/SearchResultView.vue";
import AuthCallBackView from "@/views/Auth/AuthCallBackView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/auth/login", 
      name: "login", 
      component: LoginView,
    },
    {
      path: "/auth/signup",
      name: "signup",
      component: SignUpView,
    },
    // 백엔드에서 redirect로 보내는 곳
    {
      path: "/auth/callback",
      name: "auth-callback",
      component: AuthCallBackView,
    },
    {
      path: "/search",
      name: 'search',
      component: SearchResultView,
    },
    {
      path: "/ai",
      name: "ai-recommend",
      component: AiRecommendView,
    },
    {
      path: "/ai/test",
      name: 'ai-test',
      component: AiTestView,
    },
    {
      path: "/ai/result",
      name: 'ai-result',
      component: AiTestResultView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/kluvtalk",
      name: "kluvtalk-list",
      component: KluvTalkListView,
    },
    {
      path: "/kluvtalk/:id",
      name: "kluvtalk-detail",
      component: KluvTalkDetailView,
      props: true,
    },
    {
      path: "/kluvtalk/create",
      name: "kluvtalk-create",
      component: KluvTalkCreateView,
    },
    {
      path: "/kluvtalk",
      name: "kluvtalk-list",
      component: KluvTalkListView,
    },
    {
      path: '/kluvtalk/:id',
      name: 'kluvtalk-detail',
      component: () => import('@/views/KluvTalk/KluvTalkDetailView.vue'),
      props: true,
    },
    {
      path: '/kluvtalk/:id/quiz',
      name: 'kluvtalk-quiz',
      component: () => import('@/views/KluvTalk/QuizView.vue'),
      props: true,
    },

    {
      path: "/board",
      name: "board",
      component: BoardListView,
    },
    {
      path: "/board/create",
      name: "board-create",
      component: BoardCreateView,
    },
    {
      path: "/board/:id",
      name: "board-detail",
      component: BoardDetailView,
      props: true,
    },
    {
      path: "/board/:id",
      name: "board-update",
      component: BoardUpdateView,
    },

    {
      path: "/books/:id",
      name: "book-detail",
      component: () => import('@/views/Books/BookDetailView.vue'),
      props: true,
    },
    
    {
      path: "/mypage",
      name: "mypage",
      component: () => import("@/views/MyPage/MyPageLayout.vue"),
      children: [
        {
          path: "",
          name: "mypage-info",
          component: () => import("@/views/MyPage/MyInfoTab.vue"),
        },
        {
          path: "mykluv",
          name: "mypage-mykluv",
          component: () => import("@/views/MyPage/MyKluvTab.vue"),
        },
      ],
    },
    {
      path: "/notification",
      name: "notification",
      component: Notification,
    },
  ],
});

export default router;
