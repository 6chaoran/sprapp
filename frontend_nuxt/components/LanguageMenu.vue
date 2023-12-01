<template>
    <v-menu :location="location">
      <template v-slot:activator="{ props }">
        <v-btn
          :size=" mobile ? 'small' : 'default'"
          dark
          icon
          v-bind="props"
        >
        <v-icon>mdi-translate</v-icon>
        </v-btn>
      </template>

      <v-list v-model:selected = "lang"  
      :color="themeColor"
        @click="emitLang" :items = items :mandatory=true></v-list>
    </v-menu>
</template>

<script setup>
import { useDisplay } from 'vuetify'
const { locale, setLocale } = useI18n()
const location = "bottom"
const lang = ref(['en'])
const props = defineProps({
    themeColor: String,
})
const { mobile } = useDisplay()
const emit = defineEmits(['lang'])
const emitLang = () => {
    setLocale(lang.value[0])
}
const items = [
    // {title: "Original", value: "raw"},
    {title: "English", value: "en"},
    {title: "简体中文", value: "zh"},
]
</script>