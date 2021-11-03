export default {
    GETALLOWEDUSERS(state, payload) {
        state.allAllowedUsers = payload
    },
    ADDALLOWEDUSER(state, payload) {
        state.allAllowedUsers.push(
            payload
        )
    }
}