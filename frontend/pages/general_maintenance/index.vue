<template>
  <v-container>
    <v-card>
      <v-toolbar flat>
        <v-toolbar-side-icon></v-toolbar-side-icon>
        <v-toolbar-title>Algemeen Onderhoud</v-toolbar-title>

        <v-spacer></v-spacer>
      </v-toolbar>

      <v-list two-line subheader>
        <v-subheader>{{ today }}</v-subheader>
        <p class="mx-4">
          <b>{{ general_maintenance.length }}</b> Taken
        </p>

        <v-form ref="form" class="mx-4">
          <v-text-field
            v-model="payload.description"
            label="Voer een nieuw onderhoudsitem in"
          />

          <v-btn
            color="primary"
            relative
            outlined
            @click="
              addGeneralMaintenance(payload); clearForm()
            "
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-form>
      </v-list>

      <v-list subheader two-line flat>
        <v-subheader class="subheading" v-if="general_maintenance.length == 0"
          >You have 0 Tasks, add some</v-subheader
        >
        <v-subheader class="subheading" v-if="general_maintenance.length == 1"
          >Your Tasks</v-subheader
        >

        <v-list-item-group>
          <v-list-item
            v-for="issue in general_maintenance"
            :key="issue.id"
            three-line
          >
            <template v-slot:default="{ active }">
              <v-list-item-action>
                <v-checkbox :input-value="active"></v-checkbox>
              </v-list-item-action>

              <v-list-item-content>
                <!-- <v-list-item-title>Notifications</v-list-item-title> -->
                <v-list-item-subtitle>{{
                  issue.description
                }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-btn
                fab
                ripple
                small
                color="red"
                v-if="active"
                @click="deleteGeneralMaintenance(issue.id)"
              >
                <v-icon class="white--text">mdi-close</v-icon>
              </v-btn>
            </template>
          </v-list-item>
          <!-- <v-list-item v-for="(issue, i) in general_maintenance">
                      <template #default="{ active, toggle }">
                        <v-list-item-action>

                          <v-checkbox v-model="active" @click="toggle"></v-checkbox>
                        </v-list-item-action>

                        <v-list-item-content>
                          <v-list-item-title :class="{
                  done: active
                  }">{{ general_maintenance.description | capitalize }}</v-list-item-title>
                          <v-list-item-subtitle>Added on: {{ date }}{{ ord }} {{ day }} {{ year }}</v-list-item-subtitle>
                        </v-list-item-content>
                        <v-btn fab ripple small color="red" v-if="active">
                          <v-icon class="white--text">mdi-close</v-icon>
                        </v-btn>
                      </template>
                    </v-list-item> -->
        </v-list-item-group>
      </v-list>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import moment from "moment";
export default {
  data() {
    return {
      payload: {
        description: "",
      },
      today: moment().lang("nl").format("ddd DD/MM/YYYY"),
      title: "Algemeen onderhoud",
    };
  },
  head() {
    return {
      title: this.title,
    };
  },
  methods: {
    ...mapActions({
      getAllGeneralMaintenance: "general_maintenance/getAllGeneralMaintenance",
      addGeneralMaintenance: "general_maintenance/addGeneralMaintenance",
      updateGeneralMaintenance: "general_maintenance/updateGeneralMaintenance",
      deleteGeneralMaintenance: "general_maintenance/deleteGeneralMaintenance",
    }),
      clearForm () {
     this.$refs.form.reset()
  }
  },
  computed: {
    // mix the getters into computed with object spread operator
    ...mapGetters({
      general_maintenance: "general_maintenance/GeneralMaintenance",
    }),
  },

  created() {
    this.getAllGeneralMaintenance();
  },
};
</script>

<style>
</style>