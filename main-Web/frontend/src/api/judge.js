import request from '@/utils/request'

export function judge_upload(data) {
  return request({
    url: 'http://127.0.0.1:8000/judge_upload/',
    method: 'post',
    data
  })
}

export function judge_apply(data) {
  return request({
    url: 'http://127.0.0.1:8000/judge_apply/',
    method: 'post',
    data
  })
}

export function judge_list(token) {
  return request({
    url: 'http://127.0.0.1:8000/judge_list/',
    method: 'get',
    params: { token }
  })
}