<script setup>
import { ref, onMounted, computed } from 'vue';
import { useDisplay } from 'vuetify'
import { fetchData } from '~/server/api'
// import { analytics, logEvent } from './plugins/firebase';
// import { getAnalytics, logEvent } from "firebase/analytics";
const { locale, setLocale } = useI18n()

const themeColor = "teal-darken-4"
const { width, mobile } = useDisplay()

const title = computed(() => {
  if (locale.value === 'zh'){
      return mobile.value ? '新加坡PR申请评估' : '新加坡永居申请条件评估'
    }    
  return mobile.value ? 'SGPRProfiler' : 'SGPRProfiler: A Singapore PR Profile Evaluator'
})
const version = ref('  ');
const getTitle = () => {
  const resp = fetchData('/version')
  resp.then(d => version.value = "   " + d)
}
const drawer = ref(false)
const lang = ref('raw')

onMounted(() => {
  if (!mobile.value) {
    drawer.value = true
  }
  getTitle();
  setTimeout(() => {
    // Code to modify the widget's z-index here
    const bmc = document.getElementById('bmc-wbtn');
    bmc.nextSibling.remove();
    if (bmc) {
      bmc.style.zIndex = '0'; // Set the desired z-index
    }
  }, 100);
})

useSeoMeta({
  description: 'Explore recent applications submitted by peers and leverage our advanced AI models to evaluate and enhance your own application profile.',
  ogDescription: 'Explore recent applications submitted by peers and leverage our advanced AI models to evaluate and enhance your own application profile. ',
  ogTitle: 'SGPRProfiler: A Singapore PR Profile Evaluator',
  ogLocale: 'en_US',
  ogUrl: 'https://spr.ichaoran.com',
  ogType: 'website',
  ogImage: 'https://spr.ichaoran.com/masthead.avif',
  // twitterCard: 'summary_large_image',
  charset: 'utf-8',

})

useHead({
  title: 'SGPRProfiler: Navigate Your PR Journey with Confidence',
  htmlAttrs: { lang: 'en' },
  meta: [
    // { name: 'description', content:  },
    { name: 'msapplication-TileColor', content: '#ffffff' },
    { name: 'msapplication-TileImage', content: '/favicon/ms-icon-144x144.png' },
    { name: 'theme-color', content: '#ffffff' },
  ],
  bodyAttrs: {
    class: 'test'
  },

  link: [
    {rel: 'apple-touch-icon', sizes: "57x57", href:"/favicon/apple-icon-57x57.png"},
    {rel: 'apple-touch-icon', sizes: "60x60", href:"/favicon/apple-icon-60x60.png"},
    {rel: 'apple-touch-icon', sizes: "72x72", href:"/favicon/apple-icon-72x72.png"},
    {rel: 'apple-touch-icon', sizes: "76x76", href:"/favicon/apple-icon-76x76.png"},
    {rel: 'apple-touch-icon', sizes: "114x114", href:"/favicon/apple-icon-114x114.png"},
    {rel: 'apple-touch-icon', sizes: "120x120", href:"/favicon/apple-icon-120x120.png"},
    {rel: 'apple-touch-icon', sizes: "144x144", href:"/favicon/apple-icon-144x144.png"},
    {rel: 'apple-touch-icon', sizes: "152x152", href:"/favicon/apple-icon-152x152.png"},
    {rel: 'apple-touch-icon', sizes: "180x180", href:"/favicon/apple-icon-180x180.png"},
    {rel: 'icon', type: 'image/png', sizes: "192x192", href:"/favicon/android-icon-192x192.png"},
    {rel: 'icon', type: 'image/png', sizes: "32x32", href:"/favicon/favicon-32x32.png"},
    {rel: 'icon', type: 'image/png', sizes: "96x96", href:"/favicon/favicon-96x96.png"},
    {rel: 'icon', type: 'image/png', sizes: "16x16", href:"/favicon/favicon-16x16.png"},
    {rel: 'manifest', href: "/favicon/manifest.json"},
    { rel: 'canonical', href: 'https://spr.ichaoran.com/' }
  ],
  script: [{
    'data-name': "BMC-Widget",
    'data-cfasync': false,
    async: true,
    'src': 'https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js',
    'data-id': 'chaoran',
    'data-description': 'Support me on Buy me a coffee!',
    'data-message': '',
    'data-color': "#40DCA5",
    'data-position': "Top",
    'data-x_margin': "18",
    'data-y_margin': "18"} ]
})

</script>

<template>
  <v-app>
    <v-app-bar app :color="themeColor" image="/masthead.avif" 
      density="default" rounded>
      <template v-slot:image>
        <v-img alt="SGPRProfile-site-logo" 
               title="SGPRProfile-site-logo" 
               loading="lazy"
               gradient="to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)"></v-img>
      </template>
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      </template>
      <v-app-bar-title style="flex:none;" :text="title"><span class="subclass">{{ version }}</span> </v-app-bar-title>
      <v-spacer></v-spacer>
      <InputDialog :theme-color="themeColor" />
      <LanguageMenu :theme-color="themeColor" />
    </v-app-bar>

    <v-navigation-drawer app v-model="drawer">
      <Sidebar :theme-color="themeColor" />
    </v-navigation-drawer>

    <v-main>
      
      <v-container style="max-width: 1000px;">
        <MainBody />
      </v-container>
    </v-main>
  </v-app>
</template>

<style>
.subclass {
  font-size: small;
}
</style>
