export default function ({ store, redirect }) {
    const roles = store.state.auth.user.roles
    roles.forEach(element => {
        if (element['name'] == 'admin') {
            return true;
        }
    }
    );
    return redirect('/')
}