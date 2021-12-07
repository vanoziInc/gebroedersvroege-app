<template>
  <v-data-table>
      
  </v-data-table>
</template>

<script>
export default {
 data: () => ({
         headers: [
      {
        text: "Week",
        value: "week_number",
        sortable: false,
      },
      {
        text: "Van",
        value: "start_of_week",
        sortable: false,
      },
            {
        text: "Tot",
        value: "end_of_week",
        sortable: false,
      },
      {
        text: "Totaal uren",
        value: "total_hours",
        sortable: false,
      },
      {
        text: "Ingediend?",
        value: "submitted",
        sortable: false,
      },
    ],
  }),
}
</script>

<style>

</style>