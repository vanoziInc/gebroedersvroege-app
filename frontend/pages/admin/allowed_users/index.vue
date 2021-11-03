<template>
  <v-container>
    <v-data-table :headers="headers" :items="allowed_users">
      <!-- Toolbar template -->
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Uitnodigingen</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <!-- Card for inviting new users -->
           <v-dialog
          v-model="dialog"
          max-width="500px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="primary"
              dark
              class="mb-2"
              v-bind="attrs"
              v-on="on"
            >
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
                
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="blue darken-1"
                text
                @click="close"
              >
                Cancel
              </v-btn>
              <v-btn
                color="blue darken-1"
                text
                @click="save"
              >
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
          <v-spacer></v-spacer>
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
    </v-data-table></v-container
  >
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import moment from "moment";
export default {
  data() {
    return {
      dateFormat: "ddd DD/MM/YYYY",
      headers: [
        {
          text: "Uitgenodigd op",
          value: "created_at",
          formatter: (x) =>
            x ? moment(x).lang("nl").format(this.dateFormat) : null,
        },
        { text: "Email", value: "email" },
      ],
    };
  },
  methods: {
    ...mapActions({
      getAllowedUsers: "allowed_users/getAllowedUsers",
    }),
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