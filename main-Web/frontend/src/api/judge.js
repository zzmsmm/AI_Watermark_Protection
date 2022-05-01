import request from '@/utils/request'

export function judge_apply(data) {
  return request({
    url: 'http://127.0.0.1:8000/judge_apply/',
    method: 'post',
    data
  })
}

