export default function(context) {
    const roles = context.$auth.user.roles
    roles.forEach(element => {
        if (element['name']=='admin'){
            console.log('user has admin rights')
            return true;  
        }
        else {
            return false
        }
    });
}