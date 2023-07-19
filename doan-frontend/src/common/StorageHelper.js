export default class LocalStorageWorker {
    static getToken() {
        let token = localStorage.getItem('token')
        return token
    }
    static setToken(token) {
        localStorage.setItem('token', token)
    }
}