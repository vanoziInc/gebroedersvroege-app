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
        <v-form v-model="valid">
          <v-text-field
            v-model="editedItem.hours"
            label="Uren"
            required
          ></v-text-field>
          <v-text-field
            v-model="editedItem.description"
            label="Omschrijving"
            required
          ></v-text-field></v-form
      ></v-card-text>
      <v-card-actions class="pt-3">
        <v-spacer></v-spacer>
        <v-btn
          v-if="!options.noconfirm"
          color="grey"
          text
          class="body-2 font-weight-bold"
          @click.native="cancel"
          >Annuleer</v-btn
        >
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
export default {
  name: "EditHoursDlg",
  data() {
    return {
      valid: false,
      dialog: false,
      resolve: null,
      reject: null,
      editedItem: { hours: "", description: "" },
      title: null,
      options: {
        color: "grey lighten-3",
        width: 400,
        zIndex: 200,
        noconfirm: false,
      },
    };
  },

  methods: {
    open(title, editedItem, options) {
      this.dialog = true;
      this.title = title;
      this.options = Object.assign(this.options, options);
      if (editedItem.hours == 0) {
        editedItem.hours = null;
      }
      this.editedItem = editedItem;
      return new Promise((resolve, reject) => {
        this.resolve = resolve;
        this.reject = reject;
      });
    },
    agree() {
      // Emit een event met als data editItem om zo de uren op te slaan
      console.log(this.editedItem)
      if (this.editedItem.hours == null | this.editedItem.hours == '') {
        this.editedItem.hours = 0;
      }
      this.$emit("save", this.editedItem);
      this.resolve(true);
      this.dialog = false;
    },
    cancel() {
      this.resolve(false);
      this.dialog = false;
    },
  },
};
</script>