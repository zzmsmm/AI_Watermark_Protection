import request from '@/utils/request'

export function certification_apply(data) {
  return request({
    url: 'http://127.0.0.1:8000/certification_apply/',
    method: 'post',
    data
  })
}

export function certification_list(token) {
  return request({
    url: 'http://127.0.0.1:8000/certification_list/',
    method: 'get',
    params: { token }
  })
}

export function unfinished_list(token) {
  return request({
    url: 'http://127.0.0.1:8000/unfinished_list/',
    method: 'get',
    params: { token }
  })
}

export function unfinished_detail(data) {
  return request({
    url: 'http://127.0.0.1:8000/unfinished_detail/',
    method: 'post',
    data
  })
}

export function finished_apply(data) {
  return request({
    url: 'http://127.0.0.1:8000/finished_apply/',
    method: 'post',
    data
  })
}
