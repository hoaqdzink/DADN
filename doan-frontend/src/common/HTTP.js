import axios from 'axios'
import LocalStorageWorker from "@/common/storageHelper";
class HTTPService {
  httpCommon(contentType) {
    const baseDomain = import.meta.env.VITE_APP_API_URL
    return axios.create({
      baseURL: baseDomain,
      headers: {
        "Content-Type": contentType,
      },
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
}

export default new HTTPService()
