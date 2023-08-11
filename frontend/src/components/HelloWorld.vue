<template>
  <v-container>
    <InputMessage @data="sendMessage" />
    <Spinner v-if="showSpinner" spinnerMessage="Query In Process ..." />
    <QueryOutput v-if="showOutput"   :matches="matches" :resultStyle="resultStyle" :prediction="prediction"/>
    <RecentRecords :records="records" />
  </v-container>
</template>

<script setup>
import InputMessage from './InputMessage.vue';
import RecentRecords from './RecentRecords.vue';
import Spinner from './Spinner.vue';
import QueryOutput from './QueryOutput.vue';

</script>

<script>
import { fetchData, postData } from '@/assets/js/apis'
export default {
  data: () => ({
    prediction: {
      decision: "pass",
      odds: 0.8,
      duration: 118,
    },
    showSpinner: false,
    showOutput: false,
    records: [],
    matches: [
                        // { 'desc': 1, 'result': 'pass', 'duration': 123, 'update_time': '2023-01-01', 'desc_en': 'eng' },
                        // { 'desc': 2, 'result': 'rejected', 'duration': 234, 'update_time': '2023-02-01', 'desc_en': 'eng' }
                    ],
  }),
  methods: {
    async sendMessage(message) {
      this.showOutput=false
      this.showSpinner = true
      console.log(message)
      // this.records = await fetchData('list_records')
      const matches = await postData('get_matches', {text: message})
      this.showSpinner = false
      this.showOutput=true
      console.log(matches.matches)
      this.matches = matches.matches
    }
  },
  computed: {
    resultStyle() {
      return this.prediction.decision === 'pass' ? 'text-green' : 'text-red';
    },
  }
}
</script>
<style>
.text-green {
  color: green;
}

.text-red {
  color: red;
}

.progress-container {
  display: flex;
  align-items: center;
  /* Align items vertically */
  height: 25px;
  /* Adjust the height as needed */
}

.progress-text {
  margin-left: 10px;
  /* Adjust the spacing between the circular progress and the text */
}
</style>