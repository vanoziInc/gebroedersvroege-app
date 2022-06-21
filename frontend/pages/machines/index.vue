<template>
  <v-container>
    <ConfirmDlg ref="confirm" />
    <!-- Tabel met de machines en opties om er 1 toe te voegen -->
    <section>
      <v-data-table :search="search" :headers="userIsAdmin ? headersAdmin : headers" :items="machines"
        class="elevation-1">
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Machinepark</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <!-- Toevoegen en wijzigen dialoog: Only if user is admin -->
            <v-dialog v-if="userIsAdmin" v-model="dialog" max-width="500px" @click:outside="close">
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                  Machine toevoegen
                </v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="text-h5" v-if="!machine_edited">Machine Toevoegen</span>
                  <span class="text-h5" v-if="machine_edited">Machine Aanpassen</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-form>
                      <v-text-field :readonly="machine_edited ? true : false" v-model="machine.work_number"
                        label="Werknummer"></v-text-field>
                      <v-text-field v-model="machine.work_name" label="Werknaam"></v-text-field>
                      <v-text-field v-model="machine.category" label="Categorie"></v-text-field>
                      <v-text-field v-model="machine.brand_name" label="Merk"></v-text-field>
                      <v-text-field v-model="machine.type_name" label="Type"></v-text-field>
                      <v-text-field v-model="machine.licence_number" label="Kenteken"></v-text-field>
                    </v-form>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="close">
                    Sluiten
                  </v-btn>
                  <v-btn color="blue darken-1" text @click="save"> Opslaan </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
          <v-toolbar flat>
            <v-text-field v-model="search" append-icon="mdi-magnify" label="Zoeken" single-line hide-details>
            </v-text-field>
          </v-toolbar>
        </template>

        <!-- Actions column only if user is admin -->
        <template v-if="userIsAdmin" v-slot:[`item.actions`]="{ item }">
          <v-icon small class="mr-2" @click="editItem(item)">
            mdi-pencil
          </v-icon>
          <v-icon small @click="deleteItem(item)">
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </section>
  </v-container>
</template>

<script>
import { mapGetters, mapActions, store } from "vuex";
export default {
  data: () => ({
    dialog: false,
    dialogDelete: false,
    machine_edited: false,
    machine: {},
    search: "",
    headersAdmin: [
      //   text: string,
      //   value: string,
      //   align?: 'start' | 'center' | 'end',
      //   sortable?: boolean,
      //   filterable?: boolean,
      //   groupable?: boolean,
      //   divider?: boolean,
      //   class?: string | string[],
      //   cellClass?: string | string[],
      //   width?: string | number,
      //   filter?: (value: any, search: string, item: any) => boolean,
      //   sort?: (a: any, b: any) => number
      {
        text: "Werknummer",
        value: "work_number",
        sortable: true
      },
      {
        text: "Werknaam",
        value: "work_name",
        sortable: true
      },
      {
        text: "Categorie",
        value: "category",
        sortable: true,

      },
      {
        text: "Merk",
        value: "brand_name",
        sortable: true,

      },
      {
        text: "Type",
        value: "type_name",
        sortable: true
      },
      {
        text: "Kenteken",
        value: "licence_number",
        sortable: true
      },
      { text: 'Acties', value: 'actions', sortable: false },
    ],
    headers: [
      //   text: string,
      //   value: string,
      //   align?: 'start' | 'center' | 'end',
      //   sortable?: boolean,
      //   filterable?: boolean,
      //   groupable?: boolean,
      //   divider?: boolean,
      //   class?: string | string[],
      //   cellClass?: string | string[],
      //   width?: string | number,
      //   filter?: (value: any, search: string, item: any) => boolean,
      //   sort?: (a: any, b: any) => number
      {
        text: "Werknummer",
        value: "work_number",
        sortable: true
      },
      {
        text: "Werknaam",
        value: "work_name",
        sortable: true
      },
      {
        text: "Categorie",
        value: "category",
        sortable: true,

      },
      {
        text: "Merk",
        value: "brand_name",
        sortable: true,

      },
      {
        text: "Type",
        value: "type_name",
        sortable: true
      },
      {
        text: "Kenteken",
        value: "licence_number",
        sortable: true
      }
    ],
  }),
  methods: {
    ...mapActions({
      getAllMachines: "machines/getAllMachines",
      addOrUpdateMachine: "machines/addOrUpdateMachine",
      deleteMachine: "machines/deleteMachine"
    }),
    close() {
      this.dialog = false;
      this.machine_edited = false,
        this.machine = {};
    },
    save() {
      this.addOrUpdateMachine(this.machine)
      this.machine_edited = false
      this.close();
    },
    editItem(item) {
      this.machine = Object.assign({}, item)
      this.machine_edited = true
      this.dialog = true
    },
    async deleteItem(item) {
      if (
        await this.$refs.confirm.open(
          "Bevestig",
          "Weet je zeker dat je de machine wilt verwijderen?"
        )
      ) {
        await this.deleteMachine(item.id)
      }
    }
  },
  computed: {
    // Getters from the store
    // mix the getters into computed with object spread operator
    ...mapGetters({
      machines: "machines/get_all_machines",
    }),
    userIsAdmin() {
      if (this.$auth.user.roles.filter((e) => e.name === "admin").length > 0) {
        return true;
      } else {
        return false;
      }
    },
  },

  mounted() {
    this.getAllMachines();
  }
};
</script>

<style>
</style>