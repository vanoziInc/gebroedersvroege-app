<template>
  <v-app dark>
    <!-- NAVIGATION DRAWER -->
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
          <h4>brokeback sander</h4>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <!-- Normal Users navigation list -->
      <v-list>
        <v-list-group
          v-for="item in Items"
          :key="item.title"
          v-model="item.active"
          :prepend-icon="item.action"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"></v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item v-for="child in item.items" :key="child.title" :to="child.route">
            <v-list-item-content>
              <v-list-item-title v-text="child.title"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </v-list>
      <v-divider></v-divider>
      <!-- Admin navigation list -->
      <v-list v-if="userIsAdmin">
        <v-list-group
          v-for="item in adminItems"
          :key="item.title"
          v-model="item.active"
          :prepend-icon="item.action"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"></v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item v-for="child in item.items" :key="child.title" :to="child.route">
            <v-list-item-content>
              <v-list-item-title v-text="child.title"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>
    <!-- NAVIGATION BAR -->
    <v-app-bar :clipped-left="clipped" fixed app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <h3>{{ title }}</h3>
      <v-spacer />

      <!-- RIGHT SIDE MENU WHEN LOGGED IN -->
      <div v-if="this.$auth.loggedIn">
        <!-- LARGER VIEWPORTS -->
        <div v-if="$vuetify.breakpoint.mdAndUp">
          <v-btn small @click="logout">
            <v-icon class="mr-2">mdi-lock</v-icon>UITLOGGEN
          </v-btn>
        </div>
        <!-- SMALLER VIEWPORTS -->
        <div v-if="$vuetify.breakpoint.smAndDown">
          <v-btn icon @click="logout">
            <v-icon>mdi-lock</v-icon>
          </v-btn>
        </div>
      </div>

      <!-- RIGHT SIDE MENU WHEN NOTLOGGED IN -->
      <div v-else>
        <!-- LARGER VIEWPORTS -->
        <div v-if="$vuetify.breakpoint.mdAndUp">
          <v-btn small to="/auth/login">
            <v-icon class="mr-2">mdi-lock-open</v-icon>INLOGGEN
          </v-btn>
          <v-btn small class="ml-2" to="/auth/register">
            <v-icon class="mr-2">mdi-account-plus-outline</v-icon>REGISTREREN
          </v-btn>
        </div>
        <!-- SMALLER VIEWPORTS -->
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

    <!-- APPLICATIE MAIN WINDOW -->
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
      clipped: false,
      drawer: false,
      fixed: false,
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: "Gebr. Vroege",
      // Navigation drawer items
      Items: [
                        {
          action: "mdi-format-color-text",
          items: [{title : "Onderhoud", route:"/general_maintenance" }],
          title: "Algemeen",
        },
                {
          action: "mdi-cow",
          items: [{title : "Kalfjes" }],
          title: "Melkvee",
        },
                {
          action: "mdi-tractor",
          items: [{title : "Machines" }],
          title: "Loonbedrijf",
        },
      ],
      adminItems :[
                {
          action: "mdi-account-group-outline",
          items: [{title : "Uitnodigingen", route:"/admin/allowed_users" }],
          title: "Admin",
        },
      ]
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
@use "sass:math";
</style>
