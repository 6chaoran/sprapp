

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@invictus.codes/nuxt-vuetify',
    '@nuxtjs/i18n',
  ],
  i18n: {
    locales: ['en', 'zh', 'raw'], // set locale
    defaultLocale: 'raw',
    detectBrowserLanguage: false,
    strategy: "prefix",
    fallbackLocale: 'en', // set fallback locale
    // 👇 Reference the Vue I18n config file
    vueI18n: "./i18n.config.ts",
  },
  vuetify: {
    /* vuetify options */
    vuetifyOptions: {
      // @TODO: list all vuetify options
    },

    moduleOptions: {
      /* nuxt-vuetify module options */
      treeshaking: true,
      useIconCDN: true,

      /* vite-plugin-vuetify options */
      styles: true, /*true | 'none' | 'expose' | 'sass' | { configFile: string },*/
      autoImport: true, /*true | false,*/
      useVuetifyLabs: false, //true | false, 
    }
  },
  devServer: {
    port: 4000
  }
})
