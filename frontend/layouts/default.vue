<template>
  <v-app dark>
    <!-- NAVIGATION DRAWER -->

    <v-navigation-drawer
      v-if="this.$auth.loggedIn"
      v-model="drawer"
      :clipped="clipped"
      fixed
      app
      :width="325"
    >
      <v-list-item>
        <v-list-item-content>
          <h4>Gebr. Vroege</h4>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <!-- Normal Users navigation list -->
      <v-list v-if="!userIsAdmin">
        <!-- If one item then just an item -->
        <div
          v-for="(item) in Items"
          :key="item.title"
        >
          <div v-if="item.items">
            <v-list-group
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

              <v-list-item
                v-for="child in item.items"
                :key="child.title"
                :to="child.route"
                exact
              >
                <v-list-item-content>
                  <v-list-item-subtitle v-text="child.title"></v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list-group>
          </div>
          <div v-else>
            <v-list-item :to="item.route">
              <v-list-item-icon>
                <v-icon v-text="item.action"></v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="item.title"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </div>
        </div>

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

          <v-list-item
            v-for="child in item.items"
            :key="child.title"
            :to="child.route"
            exact
          >
            <v-list-item-content>
              <v-list-item-subtitle v-text="child.title"></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>
    <!-- NAVIGATION BAR -->
    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <h3>{{ title }}</h3>
      <v-spacer />

      <!-- RIGHT SIDE MENU WHEN LOGGED IN -->
      <div v-if="this.$auth.loggedIn">
        <!-- LARGER VIEWPORTS -->
        <div v-if="$vuetify.breakpoint.mdAndUp">
          <v-btn

            @click="logout"
            color="primary"
            outlined
          >
            <v-icon class="mr-2">mdi-lock</v-icon>UITLOGGEN
          </v-btn>
        </div>
        <!-- SMALLER VIEWPORTS -->
        <div v-if="$vuetify.breakpoint.smAndDown">
          <v-btn
            icon
            @click="logout"
          >
            <v-icon>mdi-lock</v-icon>
          </v-btn>
        </div>
      </div>

      <!-- RIGHT SIDE MENU WHEN NOTLOGGED IN -->
      <div v-else>
        <!-- LARGER VIEWPORTS -->
        <div v-if="$vuetify.breakpoint.mdAndUp">
          <v-btn
                        color="primary"
            outlined
            to="/auth/login"
          >
            <v-icon class="mr-2">mdi-lock-open</v-icon>INLOGGEN
          </v-btn>
          <v-btn
                        color="primary"
            outlined
            class="ml-2"
            to="/auth/register"
          >
            <v-icon class="mr-2">mdi-account-plus-outline</v-icon>REGISTREREN
          </v-btn>
        </div>
        <!-- SMALLER VIEWPORTS -->
        <div v-if="$vuetify.breakpoint.smAndDown">
          <v-btn
            icon
            to="/auth/login"
          >
            <v-icon>mdi-lock-open</v-icon>
          </v-btn>
          <v-btn
            icon
            to="/auth/register"
          >
            <v-icon>mdi-account-plus-outline</v-icon>
          </v-btn>
        </div>
      </div>
    </v-app-bar>

    <!-- APPLICATIE MAIN WINDOW -->
    <v-main>
      <!-- Confirmation Dialog -->

      <Snackbar></Snackbar>
      <nuxt />
    </v-main>
    <v-footer
      :absolute="!fixed"
      app
    >
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
      title: "Superleuk App",
      // Navigation drawer items
      Items: [
        // {
        //   action: "mdi-format-color-text",
        //   items: [{ title: "Onderhoud", route: "/general_maintenance" }],
        //   title: "Algemeen",
        // },
        {
          action: "mdi-view-dashboard-variant-outline",
          title: "Dashboard",
          route: "/"
        },
        {
          action: "mdi-account-clock-outline",
          items: [
            { title: "Overzicht", route: "/working_hours/overview" },
            { title: "Invoeren", route: "/working_hours/" },
            // { title: "Overzicht", route: "/working_hours/overview" },
          ],
          title: "Uren",
        },

        // {
        //   action: "mdi-cow",
        //   items: [{ title: "Kalfjes" }],
        //   title: "Melkvee",
        // },
        // {
        //   action: "mdi-tractor",
        //   items: [{ title: "Machines" }],
        //   title: "Loonbedrijf",
        // },
      ],
      adminItems: [
        {
          action: "mdi-account-group-outline",
          items: [{ title: "Uitnodigingen", route: "/admin/allowed_users" }],
          title: "Toegestane users",
        },
        {
          action: "mdi-account-clock-outline",
          items: [{ title: "Overzicht", route: "/admin/working_hours" }],
          title: "Uren",
        },
        {
          action: "mdi-account-multiple-outline",
          items: [{ title: "Overzicht", route: "/" }],
          title: "Medewerkers",
        },
      ],
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
