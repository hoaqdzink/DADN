import axios from 'axios'
import LocalStorageWorker from "@/common/storageHelper";
class HTTPService {
  httpCommon(contentType, token = null) {
    const baseDomain = import.meta.env.VITE_APP_API_URL
    let headers = {
      "Content-Type": contentType
    }
    if (token) {
      headers.Authorization = `Bearer ${token}`
    }

    return axios.create({
      baseURL: baseDomain,
      headers: headers,
    })
  }
  async login(form) {
    let http = this.httpCommon("multipart/form-data")
    try {
      let response = await http.post('/login', form)
      return response
    } catch (e) {
      return e.response
    }
  }
  async add_motor_ctrl(value) {
    let token = LocalStorageWorker.getToken()
    let http = this.httpCommon("multipart/form-data", token)
    let form = { 'value': value }
    try {
      let response = await http.post('/add_motor_ctrl', form)
      return response
    } catch (e) {
      return e.response
    }
  }
  async add_mode(value) {
    let token = LocalStorageWorker.getToken()
    let http = this.httpCommon("multipart/form-data", token)
    let form = { 'value': value }
    try {
      let response = await http.post('/add_mode', form)
      return response
    } catch (e) {
      return e.response
    }
  }
  async stream() {
    let token = LocalStorageWorker.getToken()
    const response = await fetch('http://localhost:5000/stream', {
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    })
    return response
  }
}
export default new HTTPService()
