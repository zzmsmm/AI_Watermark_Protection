import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/register',
    component: () => import('@/views/register/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },



  // 404 page must be placed at the end !!!
  //{ path: '*', redirect: '/404', hidden: true }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
    {
      path: '/',
      component: Layout,
      redirect: '/home/:list',
      children: [{
        path: 'home/:list',
        name: 'Home',
        component: () => import('@/views/home/index'),
        meta: { title: '个人主页', icon: 'user', activeMenu: '/home/:list', roles: ['user'] }
      }]
    },

    {
    path: '/certification',
    component: Layout,
    redirect: '/certification/apply',
    name: 'Certification',
    meta: { title: '模型注册', icon: 'el-icon-s-claim', roles: ['user'] },
    children: [
      {
        path: 'apply',
        name: 'Certification_apply',
        component: () => import('@/views/certification/index'),
        meta: { title: '申请', icon: 'el-icon-document', roles: ['user'] }
      },
      {
        path: 'list',
        name: 'Certification_list',
        component: () => import('@/views/certification_list/index'),
        meta: { title: '待完成', icon: 'list', activeMenu: '/certification/list', roles: ['user'] }
      },
      {
        path: 'detail/:id',
        name: 'Certification_detail',
        component: () => import('@/views/certification_detail/index'),
        meta: { title: '详情', icon: 'list', activeMenu: '/certification/list', roles: ['user'] },
        hidden: true
      },
    ]
  },

  {
    path: '/judge',
    component: Layout,
    children: [
      {
        path: 'apply/:hash/:type',
        name: 'Judge',
        component: () => import('@/views/judge/index'),
        meta: { title: '裁决申请', icon: 'el-icon-s-check', activeMenu: '/judge/apply/:hash/:type', roles: ['user'] }
      }
    ]
  },

  {
    path: 'external-link',
    component: Layout,
    children: [
      {
        path: 'https://github.com/zzmsmm/AI_Watermark_Protection',
        meta: { title: 'Github Link', icon: 'link', roles: ['user'] }
      }
    ]
  },

  {
    path: '/admin',
    component: Layout,
    children: [
      {
        path: 'home',
        name: 'Admin_home',
        component: () => import('@/views/admin/index'),
        meta: { title: '首页', icon: 'dashboard', activeMenu: '/admin/home', roles: ['admin'] }
      }
    ]
  },
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
