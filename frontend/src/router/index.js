import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/views/Home/HomeView.vue"),
    },

    {
      path: "/login",
      alias: "/auth/login",
      name: "login",
      component: () => import("@/views/Auth/LoginView.vue"),
    },
    {
      path: "/signup",
      alias: "/auth/signup",
      name: "signup",
      component: () => import("@/views/Auth/SignUpView.vue"),
    },
    {
      // 백엔드에서 redirect로 보내는 곳
      path: "/auth/callback",
      name: "auth-callback",
      component: () => import("@/views/Auth/AuthCallBackView.vue"),
    },

    {
      path: "/search",
      name: "search",
      component: () => import("@/views/Search/SearchResultView.vue"),
    },

    {
      path: "/ai",
      name: "ai-recommend",
      component: () => import("@/views/AI/AiRecommendView.vue"),
    },
    {
      path: "/ai/test",
      name: "ai-test",
      component: () => import("@/views/AI/AiTestView.vue"),
    },
    {
      path: "/ai/result",
      name: "ai-result",
      component: () => import("@/views/AI/AiTestResultView.vue"),
    },

    {
      path: "/kluvtalk",
      name: "kluvtalk-list",
      component: () => import("@/views/KluvTalk/KluvTalkListView.vue"),
    },
    {
      path: "/kluvtalk/create",
      name: "kluvtalk-create",
      component: () => import("@/views/KluvTalk/KluvTalkCreateView.vue"),
    },
    {
      path: "/kluvtalk/:id/edit",
      name: "kluvtalk-update",
      component: () => import("@/views/KluvTalk/KluvTalkCreateView.vue"),
      props: true,
    },
    {
      path: "/kluvtalk/chat/:roomSlug",
      name: "kluvtalk-chat-room",
      component: () => import("@/views/KluvTalk/KluvTalkChatRoomView.vue"),
      props: true,
    },
    {
      path: "/kluvtalk/:id/quiz",
      name: "kluvtalk-quiz",
      component: () => import("@/views/KluvTalk/QuizView.vue"),
      props: true,
    },
    {
      path: "/kluvtalk/:id",
      name: "kluvtalk-detail",
      component: () => import("@/views/KluvTalk/KluvTalkDetailView.vue"),
      props: true,
    },

    {
      path: "/board",
      name: "board",
      component: () => import("@/views/Board/BoardListView.vue"),
    },
    {
      path: "/board/create",
      name: "board-create",
      component: () => import("@/views/Board/BoardCreateView.vue"),
    },
    {
      path: "/board/:id",
      name: "board-detail",
      component: () => import("@/views/Board/BoardDetailView.vue"),
      props: true,
    },
    {
      path: "/board/:id/update",
      name: "board-update",
      component: () => import("@/views/Board/BoardUpdateView.vue"),
      props: true,
    },

    {
      path: "/books/:id",
      name: "book-detail",
      component: () => import("@/views/Books/BookDetailView.vue"),
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
      path: "/alarm",
      name: "alarm",
      component: () => import("@/components/ChatAlarmBell.vue"),
    },

    // {
    //   path: "/:pathMatch(.*)*",
    //   name: "not-found",
    //   component: () => import("@/views/NotFoundView.vue"),
    // },
  ],
});

export default router;
