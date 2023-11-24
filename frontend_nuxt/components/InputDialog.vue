<script setup>
import { useDisplay } from 'vuetify'
const { width, mobile } = useDisplay()
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
</script>

<template>
    <v-dialog v-model="dialog" max-width="600px" :fullscreen="mobile">
        <template v-slot:activator="{ attrs }">
            <v-btn color="white" icon dark v-bind="attrs" @click="update">
                <!-- <v-icon>mdi-dots-vertical</v-icon> -->
                <v-icon>mdi-magnify</v-icon>
            </v-btn>
        </template>
        <template v-slot:default="{ isActive }">
            <v-card class="py-6">
                <v-card-title class="mt-3">{{ $t('search.title') }}</v-card-title>
                <v-card-text>
                    <QueryMatches :theme-color="themeColor" />
                </v-card-text>

                <v-card-actions class="mb-12">
                    <v-spacer></v-spacer>
                    <v-btn :color="themeColor" text @click="close">
                        {{ $t('button.cancel') }}
                    </v-btn>
                </v-card-actions>
            </v-card>
        </template>

    </v-dialog>
</template>
