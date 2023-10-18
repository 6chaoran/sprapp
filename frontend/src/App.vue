<template>
  <v-app>
    <v-app-bar app :color="themeColor" image="/masthead.avif" density="default" rounded>
      <template v-slot:image>
        <v-img gradient="to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)"></v-img>
      </template>
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      </template>
      <v-app-bar-title style="flex:none;" :text = "title"><span class="subclass">{{ version }}</span> </v-app-bar-title>
      <v-spacer></v-spacer>
      <InputDialog :theme-color="themeColor"/>
      <LanguageMenu :theme-color="themeColor"/>
      
    </v-app-bar>

    <v-navigation-drawer app v-model = "drawer">
      <Sidebar :theme-color="themeColor"/>
    </v-navigation-drawer>
    
    <v-main>
      <Body />
    </v-main>
  </v-app>
</template>

<script setup>
import Body from '@/components/Body.vue';
import Sidebar from '@/components/Sidebar.vue';
import InputDialog from '@/components/InputDialog.vue';
import LanguageMenu from './components/LanguageMenu.vue';
import { ref, onMounted, computed } from 'vue';
import { fetchData } from '@/assets/js/apis';
import { useDisplay } from 'vuetify'
import { nextTick } from 'vue';

const themeColor = "teal-darken-4"
const { width, mobile } = useDisplay()
const title = computed( () => {
  return mobile.value ? 'SPR Profile Estimator' : 'Singapore PR Profile Estimator'})
const version = ref('  ');
const getTitle = () => {
  fetchData('/version').then( (d) => {
    version.value = "  " + d; 
  })
}
const drawer = ref(false) 
const lang = ref('raw')

onMounted(() => {
  getTitle();
  setTimeout(() => {
  // Code to modify the widget's z-index here
  const bmc = document.getElementById('bmc-wbtn');
  if (bmc) {
    bmc.style.zIndex = '0'; // Set the desired z-index
  }
}, 1000); 
})

</script>

<style>
.subclass {
  font-size: small;
}


</style>
