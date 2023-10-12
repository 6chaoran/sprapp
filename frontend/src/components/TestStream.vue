<template>
<v-container>
    <v-row>{{ data }}</v-row>
    <v-row><v-btn rounded dark color="primary" @click="getData()">Test Stream</v-btn></v-row>
</v-container>
</template>

<script>
export default {
  data: () => ({
    data: ""
  }),
  methods: {
    async getData() {
      const response = await fetch("http://localhost:8000/stream_data");
      const reader = response.body.getReader();

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }

        this.data += new TextDecoder().decode(value);
        // this.$forceUpdate(); // Force Vue to update the DOM
      }
  }}
    
}
</script>