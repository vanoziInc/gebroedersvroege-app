export default {
    GETGENERALMAINTENANCE(state, payload) {
        state.generalMaintenace = payload
    },
    ADDGENERALMAINTENANCE(state, payload) {
        state.generalMaintenace.push(
            payload
        )
    },
    UPDATEGENERALMAINTENANCE: (state, payload) => {
        const generalMaintenance = state.generalMaintenace.find(p => p.id === payload.id)
        generalMaintenance.description = payload.description
      },
      DELETEGENERALMAINTENANCE(state, payload) {
        var index = state.generalMaintenace.findIndex(item => item.id == payload.id);
        state.generalMaintenace.splice(index, 1);
    }
}