import router from './router'
import store from './store'
import { Message } from 'element-ui'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import { getToken } from '@/utils/auth' // get token from cookie
import getPageTitle from '@/utils/get-page-title'

import {permission} from '@/api/user.js'
NProgress.configure({ showSpinner: false }) // NProgress Configuration
//将注册页面加入白名单，才可以在未登录情况下访问
const whiteList = ['/login','/register', '/myinformation', '/proof/index', '/verify/index'] // no redirect whitelist

router.beforeEach(async(to, from, next) => {
  // start progress bar
  NProgress.start()

  // set page title
  document.title = getPageTitle(to.meta.title)

  // determine whether the user has logged in
  const hasToken = getToken()

  if (hasToken) {
    if (to.path === '/login') {
      // if is logged in, redirect to the home page
      next({ path: '/' })
      NProgress.done()
    } else {
	///*
      const hasGetUserInfo = store.getters.name
      if (hasGetUserInfo) {
        next()
      } 
	  //*/
	  /*
	  const hasRoles = store.getters.roles && store.getters.roles.length > 0
	  if (hasRoles) {
	    next()
	  }
	  */
	 else {
        try {
          // get user info
		  ///*
          await store.dispatch('user/getInfo')

          next()
		  //*/
		  /*
		  const { roles } = await store.dispatch('user/getInfo')
		  //根据roles动态生成路由表
		  const accessRoutes = await store.dispatch('permission/generateRoutes', roles)
		  
		  router.addRoutes(accessRoutes)
		  
		  next({ ...to, replace: true })
		  */
        } catch (error) {
          // remove token and go to login page to re-login
          await store.dispatch('user/resetToken')
          Message.error(error || 'Has Error')
          next(`/login?redirect=${to.path}`)
          NProgress.done()
        }
      }
    }
  } else {
    /* has no token*/

    if (whiteList.indexOf(to.path) !== -1) {
      // in the free login whitelist, go directly
      next()
    } else {
      // other pages that do not have permission to access are redirected to the login page.
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
