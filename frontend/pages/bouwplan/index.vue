<template>
  <v-container>
    <template>
      <v-card>
        <v-card-title> Bouwplan 2022 </v-card-title>
        <v-card-subtitle>
          <span><b>Upload datum: </b></span
          >{{ formatDateforTemplate(this.upload_date) }}
        </v-card-subtitle>
        <v-card-text>
          <v-row v-if="userIsAdmin">
            <v-col>
              <v-file-input
                v-model="files"
                accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                placeholder="Selecteer bouwplan excel"
                prepend-icon="mdi-microsoft-excel"
                outlined
                dense
              ></v-file-input>
              <v-btn
                :disabled="!this.fileSelected"
                color="primary"
                outlined
                @click="uploadBouwplan"
                >Uploaden</v-btn
              >
            </v-col>
          </v-row>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Zoeken"
            single-line
            hide-details
          ></v-text-field>
        </v-card-text>
        <v-data-table
          :headers="headers"
          :items="items"
          :search="search"
          :items-per-page="100"
          mobile-breakpoint="0"
          class="elevation-1"
        >
          <template v-slot:[`item.werknaam`]="{ item }">
            <a :href="item.link">{{ item.werknaam }}</a>
          </template></v-data-table
        ></v-card
      >
    </template></v-container
  >
</template>

<script>
import moment from "moment";
export default {
  data: () => ({
    title: "Bouwplan 2022",
    search: "",
    files: null,
    headers: [
      {
        text: "Perceel",
        align: "start",
        sortable: true,
        value: "perceel_nummer", align:"left" , width:"1%" 
        
      },
      { text: "Werknaam", sortable: true, value: "werknaam" , align:"left" , width:"1%" },
      //   { text: "Link", sortable: true, value: "boer en bunder link" },
      { text: "RVO ha", sortable: true, value: "ha" , align:"left" , width:"1%" },
      { text: "Gewas", sortable: true, value: "gewas" , align:"left" , width:"1%" },
      { text: "Mest", sortable: true, value: "mest" , align:"left" , width:"1%" },
      { text: "Opmerking", sortable: true, value: "opmerking", align:"left" , width:"1%" },
    ],
    upload_date: "",
    items: [],
  }),
  methods: {
    formatDateforTemplate(value) {
      return moment(value).locale("nl").format("dd DD MMM YYYY");
    },
    async bouwplan() {
      // Login API call
      try {
        let response = await this.$axios.get("/bouwplan/", {
          params: { year: 2022 },
        });
        this.items = response.data;
        this.upload_date = response.data.upload_date;
      } catch (err) {
        if (err.response) {
          this.$notifier.showMessage({
            content: err.response.data.detail,
            color: "error",
          });
        }
      }
    },
    async uploadBouwplan() {
      let formData = new FormData();
      console.log(this.files);
      formData.append("in_file", this.files);
      try {
        let response = await this.$axios.post("/bouwplan/upload", formData, {
          params: { year: 2022 },
        });
        this.$notifier.showMessage({
          content: "Bouwplan succesvol geupload",
          color: "success",
        });
        this.bouwplan();
        this.files = null;
      } catch (err) {
        if (err.response) {
          this.$notifier.showMessage({
            content: err.response.data.detail,
            color: "error",
          });
        }
      }
    },
  },
  computed: {
    userIsAdmin() {
      if (this.$auth.user.roles.filter((e) => e.name === "admin").length > 0) {
        return true;
      } else {
        return false;
      }
    },
    fileSelected() {
      if (this.files !== null) {
        return true;
      } else {
        return false;
      }
    },
  },

  created() {
    this.bouwplan();
  },
  head() {
    return {
      title: this.title,
    };
  },
};
</script>

<style>
</style>
