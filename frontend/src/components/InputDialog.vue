<script setup>
import InputMessage from './InputMessage.vue';

import { ref } from 'vue'
const props = defineProps({
    themeColor: String,
})
const dialog = ref(false)
const update = () => {
    dialog.value = true
}
const close = () => {
    dialog.value = false
}
const sendMessage = () => {

}

</script>

<template>
    <v-dialog v-model="dialog" max-width="500px">
        <template v-slot:activator="{ attrs }">

            <v-btn :color="themeColor" icon dark v-bind="attrs" @click="update">
                <!-- <v-icon>mdi-dots-vertical</v-icon> -->
                <v-icon>mdi-magnify</v-icon>

            </v-btn>
        </template>
        <template v-slot:default="{ isActive }">
            <v-card>
                <v-card-text>
                    <InputMessage @data="sendMessage" />
                </v-card-text>
                
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn :color="themeColor" text @click="close">
                        Cancel
                    </v-btn>
                </v-card-actions>
            </v-card>

        </template>

    </v-dialog>
</template>
