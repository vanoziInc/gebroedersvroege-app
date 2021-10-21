
export default async ({store, redirect}) => {

    if (await store.state.auth.user) {
        return redirect('/')
    }
}