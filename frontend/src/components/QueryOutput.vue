<template>
    <v-row>
        <v-col>
            <p style="text-align: justify;">
                Taking into account the comparable profiles, <br>
                there is a <span :class="resultStyle">{{ (odds * 100) + '%' }}</span> possibility of
                obtaining Singapore Permanent
                Resident status,
                indicating a probable <span :class="resultStyle">{{ decision }}</span> result for your
                application. The estimated
                waiting period is <span :class="resultStyle">{{ (duration / 30).toFixed(1) }}</span>
                months.<span v-if="decision == 'pass'">If you've been
                    waiting more than {{ (duration / 30).toFixed(1) }} months, you should have better
                    chance that your ICA letter is
                    on the way to you!</span>
            </p>
        </v-col>
    </v-row>

    <v-row align="baseline">
        <v-col>
            <p>The 5 most similar profiles:</p>
        </v-col>
        <v-col cols = 2>
            <v-switch v-model="descLang" prepend-icon="mdi-translate" inset dense true-value="en" false-value="raw"
                hint="switch language" label="EN"></v-switch>
        </v-col>

    </v-row>

    <v-row no-gutters>
        <v-col cols='12'>
            <v-card v-for="(item, index) in matches" :key="index" class="mt-3" elevation="2">
                <v-card-text>{{ descLang == 'raw' ? item.desc : item.desc_en }}</v-card-text>
                <v-card-text>
                    <v-row class="px-3" style="align-items: center;">
                        <v-icon class="mr-1">mdi-calendar</v-icon>{{
                            item.update_time.substring(0, 10) }}
                        <v-spacer></v-spacer>
                        <v-icon class="mr-1">mdi-timer-sand</v-icon>
                        {{ (item.duration / 30).toFixed(1) }} months
                        <v-spacer></v-spacer>
                        <v-chip text-color="white" :color="statusIconColor(item.result)">
                            <v-avatar left v-if="item.result == 'pass'">
                                <v-icon color="green">mdi-checkbox-marked-circle</v-icon>
                            </v-avatar>
                            {{ item.result }}
                        </v-chip>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-col>

    </v-row>
</template>

<script>
export default {
    props: {
        matches: Array,
        prediction: Object,
        resultStyle: String,
    },
    data() {
        return {
            descLang: "raw",
            odds: this.prediction.odds,
            duration: this.prediction.duration,
            decision: this.prediction.decision,
        }
    },
    methods: {
        statusIconColor(x) {
            let colors = {
                pass: 'green',
                rejected: 'red',
            }

            return colors[x] ?? 'primary'
        },
    }
}
</script>

<style scoped>
.text-green {
    color: green;
}

.text-red {
    color: red;
}
</style>