export default class LocalStorageWorker {
    static getToken() {
        let token = localStorage.getItem('token')
        return token
    }
}