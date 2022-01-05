// https://techformist.com/reusable-confirmation-dialog-vuetify/

<template>
  <v-dialog
    v-model="dialog"
    :max-width="options.width"
    :style="{ zIndex: options.zIndex }"
    @keydown.esc="cancel"
  >
    <v-card>
      <v-toolbar dark :color="options.color" dense flat>
        <v-toolbar-title
          class="text-body-1 font-weight-bold grey--text text--darken-2"
        >
          Week: {{ week_number }} ({{ formatDateforTemplate(week_start) }}/{{
            formatDateforTemplate(week_end)
          }})
        </v-toolbar-title>
      </v-toolbar>
      <v-card-text class="pa-4 black--text">
        <v-simple-table>
          <thead>
            <tr>
              <th class="text-left">Datum</th>
              <th class="text-left">Uren</th>
              <th class="text-left">Omschrijving</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(x, i) in working_hours" :key="i">
              <td width="120px">{{ formatDateforTemplate(x.date) }}</td>
              <td width="80px ">{{ x.hours }}</td>
              <td>
                {{ x.description }}
              </td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-card-text>
      <v-card-actions class="pt-3">
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          class="body-2 font-weight-bold"
          outlined
          @click.native="agree"
          >OK</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import moment from "moment";
export default {
  name: "SubmittedWeekDlg",
  data() {
    return {
      resolve: null,
      dialog: false,
      options: {
        color: "grey lighten-3",
        width: 700,
        zIndex: 200,
        noconfirm: false,
      },
      week_number: null,
      week_start: null,
      week_end: null,
      working_hours: null,
    };
  },

  methods: {
    open(week_number, week_start, week_end, working_hours, options) {
      this.dialog = true;
      this.week_number = week_number;
      this.week_start = week_start;
      this.week_end = week_end;
      this.working_hours = working_hours;
      this.workingHoursSorted();
      this.options = Object.assign(this.options, options);
      return new Promise((resolve, reject) => {
        this.resolve = resolve;
        this.reject = reject;
      });
    },
    agree() {
      // Emit een event met als data editItem om zo de uren op te slaan
      this.resolve(true);
      this.dialog = false;
    },
    cancel() {
      this.resolve(false);
      this.dialog = false;
    },
    formatDateforTemplate(value) {
      return moment(value).locale("nl").format("dd DD MMM");
    },
    workingHoursSorted() {
      if (this.working_hours != null) {
        this.working_hours.sort(function (a, b) {
          console.log(a.date, b.date);
          console.log(a.date.localeCompare(b.date));
          return a.date.localeCompare(b.date);
        });
      } else {
        return false;
      }
    },
  },
  computed: {},
};
</script>