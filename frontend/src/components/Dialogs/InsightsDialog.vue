<template>
    <v-dialog v-model="dialogInsight" :fullscreen="mobile">
        <v-card class="pa-6">
            <InsightCharts />
            <v-card-actions class="mb-12">
                <v-spacer></v-spacer>
                <v-btn @click="closeInsightDialog">Cancel</v-btn>
            </v-card-actions>
        </v-card>

    </v-dialog>
</template>
<script setup>
import { ref } from 'vue'
import { $on } from 'vue-happy-bus'
import { useDisplay } from 'vuetify'
const { mobile } = useDisplay()

import InsightCharts from '@/components/InsightCharts.vue'

const dialogInsight = ref(false)
const closeInsightDialog = () => {
    dialogInsight.value = false
}
$on('open-insight-dialog', () => {
    dialogInsight.value = true
})
</script>