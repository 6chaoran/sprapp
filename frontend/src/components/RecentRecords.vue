<template>
<v-row>
      <v-col>
        <v-card v-for="(item, i) in records" class="my-3">
          <v-card-title>{{ item.username }}</v-card-title>
          <v-card-subtitle>{{ item.datetime }}</v-card-subtitle>
          <v-card-text>{{ item.description }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
</template>

<script>
export default {
    props: {
        records: Array,
    },
    data: () => ({
    })
}
</script>