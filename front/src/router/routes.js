
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: 'comment', component: () => import('pages/comment.vue') },
      { path: 'upload_word', component: () => import('pages/upload_word.vue') },
      { path: 'upload_picture', component: () => import('pages/upload_picture.vue') },
      { path: 'register', component: () => import('pages/register.vue') },
      { path: 'login', component: () => import('pages/login.vue') },
    ]
  },

  {
    path: '/111',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/myself.vue') }
    ]
  },

  {
    path: '/222',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/upload_word.vue') }
    ]
  },

  {
    path: '/333',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/others.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
