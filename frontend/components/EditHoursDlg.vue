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
        <v-toolbar-title class="text-body-2 font-weight-bold grey--text">
          {{ title }}
        </v-toolbar-title>
      </v-toolbar>
      <v-card-text class="pa-4 black--text">
        <v-form ref="hours_submission" v-model="valid">
          <v-text-field
            v-model="editedItem.hours"
            label="Uren"
            :rules="hoursRules"
          ></v-text-field>
          <v-text-field
            v-model="editedItem.description"
            label="Omschrijving"
          ></v-text-field></v-form
      ></v-card-text>
      <v-card-actions class="pt-3">
        <v-spacer></v-spacer>
        <v-btn
          color="warning"
          outlined
          class="body-2 font-weight-bold"
          @click.native="cancel"
          >Annuleer</v-btn
        >
        <v-btn
          :disabled="!valid"
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
export default {
  name: "EditHoursDlg",
  data() {
    return {
      hoursRules: [
        (v) => /^[+-]?\d+(\.\d+)?$/.test(v) || "Onjuiste invoer",
        (v) => v <= 24 || "Er zitten niet meer dan 24 uur in een dag",
      ],
      valid: false,
      dialog: false,
      editedItem: { hours: "", description: "" },
      title: null,
      options: {
        color: "grey lighten-3",
        width: 400,
        zIndex: 200,
      },
    };
  },

  methods: {
    open(title, editedItem, options) {
      this.title = title;
      this.options = Object.assign(this.options, options);
      if (editedItem.hours == 0 || editedItem.hours == null) {
        editedItem.hours = "";
      }
      this.editedItem = editedItem;
      this.dialog = true;

    },
    agree() {
      // Emit een event met als data editItem om zo de uren op te slaan
      if ((this.editedItem.hours == null) | (this.editedItem.hours == "")) {
        this.editedItem.hours = 0;
      }
      this.$emit("save", this.editedItem);
      this.dialog = false;
    },
    cancel() {
      this.reset();
      this.resetValidation();
      this.editedItem = { hours: "", description: "" },
      this.dialog = false;
    },
    validate() {
      this.$refs.hours_submission.validate();
    },
    reset() {
      this.$refs.hours_submission.reset();
    },
    resetValidation() {
      this.$refs.hours_submission.resetValidation();
    },
  },
};
</script>