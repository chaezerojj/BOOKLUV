import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/Home/HomeView.vue'

import AiRecommendView from '@/views/AI/AiRecommendView.vue'

import LoginView from '@/views/Auth/LoginView.vue'
import SignUpView from '@/views/Auth/SignUpView.vue'

import KluvTalkListView from '@/views/KluvTalk/KluvTalkListView.vue'
import KluvTalkDetailView from '@/views/KluvTalk/KluvTalkDetailView.vue'
import KluvTalkCreateView from '@/views/KluvTalk/KluvTalkCreateView.vue'

import BoardListView from '@/views/Board/BoardListView.vue'
import BoardCreateView from '@/views/Board/BoardCreateView.vue'
import BoardDetailView from '@/views/Board/BoardDetailView.vue'
import BookDetailView from '@/views/Books/BookDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/ai',
      name: 'ai',
      component: AiRecommendView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/kluvtalk',
      name: 'kluvtalk-list',
      component: KluvTalkListView,
    },
    {
      path: '/kluvtalk/:id',
      name: 'kluvtalk-detail',
      component: KluvTalkDetailView,
      props: true,
    },
    {
      path: '/kluvtalk/create',
      name: 'kluvtalk-create',
      component: KluvTalkCreateView,
    },
    {
      path: '/kluvtalk',
      name: 'kluvtalk',
      component: KluvTalkListView,
    },
    {
      path: '/board',
      name: 'board',
      component: BoardListView,
    },
    {
      path: '/board/create',
      name: 'board-create',
      component: BoardCreateView,
    },
    {
      path: '/board/:id',
      name: 'board-detail',
      component: BoardDetailView,
      props: true
    },
    {
      path: '/books/:id',
      name: 'book-detail',
      component: BookDetailView,
      props: true,
    },
  ],
})

export default router
