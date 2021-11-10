// https://codepen.io/Jayesh_v/pen/wvgjMva

<template>
  <v-container>
    <v-card >
      <v-card-title class="mb-4"> <span><h5 class="font-weight-medium">
Uren overzicht week {{ computedSelectedWeek }}
      </h5>
        
        </span> </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="datesOfCurrentWeek"
          fixed-header
          hide-default-footer
        >
          <v-divider inset></v-divider>
          <template v-slot:top>
            <v-toolbar flat>
              <div>
                <!-- TODO Week nummer maannummer-->
                <v-menu
                  v-model="menu2"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="computedDateFormattedMomentjs"
                      label="Kies een datum"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="date"
                    @input="menu2 = false"
                    locale="nl"
                  ></v-date-picker>
                </v-menu>
              </div>
              <v-spacer></v-spacer>
            </v-toolbar>
          </template>
          <template v-slot:[`item.name`]="{ item }">
            <v-text-field
              v-model="editedItem.name"
              :hide-details="true"
              dense
              single-line
              v-if="item.id === editedItem.id"
            ></v-text-field>
            <span v-else>{{ item.name }}</span>
          </template>
          <template v-slot:[`item.calories`]="{ item }">
            <v-text-field
              v-model="editedItem.calories"
              :hide-details="true"
              dense
              single-line
              v-if="item.id === editedItem.id"
            ></v-text-field>
            <span v-else>{{ item.calories }}</span>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <div v-if="item.id === editedItem.id">
              <v-icon color="red" class="mr-3" @click="close">
                mdi-window-close
              </v-icon>
              <v-icon color="green" @click="save"> mdi-content-save </v-icon>
            </div>
            <div v-else>
              <v-icon color="green" class="mr-3" @click="editItem(item)">
                mdi-pencil
              </v-icon>
              <v-icon color="red" @click="deleteItem(item)">
                mdi-delete
              </v-icon>
            </div>
          </template>
          <template v-slot:no-data>
            <v-btn color="primary" @click="initialize">Reset</v-btn>
          </template>
        </v-data-table>
      </v-card-text>
      <v-card-actions>
        <div>
          <v-btn icon @click="substractWeek"
            ><v-icon>mdi-chevron-left</v-icon></v-btn
          >
          <b>{{ computedSelectedWeek }}</b>
          <v-btn icon @click="addWeek"
            ><v-icon>mdi-chevron-right</v-icon></v-btn
          >
        </div>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import moment from "moment";
export default {
  data: () => ({
    date: moment().format("YYYY-MM-DD"),
    menu2: false,
    search: "",
    headers: [
      {
        text: "Datum",
        value: "datum",
        sortable: false,
      },
            {
        text: "Uren",
        value: "datum",
        sortable: false,
      },
            {
        text: "Omschrijving",
        value: "datum",
        sortable: false,
      },
                  {
        text: "Acties",
        value: "datum",
        sortable: false,
      },
    ],
    desserts: [],
    editedIndex: -1,
    editedItem: {
      id: 0,
      name: "",
      calories: 0,
    },
    defaultItem: {
      id: 0,
      name: "New Item",
      calories: 0,
    },
  }),
  methods: {
    editItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
    },

    deleteItem(item) {
      const index = this.desserts.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.desserts.splice(index, 1);
    },

    close() {
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },
    addNew() {
      const addObj = Object.assign({}, this.defaultItem);
      addObj.id = this.desserts.length + 1;
      this.desserts.unshift(addObj);
    },
    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem);
      }
      this.close();
    },
    substractWeek() {
      this.date = moment(this.date).subtract(7, "days").format("YYYY-MM-DD");
    },
    addWeek() {
      this.date = moment(this.date).add(7, "days").format("YYYY-MM-DD");
    },
  },

  computed: {
    computedDateFormattedMomentjs() {
      return this.date
        ? moment(this.date).lang("nl").format("dd, D MMMM YYYY")
        : "";
    },
    computedSelectedWeek() {
      return this.date ? moment(this.date).week() : "";
    },
    computedFirstDayCurrentWeek() {
      return moment(this.date).startOf("isoweek");
    },
    computedLastDayCurrentWeek() {
      return moment(this.computedFirstDayCurrentWeek)
        .add(7, "days")
        .startOf("isoweek");
    },
    datesOfCurrentWeek() {
      var now = this.computedFirstDayCurrentWeek.clone(),
        dates = [];

      while (now.isBefore(this.computedLastDayCurrentWeek)) {
        dates.push({ datum: now.lang("nl").format("dd, DD-MM") });
        now.add(1, "days");
      }
      return dates;
    },
  },
};
</script>