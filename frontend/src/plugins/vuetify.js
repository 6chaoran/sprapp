/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'

// Composables
import { createVuetify } from 'vuetify'

// Dates
import { VDatePicker } from 'vuetify/labs/VDatePicker'
import 'vuetify/styles'


// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#1867C0',
          secondary: '#5CBBF6',
        },
      },
    },
  },
  components: {
    VDatePicker,
  }
})
