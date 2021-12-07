import state from "../allowed_users/state";

export default {
    Users: state => state.allUsers,
    Werknemers: state => {
        var werknemers = []
        for (const x of state.allUsers)

        {
            const role_names = Array.from(x.roles, x => x.name)
            if (role_names.includes('werknemer') && x.is_active ==true) {
                werknemers.push(x)
            }
        }
        return werknemers
    }

}