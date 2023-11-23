<template>
  <v-container class="px-0">
    <h1 v-if="!mobile">Navigate Your PR Journey with Confidence</h1>
    <QueryMatches :theme-color="themeColor"/>
    <v-btn :color="themeColor" class="mt-3" rounded @click="openInsightDialog">{{ $t('button.insight') }}</v-btn>
    <InsightDialog />
    <RecentRecords :records="records" :loading="loading" :theme-color="themeColor"/>
  </v-container>
</template>

<script setup>

import { $on,$emit } from 'vue-happy-bus'
import { fetchData } from '~/server/api';
import { useDisplay } from 'vuetify'
import InsightDialog from '~/components/Dialogs/InsightsDialog.vue';
const { logEventGA } = useAnalytics() // auto-imported
const { width, mobile } = useDisplay()

$on('edit-item', (editedItem) => {
  console.log(editedItem)
  records.value.unshift(editedItem)
})

$on('add-item', (editedItem) => {
  console.log(editedItem)
  records.value.unshift(editedItem)
})

const openInsightDialog = () => {
  $emit('open-insight-dialog')
  logEventGA('click_insight')
}

const themeColor = "teal-darken-4";

const records = ref([
  // {username: 'user', datetime: '2023-01-01', description: 'pass', applied_date:'2023-01-01', closed_date: '2023-09-01', status: 'rejected', update_ts: '2023-01-01'},
  // {username: 'user', datetime: '2023-01-01', description: 'pass', applied_date:'2023-01-01', closed_date: '2023-09-01', status: 'pass', update_ts: '2023-02-01'}
])

const loading = ref(false)

onMounted(async () => {
  loading.value = true
  records.value = await fetchData('/list_records');
  // console.log(records.value)
  loading.value = false
})
</script>
