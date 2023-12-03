

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: true,
  devtools: { enabled: true },
  modules: [
    '@invictus.codes/nuxt-vuetify',
    '@nuxtjs/i18n',
    'nuxt-simple-sitemap'
  ],
  i18n: {
    locales: [{
      code: 'en',
      iso: 'en-US'
    }, {
      code: 'zh',
      iso: 'zh-SG'
    }], // set locale
    defaultLocale: 'en',
    detectBrowserLanguage: false,
    strategy: "prefix_except_default",
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
  sitemap: {

  },
  site: {
    url: 'https://spr.ichaoran.com'
    // url: 'http://localhost:4000'
  },
  runtimeConfig: {
    public: {
      gtagId: "G-FG3L7LZ5CN",
    }
  },
  devServer: {
    port: 4000
  }
})
