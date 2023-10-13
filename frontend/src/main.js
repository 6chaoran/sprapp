/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'
import { useI18n } from 'vue-i18n'


// const app = createApp(App)
const app = createApp(App, {
    setup() {
        const { t } = useI18n() // call `useI18n`, and spread `t` from  `useI18n` returning
        return { t } // return render context that included `t`
      }
})
registerPlugins(app)
app.mount('#app')
