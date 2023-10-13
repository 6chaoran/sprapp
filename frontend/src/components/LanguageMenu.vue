<template>
    <v-menu :location="location">
      <template v-slot:activator="{ props }">
        <v-btn
          color="white"
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
import { ref } from 'vue'
import { $emit } from 'vue-happy-bus'

const location = "bottom"
const lang = ref(['raw'])
const props = defineProps({
    themeColor: String,
})
const emit = defineEmits(['lang'])
const emitLang = () => {
    $emit('lang', lang.value[0])
}
const items = [
    {title: "Original", value: "raw"},
    {title: "English", value: "en"},
    {title: "简体中文", value: "zh"},
]
</script>