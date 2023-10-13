<template>
    <v-row class="mx-1 my-3">
        <v-textarea v-model="message" 
            :color="themeColor" 
            :append-icon="message ? 'mdi-send' : ''" @click:clear="clearMessage"
            @click:append="sendMessage" auto-grow clearable rows="1" row-height="15" variant="underlined"
            @keyup.ctrl.enter.prevent="sendMessage"
            label="Enter your profile here"
            hint="You are free to input any languages that best describe your profile of Singapore PR application."></v-textarea>
    </v-row>
</template>
<script setup>
import { ref } from 'vue'
const message = ref(null)
const emit = defineEmits(['data'])
const props = defineProps({
    themeColor: String
}) 
const sendMessage = () => {
    emit('data', message.value);
}
const clearMessage = () => {
    message.value = null
}
</script>