<template>
  <v-container>
    <QueryMatches :theme-color="themeColor"/>
    <RecentRecords :records="records" :loading="loading" :theme-color="themeColor"/>
  </v-container>
</template>

<script setup>
import RecentRecords from './RecentRecords.vue';
import QueryMatches from './QueryMatches.vue';
import { ref } from 'vue';
import { fetchData } from '@/assets/js/apis'
import { onMounted } from 'vue';
import { $on } from 'vue-happy-bus'

$on('edit-item', (editedItem) => {
  console.log(editedItem)
  records.value.unshift(editedItem)
})

$on('add-item', (editedItem) => {
  console.log(editedItem)
  records.value.unshift(editedItem)
})

const themeColor = "teal-darken-4";

const records = ref([
  // {username: 'user', datetime: '2023-01-01', description: 'pass', applied_date:'2023-01-01', closed_date: '2023-09-01', status: 'rejected'},
  // {username: 'user', datetime: '2023-01-01', description: 'pass', applied_date:'2023-01-01', closed_date: '2023-09-01', status: 'pass'}
])

const loading = ref(false)

onMounted(async () => {
  loading.value = true
  records.value = await fetchData('/list_records');
  // console.log(records.value)
  loading.value = false
})
</script>
