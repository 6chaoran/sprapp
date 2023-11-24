<template>
    <v-dialog v-model="dialogInsight" :fullscreen="mobile">
        <v-card class="pt-12 px-6">
            <InsightCharts />
            <v-card-actions class="mb-12">
                <v-spacer></v-spacer>
                <v-btn @click="closeInsightDialog">{{ $t('button.cancel') }}</v-btn>
            </v-card-actions>
        </v-card>

    </v-dialog>
</template>
<script setup>
import { ref } from 'vue'
import { $on } from 'vue-happy-bus'
import { useDisplay } from 'vuetify'
const { mobile } = useDisplay()

import InsightCharts from '~/components/InsightCharts.vue'

const dialogInsight = ref(false)
const closeInsightDialog = () => {
    dialogInsight.value = false
}
$on('open-insight-dialog', () => {
    dialogInsight.value = true
})
</script>