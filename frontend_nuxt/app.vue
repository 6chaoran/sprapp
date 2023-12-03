<script setup>
import { ref, onMounted, computed } from 'vue';
import { useDisplay } from 'vuetify'
import { fetchData } from '~/server/api'
// import { analytics, logEvent } from './plugins/firebase';
// import { getAnalytics, logEvent } from "firebase/analytics";
const { locale, setLocale } = useI18n()

const themeColor = "#00C16A" //"teal-darken-4"
const { width, mobile } = useDisplay()
const title = ref('SGPRProfiler')
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
    if (bmc) {
      bmc.nextSibling.remove();
      bmc.style.zIndex = '0'; // Set the desired z-index
    }
  }, 100);
  // setLocale('en');
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
    { rel: 'apple-touch-icon', sizes: "57x57", href: "/favicon/apple-icon-57x57.png" },
    { rel: 'apple-touch-icon', sizes: "60x60", href: "/favicon/apple-icon-60x60.png" },
    { rel: 'apple-touch-icon', sizes: "72x72", href: "/favicon/apple-icon-72x72.png" },
    { rel: 'apple-touch-icon', sizes: "76x76", href: "/favicon/apple-icon-76x76.png" },
    { rel: 'apple-touch-icon', sizes: "114x114", href: "/favicon/apple-icon-114x114.png" },
    { rel: 'apple-touch-icon', sizes: "120x120", href: "/favicon/apple-icon-120x120.png" },
    { rel: 'apple-touch-icon', sizes: "144x144", href: "/favicon/apple-icon-144x144.png" },
    { rel: 'apple-touch-icon', sizes: "152x152", href: "/favicon/apple-icon-152x152.png" },
    { rel: 'apple-touch-icon', sizes: "180x180", href: "/favicon/apple-icon-180x180.png" },
    { rel: 'icon', type: 'image/png', sizes: "192x192", href: "/favicon/android-icon-192x192.png" },
    { rel: 'icon', type: 'image/png', sizes: "32x32", href: "/favicon/favicon-32x32.png" },
    { rel: 'icon', type: 'image/png', sizes: "96x96", href: "/favicon/favicon-96x96.png" },
    { rel: 'icon', type: 'image/png', sizes: "16x16", href: "/favicon/favicon-16x16.png" },
    { rel: 'manifest', href: "/favicon/manifest.json" },
    { rel: 'canonical', href: 'https://spr.ichaoran.com/' }
  ],
  // script: [{
  //   'data-name': "BMC-Widget",
  //   'data-cfasync': false,
  //   async: true,
  //   'src': 'https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js',
  //   'data-id': 'chaoran',
  //   'data-description': 'Support me on Buy me a coffee!',
  //   'data-message': '',
  //   'data-color': "#40DCA5",
  //   'data-position': "Top",
  //   'data-x_margin': "18",
  //   'data-y_margin': "18"
  // }]
})

</script>

<template>
  <v-app >
    <v-app-bar :elevation=" mobile ? 1 : 0" color="rgba(255,255,255,0.9)">
      <v-app-bar-title 
        style="flex:none; color:#00C16A; font-weight:bolder;"
        class="text-h5"><a style="color:unset;text-decoration: unset;" href="/">{{ title }} 
          </a><v-chip density="compact" color="grey" class="mx-1 px-1"><p class="subclass">{{  version }}</p></v-chip>
      </v-app-bar-title>
      <v-spacer></v-spacer>
      <InputDialog :theme-color="themeColor" />
      <LanguageMenu :theme-color="themeColor" />
      <v-app-bar-nav-icon @click="drawer = !drawer" :size="mobile ? 'small' : 'default'"></v-app-bar-nav-icon>
    </v-app-bar>
    <v-main>

    <v-navigation-drawer  v-model="drawer" location="right" :floating="true" :temporary="true">
      <Sidebar :theme-color="themeColor"/>
    </v-navigation-drawer>
      <v-container style="max-width: 1200px;">
          <!-- <MainBody /> -->
          <NuxtPage />

      </v-container>
    </v-main>
    <v-footer app elevation="1" color="rgba(255, 255, 255, 0.9)">
      <FooterPage :theme-color="themeColor"/>
    </v-footer>
</v-app>
  
</template>

<style>
.subclass {
  font-size: small;
  color: gray;
}

.v-toolbar__content {
  margin-left: auto;
  max-width: 1200px;
  margin-right: auto;
}
</style>
