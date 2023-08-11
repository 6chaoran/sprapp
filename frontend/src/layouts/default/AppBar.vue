<template>
  <v-app-bar app color="primary" dense dark>{{ title }}</v-app-bar>
</template>

<script>
import { fetchData } from '@/assets/js/apis';
export default {
  data(){
    return{
      title: "null"
    }
  },
  methods: {
    async getTitle(){
      this.title = await fetchData('version')
    }
  },
  mounted(){
      this.getTitle()
  }
}
</script>
