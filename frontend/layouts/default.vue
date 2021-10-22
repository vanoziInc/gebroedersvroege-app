//       :permanent="$vuetify.breakpoint.mdAndUp"

<template>
  <v-app dark>
    <v-navigation-drawer
      v-if="this.$auth.loggedIn"
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      app
    >
      <v-list-item>
        <v-list-item-content>
          <h4>Gebr. Vroege (TEST)</h4>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>


<template v-slot:append>
        <div class="pa-2">
        <v-divider></v-divider>
      <v-list v-if="userIsAdmin">
        <v-list-item>
        <v-list-item-icon>
          <v-icon>mdi-crown-outline</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>Administratie</v-list-item-title>
        </v-list-item-content>
        </v-list-item>

      </v-list>
        </div>
      </template>
      <!--
      <v-list
        nav
        dense
      >
        <div
          v-for="(link, i) in links"
          :key="i"
        >

          <v-list-item
            v-if="!link.subLinks"
            :to="link.to"
            :active-class="color"
            class="v-list-item"
          >

          </v-list-item>

          <v-list-group
            v-else
            :key="link.text"
            no-action
            :value="false"
          >
            <template v-slot:activator>
              <h4 v-text="link.text"></h4>
            </template>
            <v-list-item
              v-for="sublink in link.subLinks"
              :to="sublink.to"
              :key="sublink.text"
            >
              <v-list-item-content>
                <h5 v-text="sublink.text"></h5>
              </v-list-item-content>
            </v-list-item>
          </v-list-group>
        </div>
      </v-list>
-->
    </v-navigation-drawer>
    <v-app-bar :clipped-left="clipped" fixed app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <h3>{{ title }}</h3>
      <v-spacer />
      <!-- Right side menu when logged in -->
      <div v-if="this.$auth.loggedIn">
        <!-- Larger viewports -->
        <div v-if="$vuetify.breakpoint.mdAndUp">
          <v-btn @click="logout">
            <v-icon class="mr-2">mdi-lock</v-icon> Sign Out
          </v-btn>
        </div>
        <!-- Mobile viewports -->
        <div v-if="$vuetify.breakpoint.smAndDown">
          <v-btn icon @click="logout">
            <v-icon>mdi-lock</v-icon>
          </v-btn>
        </div>
      </div>
      <!-- Right side menu when not logged in -->

      <div v-else>
        <!-- Larger viewports -->
        <div v-if="$vuetify.breakpoint.mdAndUp">
          <v-btn to="/auth/login">
            <v-icon class="mr-2">mdi-lock-open</v-icon> Sign in
          </v-btn>
          <v-btn class="ml-2" to="/auth/register">
            <v-icon class="mr-2">mdi-account-plus-outline</v-icon>Sign up
          </v-btn>
        </div>
        <!-- Mobile viewports -->
        <div v-if="$vuetify.breakpoint.smAndDown">
          <v-btn icon to="/auth/login">
            <v-icon>mdi-lock-open</v-icon>
          </v-btn>
          <v-btn icon to="/auth/register">
            <v-icon>mdi-account-plus-outline</v-icon>
          </v-btn>
        </div>
      </div>
    </v-app-bar>
    <v-main>
      <Snackbar></Snackbar>
      <nuxt />
    </v-main>
    <v-footer :absolute="!fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import Snackbar from "~/components/Snackbar.vue";

export default {
  components: { Snackbar },
  data() {
    return {
      color: "grey lighten-5",
      clipped: false,
      drawer: false,
      fixed: false,
      // links: [
      //   {
      //     icon: "mdi-cake-variant-outline",
      //     text: "Kalveren",
      //     subLinks: [
      //       {
      //         text: "Vlees kalveren",
      //         to: "/calves/vleeskalveren",
      //       },
      //       {
      //         text: "Geboortes",
      //         to: "/calves/births",
      //       },
      //     ],
      //   },
      // ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: "Gebr. Vroege",
    };
  },
  methods: {
    async logout() {
      await this.$auth.logout();
      this.$router.push("/auth/login");
    },
  },
  computed: {
    userIsAdmin() {
      if (this.$auth.user.roles.filter((e) => e.name === "admin").length > 0) {
        return true;
      } else {
        return false;
      }
    },
  },
};
</script>

<style>
@use 'sass:math';
</style>