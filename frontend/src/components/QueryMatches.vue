<template>
    <InputMessage @data="sendMessage" />
    <Spinner v-if="showSpinner" :spinnerMessage="$t('query.progress')" :themeColor="themeColor" />
    <div v-if="showOutput">
        <QueryOutput :matches="matches" :resultStyle="resultStyle" :prediction="prediction" :color="themeColor" />
        <Dialog class="mb-3" :theme-color="themeColor" :button-text="$t('button.add')" :card-text="$t('button.add')" formType="add"
            :desc="msg" />
    </div>
</template>

<script setup>
import InputMessage from './InputMessage.vue';
import Spinner from './Spinner.vue';
import QueryOutput from './QueryOutput.vue';
import Dialog from './Dialog.vue';
import { ref, computed, onBeforeMount } from 'vue';
import { fetchData, postData } from '@/assets/js/apis'

const props = defineProps({
    themeColor: String,
})
const showSpinner = ref(false);
const showOutput = ref(false);
const matches = ref([
  { 'description': 1, 'status': 'pass', 'duration': 123, 'update_ts': '2023-01-01', 'description_en': 'eng' },
]);
const prediction = ref({
  // decision: "pass",
  // odds: 0.8,
  // duration: 118,
});
const msg = ref('');

const sendMessage = async (message) => {
  showOutput.value = false;
  showSpinner.value = true;
  msg.value = message;
  // console.log(msg.value)
  const resp = await fetchData('/get_matches', { text: message })
  showSpinner.value = false
  showOutput.value = true
  matches.value = resp.matches;
  prediction.value.decision = resp.pred_decision;
  prediction.value.odds = resp.odds;
  prediction.value.duration = resp.pred_duration;
  // console.log(resp);
};
const resultStyle = computed(() => {
  return prediction.value.decision === 'pass' ? 'text-green' : 'text-red';
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