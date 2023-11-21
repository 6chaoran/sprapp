<template>
    <v-row>
        <InsightChart />
    </v-row>
    <v-row v-if="mobile">
        <v-col>
            <InsightChartHist />
            <InsightChartBox />
        </v-col>
    </v-row>
    <v-row v-else>
        <v-col cols="7">
            <InsightChartHist />
        </v-col>
        <v-col cols="5">
            <InsightChartBox />
        </v-col>
    </v-row>
</template>

<script setup>
import InsightChart from './Charts/InsightChart.vue';
import InsightChartBox from './Charts/InsightChartBox.vue';
import InsightChartHist from './Charts/InsightChartHist.vue';
import { useDisplay } from 'vuetify'
const { mobile } = useDisplay()
</script>