<template>
  <v-container>
    <InputMessage @data="sendMessage" />
    <Spinner v-if="showSpinner" spinnerMessage="Query In Process ..." :themeColor="themeColor" />
    <div v-if="showOutput">
      <QueryOutput :matches="matches" :resultStyle="resultStyle" :prediction="prediction" :color="themeColor" />
      <Dialog class="mb-3" :theme-color="themeColor" 
        button-text="add my record" card-text="Add Record" formType="add" :desc="msg" 
        @edited-item="addItem" />
    </div>
    <Dialog :theme-color="themeColor" button-text="Edit my record" 
     card-text="Edit Record" formType="edit" desc="" @edited-item="addItem"/>
    <RecentRecords :records="records" />
  </v-container>
</template>

<script setup>
import InputMessage from './InputMessage.vue';
import RecentRecords from './RecentRecords.vue';
import Spinner from './Spinner.vue';
import QueryOutput from './QueryOutput.vue';
import Dialog from './Dialog.vue';
import { ref, computed } from 'vue';
import { fetchData, postData } from '@/assets/js/apis'
import { onMounted } from 'vue';

const themeColor = "teal-darken-4";
const prediction = ref({
  // decision: "pass",
  // odds: 0.8,
  // duration: 118,
});
const msg = ref('');
const showSpinner = ref(false);
const showOutput = ref(false);
const records = ref([
  // {username: 'user', datetime: '2023-01-01', description: 'pass', applied_date:'2023-01-01', closed_date: '2023-09-01', status: 'rejected'},
  // {username: 'user', datetime: '2023-01-01', description: 'pass', applied_date:'2023-01-01', closed_date: '2023-09-01', status: 'pass'}

]);
const matches = ref([
  { 'desc': 1, 'result': 'pass', 'duration': 123, 'update_time': '2023-01-01', 'desc_en': 'eng' },
  { 'desc': 2, 'result': 'rejected', 'duration': 234, 'update_time': '2023-02-01', 'desc_en': 'eng' }
]);
const sendMessage = async (message) => {
  showOutput.value = false;
  showSpinner.value = true;
  msg.value = message;
  console.log(msg.value)
  const resp = await postData('get_matches', { text: message })
  showSpinner.value = false
  showOutput.value = true
  matches.value = resp.matches;
  prediction.value.decision = resp.pred_decision;
  prediction.value.odds = resp.odds;
  prediction.value.duration = resp.pred_duration;
  console.log(resp);
};

const addItem = (editedItem) => {
  records.value.unshift(editedItem)
}

const resultStyle = computed(() => {
  return prediction.value.decision === 'pass' ? 'text-green' : 'text-red';
});

onMounted(async () => {
  records.value = await fetchData('api/v1/list_records');
});

</script>
<style>
.progress-container {
  display: flex;
  align-items: center;
  height: 25px;
}

.progress-text {
  margin-left: 20px;
}
</style>