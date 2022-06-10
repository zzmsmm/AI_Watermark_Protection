import request from '@/utils/request'

export function login(data) {
  return request({
    url: 'http://127.0.0.1:8000/login/',
    method: 'post',
    data
  })
}

export function register(data) {
  return request({
    url: 'http://127.0.0.1:8000/register/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
	  url: 'http://127.0.0.1:8000/getinfo/',
    method: 'get',
    params: { token }
  })
}

export function changeAvatar(data) {
  return request({
    url: 'http://127.0.0.1:8000/changeavatar/',
    method: 'post',
    data
  })
}

export function logout() {
  return request({
    url: 'http://127.0.0.1:8000/logout/',
    method: 'post'
  })
}
