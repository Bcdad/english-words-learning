import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import signup from '../views/signup.vue'
import study from '../views/study.vue'
import user from '../views/user.vue'
import data from '@/views/data.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: signup
    },
    {
      path: '/study/:username',
      name: 'study',
      component: study
    },
    {
      path: '/user/:username',
      name: 'User',
      component: user
    },
    {
      path: '/data/:username',
      name: 'Data',
      component: data
    }
  ]
})

export default router
