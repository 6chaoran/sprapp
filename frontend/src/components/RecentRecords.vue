<template>

  <v-row class="mt-6">
    <v-col>
      {{ lang != 'zh' ? "Recent Records:" : "最近案例：" }}
    </v-col>
  </v-row>
  <v-row v-if = 'loading'> 
    <v-col>{{ lang != 'zh' ? "Loading records ..." : "加载记录。。。" }}  </v-col>
  </v-row>
  <v-row>
    <v-col>
      <v-card v-for="data in recordsFiltered" :key="data.id" class="my-3" min-height="30px" elevation="2">
        <v-card-text>
          <v-row class="mx-1">
            {{ data.username }}
            <v-spacer></v-spacer>
            {{ data.update_ts.replace('T', ' ') }} </v-row>

        </v-card-text>
        <v-card-text>{{ lang == "en" ? data.description_en : data.description }}</v-card-text>
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
import { $on } from 'vue-happy-bus'
import { ref } from 'vue'
import { computed } from 'vue';
const props = defineProps({
  records: Array,
  loading: Boolean
})
const statusIconColor = (x) => {
  let colors = {
    pass: 'green',
    rejected: 'red'}
  return colors[x] ?? 'primary'
}
const lang = ref('raw')
$on('lang', (data) => {
  lang.value = data
})

const recordsFiltered = computed(() => {
  if (lang.value == 'en'){
    return props.records.filter(elm => elm.description_en.length > 0 && elm.description != elm.description_en)
  } else {
    return props.records
  }
})
</script>

