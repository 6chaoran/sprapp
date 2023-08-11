<template>
    <v-row class="mx-1 my-3">
        <v-textarea v-model="message" color="primary" :append-icon="message ? 'mdi-send' : ''" @click:clear="clearMessage"
            @click:append="sendMessage" auto-grow clearable rows="1" row-height="15" counter variant="underlined"
            label="Enter your profile here"
            hint="You are free to input any languages that best describe your profile of Singapore PR application."></v-textarea>
    </v-row>
</template>
<script>
export default {
    data: () => ({
        message: null,
    }),
    methods: {
        sendMessage() {
            this.$emit("data", this.message)
        },
        clearMessage() {
            this.message = null
        }
    }
}
</script>