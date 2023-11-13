import { createI18n, useI18n } from 'vue-i18n'


import { messages } from '@/assets/js/translation'

const i18n = createI18n({
    legacy: true, // you must set `false`, to use Composition API
    locale: 'en', // set locale
    fallbackLocale: 'en', // set fallback locale
    messages, // set locale messages
    // If you need to specify other options, you can set other options
    // ...
  })

export { i18n } ;