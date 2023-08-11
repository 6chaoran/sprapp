<template>
  <v-app>
    <v-app-bar app color="primary" dense dark>{{ title }}</v-app-bar>
    <v-main>
      <HelloWorld />
    </v-main>
  </v-app>
</template>

<script setup>
import HelloWorld from '@/components/HelloWorld.vue'
</script>

<script>
import { fetchData } from '@/assets/js/apis';
export default {
  data() {
    return {
      title: "null"
    }
  },
  methods: {
    async getTitle() {
      this.title = await fetchData('version')
    }
  },
  mounted() {
    this.getTitle()
  }
}
</script>
