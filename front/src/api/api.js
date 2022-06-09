import  request from 'request'

export function getEmailCode(email){
    return request(
        {
            url:'auth/emailCode?email='+email,
            method:'post'
        }
    )
}