export default {
    GETWORKINGHOURS(state, payload) {
        state.working_hours = payload
    },
    GETWORKINGHOURSALLUSERS(state, {user, payload}) {
        state.working_hours_all_users.push({user :user, working_hours:payload })
    },
    ADDWORKINGHOURS(state, payload) {
        state.working_hours.push(
            payload
        )
    },

    ADDORUPDATEWORKINGHOURS: (state, payload) => {
        const working_hours_item = state.working_hours.find(p => p.id === payload.id)
        if (working_hours_item == null) {
            state.working_hours.push(
                payload
            )
        }
        else {
            working_hours_item.hours = payload.hours
            working_hours_item.submitted = payload.submitted
            working_hours_item.description = payload.description
        }
    },

    DELETEWORKINGHOURS(state, id) {
        var index = state.working_hours.findIndex(item => item.id == id);
        state.working_hours.splice(index, 1);
    },
    RESETALLWORKINGHOURSALLUSERS(state) {
        state.working_hours_all_users = []
    }
}