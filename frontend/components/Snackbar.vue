<template>
  <v-snackbar
    v-model="show"
    dismissible
    outlined
    top
    text
    :color="color"
  >{{
    message
  }}
    <template v-slot:action="{ attrs }">
      <v-btn
        icon
        v-bind="attrs"
        @click="show = false"
      >
        <v-icon :color="color">
          mdi-close-circle-outline
        </v-icon>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      show: false,
      message: "",
      color: "",
    };
  },

  created() {
    this.$store.subscribe((mutation, state) => {
      if (mutation.type === "snackbar/showMessage") {
        this.message = state.snackbar.content;
        this.color = state.snackbar.color;
        this.show = true;
      }
      setTimeout(() => {
        this.show = false;
      }, 5000);
    });
  },
};
</script>