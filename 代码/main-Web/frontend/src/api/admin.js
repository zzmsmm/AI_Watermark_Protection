import request from '@/utils/request'

export function getcount(token) {
  return request({
    url: 'http://127.0.0.1:8000/get_count/',
    method: 'get',
    params: { token }
  })
}
