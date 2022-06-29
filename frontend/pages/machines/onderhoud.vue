<template>
    <v-container>
        <!-- Machine maintenance issue dialog -->
        <EditMachineMaintenanceIssueDlg ref="editMachineMaintenanceIssue" @save="save($event)"
            @saveEdit="saveEdit($event)" />
        <ConfirmDlg ref="confirm" />
        <!-- Tabel met de machines en opties om er 1 toe te voegen -->
        <section>
            <v-data-table :search="search" :headers="userIsAdmin ? headersAdmin : headers" :items="maintenance_issues"
                class="elevation-1">
                <!-- Toolbar met titel en knop om een nieuw onderhouds item toe te voegen -->
                <template v-slot:top>
                    <v-toolbar flat>
                        <v-toolbar-title>Storingen / onderhoud</v-toolbar-title>
                        <v-divider class="mx-4" inset vertical></v-divider>
                        <v-spacer></v-spacer>
                        <!-- Toevoegen en wijzigen dialoog: Only if user is admin -->
                        <v-btn></v-btn>
                    </v-toolbar>
                    <!-- Toolbar voor snel zoeken -->
                    <v-toolbar flat>
                        <v-text-field v-model="search" append-icon="mdi-magnify" label="Zoeken" single-line
                            hide-details>
                        </v-text-field>
                    </v-toolbar>
                </template>
                


                <!-- Item template om de created_at datum te formatteren -->
                <template v-slot:item.created_at="{ item }">
                    <span>{{ new Date(item.created_at).toLocaleDateString() }}</span>
                </template>
                <!-- Status translation -->
                <template v-slot:item.status="{ item }">
                    <span v-if="item.status == 0">Nieuw</span>
                    <span v-if="item.status == 1">In behandeling</span>
                    <span v-if="item.status == 2">Gesloten</span>
                </template>
                <!-- Actions column only if user is admin -->
                <template v-if="userIsAdmin" v-slot:[`item.actions`]="{ item }">
                    <v-icon small class="mr-2" @click="editMaintenanceIssue(item)">
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
                text: "Aangemaakt op",
                value: "created_at",
                sortable: true
            },
            {
                text: "Aangemaakt door",
                value: "created_by",
                sortable: true
            },
            {
                text: "Werknaam",
                value: "machine.work_name",
                sortable: true
            },
            {
                text: "Omschrijving",
                value: "issue_description",
                sortable: true,
            },
            {
                text: "Status",
                value: "status",
                sortable: true,
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
                text: "Aangemaakt op",
                value: "created_at",
                sortable: true
            },
            {
                text: "Aangemaakt door",
                value: "created_by",
                sortable: true
            },
            {
                text: "Werknaam",
                value: "machine.work_name",
                sortable: true
            },
            {
                text: "Omschrijving",
                value: "issue_description",
                sortable: true,
            },
        ],
    }),
    methods: {
        ...mapActions({
            getAllMachineMaintenanceIssues: "machine_maintenance/getAllMachineMaintenanceIssues",
            addMachineMaintenanceIssue: "machine_maintenance/addMachineMainetenanceIssue",
            updateMachineMaintenanceIssue: "machine_maintenance/updateMachineMainetenanceIssue",
            deleteMachineMaintenanceIssue: "machine_maintenance/deleteMachineMaintenanceIssue"
        }),
        async newMaintenanceIssue() {

        },
        save(maintenance_issue) {
            this.addMachineMaintenanceIssue(maintenance_issue)
        },
        saveEdit(maintenance_issue) {
            this.updateMachineMaintenanceIssue(maintenance_issue)
        },
        // Machine maintenace dialog
        async editMaintenanceIssue(issue) {
            if (await this.$refs.editMachineMaintenanceIssue.openEdit("Storing / Onderhoud aanpassen", issue)) {
            }
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
            maintenance_issues: "machine_maintenance/get_all_machine_maintenance_issues",
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
        this.getAllMachineMaintenanceIssues();
    }
};
</script>

<style>
</style>