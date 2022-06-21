export default {
    GETMACHINES(state, payload) {
        state.machines = payload
    },
    ADDORUPDATEMACHINE: (state, payload) => {
        var foundIndex = state.machines.findIndex(p => p.id === payload.id)
        if (foundIndex !== -1) {
            state.machines.splice(foundIndex, 1, payload)
        } else {
            state.machines.push(payload)
        }
    },
}