<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <v-card>
        <v-card-title class="headline">
          Auth Practice
        
        </v-card-title>
        <v-card-text>
          Auh User : {{ this.$store.state.auth.user }} <br>
          tokens : {{this.$auth.user}}


        </v-card-text>
        <v-card-actions>
          <v-btn
            color="primary"
            @click="refresh()"
          >
            Refresh tokens
          </v-btn>
          <v-btn @click="addOne">Add 1</v-btn>
          <v-btn @click="getUsers">Get Users</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
export default {
  data() {
    return {
      login: {
        username: 'test@test.com',
        password: 'test123$%'
      },
    }
  },
  methods: {
    ...mapActions({
      getUsers: 'users/getUsers'
    }),
    async userLogin() {
      const form = new FormData()
        form.append("username", this.login.username)
        form.append("password", this.login.password)
      try {
        let response = await this.$auth.loginWith('local', { data: form })
      } catch (err) {
        console.log(err.response)
      }
    },
    
    addOne() {
      this.$store.commit('todos/increment')
    },

    refresh() {
this.$auth.refreshTokens()
    }
  },
  computed: {
// mix the getters into computed with object spread operator
  ...mapGetters({
    users :'users/Users'
  })
  }
}
</script>