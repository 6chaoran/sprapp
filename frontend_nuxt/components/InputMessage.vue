<template>
    <v-row class="mx-1 my-3">
        <v-textarea v-model="message" 
            :color="themeColor" 
            :append-icon="message ? 'mdi-send' : ''" @click:clear="clearMessage"
            @click:append="sendMessage" auto-grow clearable rows="1" row-height="15" variant="underlined"
            @keyup.ctrl.enter.prevent="sendMessage"
            :label="$t('search.label')"
            :hint="$t('search.hint')"></v-textarea>
    </v-row>
    <v-row class="mx-3 mt-6 mb-3">
        <structure-input :theme-color="themeColor"/>
    </v-row>
</template>
<script setup>
import { $on } from 'vue-happy-bus';
const { logEventGA } = useAnalytics() // auto-imported
const message = ref(null)
const emit = defineEmits(['data'])
const props = defineProps({
    themeColor: String
}) 
const sendMessage = () => {
    emit('data', message.value);
    logEventGA('search', {query: message.value})
}
const clearMessage = () => {
    message.value = null
}

$on('profileMsg', (msg) => {
    message.value = msg
    showLazyTyping.value = false
})


</script>