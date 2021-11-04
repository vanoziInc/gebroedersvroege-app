export default function ({ store, redirect }) {
    if (store.state.auth.user.roles.filter((e) => e.name === "admin").length > 0) {
      return true;
    } else {
        return redirect('/');
    }
  }

