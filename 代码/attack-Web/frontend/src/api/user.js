import request from '@/utils/request'

//登录
export function login(data) {
  return request({
    //url: '/vue-admin-template/user/login',
    url: 'http://127.0.0.1:8001/login/',
    method: 'post',
    data
  })
}

//登出
export function logout() {
  return request({
    url: 'http://127.0.0.1:8001/logout/',
    method: 'post'
  })
}


export function Download() {
  return request({
    url: 'http://127.0.0.1:8001/download/',
    method: 'get',
    params:{}
  })
}

export function permission() {
	return request({
		url: 'http://127.0.0.1:8001/permission/',
		method: 'get',
		params:{}
	})
}

export function upload(data) {
	return request({
		url: 'http://127.0.0.1:8001/upload/',
		method: 'post',
		data
	})
}

export function getinfo() {
	return request({
		url: 'http://127.0.0.1:8001/getinfo/',
		method: 'get',
		params:{}
	})
}