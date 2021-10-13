export default {
    GETUSERS(state, payload) {
        state.allUsers = payload
    },
    ADDUSER(state, payload) {
        state.allUsers.push(
            payload
        )
    }
}