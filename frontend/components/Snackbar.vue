<template>
  <v-alert v-model="show" dismissible outlined text :color="color">{{
    message
  }}</v-alert>
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