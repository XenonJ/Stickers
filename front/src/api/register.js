import request from '@/utils/request'
// 用户注册api接口
export function register(code, data) {
  return request({
    url: 'auth/register?code=' + code,
    method: 'post',
    data
  })
}