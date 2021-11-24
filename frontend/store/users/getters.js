import state from "../allowed_users/state";

export default {
    Users: state => state.allUsers,
    nonAdminUsers: state => {
        for (const x of state.allUsers)
        {
            console.log(x)
            const roles = Array.from(x, x => x.roles)
            const role_names = Array.from(roles, x => x.name)
            console.log(roles)
        }
    }

}