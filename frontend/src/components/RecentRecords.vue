<template>
  <v-row class="mt-6">
    <v-col>
      Recent Records:
    </v-col>
  </v-row>
  <v-row>
    <v-col>
      <v-card v-for="data in records" :key="data.id" class="my-3" min-height="30px" elevation="2">
        <v-card-text>
          <v-row class="mx-1">
            {{ data.username }}
            <v-spacer></v-spacer>
            {{ data.datetime }} </v-row>

        </v-card-text>
        <v-card-text>{{ data.description }}</v-card-text>
        <v-card-text>
          <v-row class="px-3" align="center">
            {{ data.applied_date }} &nbsp; <v-icon>mdi-ray-start-arrow</v-icon>&nbsp; {{ data.status ==
              "pending" ? '' : data.closed_date }}
            <v-spacer></v-spacer>
            <v-chip :color="statusIconColor(data.status)" text-color="white">
              <v-avatar left v-if="data.status == 'pass'">
                <v-icon :color="statusIconColor(data.status)">mdi-checkbox-marked-circle</v-icon>
              </v-avatar>
              {{ data.status }}</v-chip></v-row>

        </v-card-text>

      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
const statusIconColor = (x) => {
  let colors = {
    pass: 'green',
    rejected: 'red'}
  return colors[x] ?? 'primary'
}
</script>

<script>
export default {
      props: {
      records: Array}
}
</script>