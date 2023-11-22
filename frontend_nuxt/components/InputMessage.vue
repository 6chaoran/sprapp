<template>
    <v-row class="mx-1 my-3">
        <v-textarea v-model="message" 
            :color="themeColor" 
            :append-icon="message ? 'mdi-send' : ''" @click:clear="clearMessage"
            @update:focused="touch"
            @click:append="sendMessage" auto-grow clearable rows="1" row-height="15" variant="underlined"
            @keyup.ctrl.enter.prevent="sendMessage"
            :label="$t('search.label')"
            :hint="$t('search.hint')"></v-textarea>
    </v-row>
    <v-row class="mx-1 my-3" v-if="showLazyTyping">
        <structure-input />
    </v-row>
</template>
<script setup>
import { $on } from 'vue-happy-bus';
const { logEventGA } = useAnalytics() // auto-imported
const showLazyTyping = ref(false)
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

const touch = () => {
    showLazyTyping.value = true;

}
</script>