import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

export const constantRoutes = [{
		path: '/login',
		component: () => import('@/views/login/index'),
		hidden: true
	},

	{
		path: '/404',
		component: () => import('@/views/404'),
		hidden: true
	},

	{
		path: '/',
		component: Layout,
		redirect: '/myinformation',
		children: [{
			path: 'myinformation',
			name: 'Dashboard',
			component: () => import('@/views/dashboard/index'),
			meta: {
				title: '个人主页',
				icon: 'documentation'
			}
		}]
	},

	{
		path: '/proof',
		component: Layout,
		children: [{
			path: 'index',
			name: 'Proof',
			component: () => import('@/views/proof/index'),
			meta: {
				title: '证明平台',
				icon: 'form'
			}
		}],
    hidden: true
	},

	{
		path: '/verify',
		component: Layout,
		children: [{
			path: 'index',
			name: 'Verify',
			component: () => import('@/views/verify/index'),
			meta: {
				title: '数字识别平台',
				icon: 'search'
			}
		}]
	},

	{
		path: '*',
		redirect: '/404',
		hidden: true
	}
]

const createRouter = () => new Router({
	// mode: 'history', // require service support
	scrollBehavior: () => ({
		y: 0
	}),
	routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
	const newRouter = createRouter()
	router.matcher = newRouter.matcher // reset router
}

export default router
