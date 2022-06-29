// https://techformist.com/reusable-confirmation-dialog-vuetify/

<template>
    <v-dialog v-model="dialog" :max-width="options.width" :style="{ zIndex: options.zIndex }" @keydown.esc="cancel">
        <v-card>
            <v-toolbar dark :color="options.color" dense flat>
                <v-toolbar-title class="text-body-2 font-weight-bold grey--text">
                    {{ title }}
                </v-toolbar-title>
            </v-toolbar>
            <v-card-text class="pa-4 black--text">
                <v-form ref="issue" v-model="valid">
                    <!-- Select machine if you create a new maintenance issue -->
                    <v-select v-if="!this.edit" :items="machines" v-model="maintenance_issue.machine_id" label="Machine"
                        item-value="id">
                        <template slot="selection" slot-scope="data">
                            <!-- HTML that describe how select should render selected items -->
                            {{ data.item.work_number }} - {{ data.item.work_name }}
                        </template>
                        <template slot="item" slot-scope="data">
                            <!-- HTML that describe how select should render items when the select is open -->
                            {{ data.item.work_number }} - {{ data.item.work_name }}
                        </template>
                    </v-select>
                    <!-- Show the machine if you edit a maintenance issue -->
                    <v-text-field readonly
                        :value="`${maintenance_issue.machine.work_number} - ${maintenance_issue.machine.work_name}`"
                        v-else></v-text-field>
                    <!-- Maintenance issue description , can be edited all the time -->
                    <v-text-field v-model="maintenance_issue.issue_description" label="Omschrijving"></v-text-field>
                    <!-- Change status option if you want to edit a maintenance issue -->
                    <v-select v-if="this.edit" :items="status_items" item-text="description" item-value="value"
                        label="Status" v-model="maintenance_issue.status">
                    </v-select>
                </v-form>
            </v-card-text>
            <v-card-actions class="pt-3">
                <v-spacer></v-spacer>
                <v-btn color="warning" outlined class="body-2 font-weight-bold" @click.native="cancel">Annuleer</v-btn>
                <v-btn v-if="!this.edit" color="primary" class="body-2 font-weight-bold" outlined @click.native="agree">
                    OK</v-btn>
                <v-btn v-if="this.edit" color="primary" class="body-2 font-weight-bold" outlined
                    @click.native="agreeEdit">OK</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
    name: "EditMachineMaintenanceIssueDlg",
    data() {
        return {
            valid: false,
            dialog: false,
            edit: false,
            maintenance_issue: {},
            select: {},
            title: "",
            options: {
                color: "grey lighten-3",
                width: 400,
                zIndex: 200,
            },
            status_items: [
                { value: 0, description: 'Nieuw' },
                { value: 1, description: 'In Behandeling' },
                { value: 2, description: 'Gesloten' },
            ]
        };
    },
    methods: {
        open(title, maintenance_issue, options) {
            this.title = title;
            this.options = Object.assign(this.options, options);
            this.maintenance_issue = Object.assign(this.maintenance_issue, maintenance_issue)
            this.dialog = true;
        },
        openEdit(title, maintenance_issue, options) {
            this.title = title;
            this.options = Object.assign(this.options, options);
            this.maintenance_issue = Object.assign(this.maintenance_issue, maintenance_issue)
            this.edit = true;
            this.dialog = true;
        },
        agree() {
            // Emit een event met als data editItem om zo de uren op te slaan
            if (!this.maintenance_issue.hasOwnProperty('status')) {
                this.maintenance_issue.status = 0;
            }
            this.$emit("save", this.maintenance_issue);
            this.dialog = false;
            this.$nuxt.$options.router.push('/machines/onderhoud/');
        },
        agreeEdit() {
            // Emit een event met als data editItem om zo de uren op te slaan
            if (!this.maintenance_issue.hasOwnProperty('status')) {
                this.maintenance_issue.status = 0;
            }
            this.maintenance_issue.machine_id = this.maintenance_issue.machine.id
            this.$emit("saveEdit", this.maintenance_issue);
            this.edit = !this.edit
            this.dialog = false;
        },
        cancel() {
            this.maintenance_issue = {};
            if(this.edit) {
                this.edit = false
            }
            this.dialog = false;
        },
        validate() {
            this.$refs.issue.validate();
        },
        reset() {
            this.$refs.issue.reset();
        },
        resetValidation() {
            this.$refs.issue.resetValidation();
        },
        ...mapActions({
            getAllMachines: "machines/getAllMachines",
        }),
    },
    computed: {
        ...mapGetters({
            machines: "machines/get_all_machines",
        }),
    },
    mounted() {
        this.getAllMachines();
    }

};
</script>