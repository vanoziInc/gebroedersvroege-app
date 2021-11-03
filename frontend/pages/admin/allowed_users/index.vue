<template>
  <v-container>
    <v-data-table :headers="headers" :items="allowed_users" :search="search">
      <!-- Toolbar template -->
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Uitnodigingen</v-toolbar-title>

          <v-divider class="mx-4" inset vertical></v-divider>

          <v-spacer></v-spacer>
          <!-- Card for inviting new users -->
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                Nieuwe uitnodiging
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">Nieuwe uitnodiging</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col>
                      <v-text-field
                        v-model="payload.email"
                        label="Email adres"
                        :rules="emailRules"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">
                  Annuleer
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="
                    addAllowedUser(payload);
                    close();
                  "
                >
                  Verstuur
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
        <v-toolbar flat>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Zoeken"
            single-line
            hide-details
          ></v-text-field>
        </v-toolbar>
      </template>
      <!-- This template looks for headers with formatters and executes them -->
      <template
        v-for="header in headers.filter((header) =>
          header.hasOwnProperty('formatter')
        )"
        v-slot:[`item.${header.value}`]="{ header, value }"
      >
        {{ header.formatter(value) }}
      </template>
      <!-- Actions template -->
      <template v-slot:item.actions="{ item }">
        <v-icon @click="deleteAllowedUser(item.id)"> mdi-delete </v-icon>
      </template>
    </v-data-table></v-container
  >
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import moment from "moment";
export default {

  data() {
    return {
      title: "Uitnodigingen",
      search: "",
      dialog: false,
      dateFormat: "ddd DD/MM/YYYY",
      payload: {
        email: "",
        password: "",
      },
      emailRules: [
        (v) => !!v || "Dit veld is verplicht",
        (v) => /.+@.+\..+/.test(v) || "Dit is geen valide e-mail adres",
      ],
      headers: [
        {
          text: "Uitgenodigd op",
          value: "created_at",
          formatter: (x) =>
            x ? moment(x).lang("nl").format(this.dateFormat) : null,
        },
        { text: "Email", value: "email" },
        { text: "Acties", value: "actions", sortable: false },
      ],
    };
  },
  head() {
      return {
        title: this.title,}
        },
  methods: {
    ...mapActions({
      getAllowedUsers: "allowed_users/getAllowedUsers",
      addAllowedUser: "allowed_users/addAllowedUser",
      deleteAllowedUser: "allowed_users/deleteAllowedUser",
    }),
    close() {
      (this.payload.email = ""), (this.dialog = false);
    },
  },
  computed: {
    // mix the getters into computed with object spread operator
    ...mapGetters({
      allowed_users: "allowed_users/AllowedUsers",
    }),
  },
  created() {
    this.getAllowedUsers();
  },
};
</script>

<style>
</style>