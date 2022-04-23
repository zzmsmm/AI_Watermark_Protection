import request from '@/utils/request'

export function login(data) {
  return request({
    //url: '/vue-admin-template/user/login',
	url: 'http://127.0.0.1:8000/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    //url: '/vue-admin-template/user/info',
	url: 'http://127.0.0.1:8000/getinfo/',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}
