<template>
    <v-row>
        <v-col class = 'mx-3'><Dialog :theme-color="themeColor" :button-text="$t('button.edit')" :card-text="$t('button.edit')" formType="edit" desc="" btn-width="100%"/></v-col>
    </v-row>
    
    <v-row style="position: fixed; left: 9px; bottom: 18px; justify-content: center;"> 
        <v-col>    
        <a href="https://www.buymeacoffee.com/chaoran"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=chaoran&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>
     </v-col></v-row>
   
</template>

<script setup>
import Dialog from './Dialog.vue';
const props = defineProps({
    themeColor: String
})

</script>