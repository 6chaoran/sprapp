<template>
  <v-app>
    <v-app-bar app color="teal-darken-4" image="https://picsum.photos/1920/1080?random" density="default" rounded>
      <template v-slot:image>
        <v-img gradient="to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)"></v-img>
      </template>
      <template v-slot:prepend>
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
      </template>

      <v-app-bar-title>{{ title }}<span class="subclass">{{ version }}</span>  </v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <HelloWorld />
    </v-main>
  </v-app>
</template>

<script setup>
import HelloWorld from '@/components/HelloWorld.vue';
import { ref, onMounted } from 'vue';
import { fetchData } from '@/assets/js/apis';
const title = "Singapore PR Profile Estimator";
const version = ref('  ');
const getTitle = () => {
  fetchData('version').then( (d) => {
    const parts = d.split(" "); 
    version.value = "  " + parts[3]; 
  })
}
onMounted(() => {
  getTitle();
})
</script>

<style>
.subclass {
  font-size: small;
}
</style>
