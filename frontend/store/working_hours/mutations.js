export default {
    GETALLOWEDUSERS(state, payload) {
        state.allAllowedUsers = payload
    },
    ADDALLOWEDUSER(state, payload) {
        state.allAllowedUsers.push(
            payload
        )
    },
    DELETEALLOWEDUSER(state, payload) {
        var index = state.allAllowedUsers.findIndex(allowedUser => allowedUser.id == payload.id);
        state.allAllowedUsers.splice(index, 1);
        console.log(state.allAllowedUsers)
    }
}