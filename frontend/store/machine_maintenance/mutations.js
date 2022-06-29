export default {
    GETMACHINEMAINTENANCEISSUES(state, payload) {
        state.machines_maintenance_issues = payload
    },
    ADDORUPDATEMACHINEMAINTENANCEISSUES: (state, payload) => {
        var foundIndex = state.machines_maintenance_issues.findIndex(p => p.id === payload.id)
        if (foundIndex !== -1) {
            state.machines_maintenance_issues.splice(foundIndex, 1, payload)
        } else {
            state.machines_maintenance_issues.push(payload)
        }
    },
    DELETEMACHINEMAINTENANCEISSUE(state, id) {
        var index = state.machines_maintenance_issues.findIndex(item => item.id == id);
        state.machines_maintenance_issues.splice(index, 1);
    },
}