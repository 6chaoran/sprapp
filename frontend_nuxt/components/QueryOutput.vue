<script setup>
import { ref } from 'vue'
const { locale, setLocale } = useI18n()
const props = defineProps({
    matches: Array,
    prediction: Object,
    resultStyle: String,
    color: String
})

const odds = ref(props.prediction.odds)
const duration = ref(props.prediction.duration)
const decision = ref(props.prediction.decision)
const statusIconColor = (x) => {
    let colors = {
                pass: 'green',
                rejected: 'red',
            }
    return colors[x] ?? 'primary'
}

</script>
<template>
   
    <v-row>
        <v-col cols=12>
            <p style="text-align: justify;" v-if="locale != 'zh'">
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
            <p style="text-align: justify;" v-else>
                考虑到可比较的情况，<br>
                您获得新加坡永久居民身份的可能性为<span :class="resultStyle">{{ (odds * 100) + '%' }}</span>，这表明您的申请很可能会<span :class="resultStyle">{{ decision === 'pass' ? '通过' : '失败' }}</span>。估计的等待时间为<span :class="resultStyle">{{ (duration / 30).toFixed(1) }}</span>个月。如果您已经等待了超过<span :class="resultStyle">{{ (duration / 30).toFixed(1) }}</span>个月，那么您更有可能会收到新加坡移民与关卡局的来信
            </p>
        </v-col>
    </v-row>

    <v-row align="baseline">
        <v-col>
            <p v-if="locale != 'zh'">The 5 most similar profiles:</p>
            <p v-else>五个最相似的档案：</p>

        </v-col>
    </v-row>

    <v-row no-gutters>
        <v-col cols='12'>
            <v-card v-for="(item, index) in matches" :key="index" class="mt-3" elevation="2">
                <v-card-text>{{ locale == 'en' ? item.description_en : item.description }}</v-card-text>
                <v-card-text>
                    <v-row class="px-3" style="align-items: center;">
                        <v-icon class="mr-1">mdi-calendar</v-icon>{{
                            item.applied_date }}
                        <v-spacer></v-spacer>
                        <v-icon class="mr-1">mdi-timer-sand</v-icon>
                        {{ (item.duration / 30).toFixed(1) }} months
                        <v-spacer></v-spacer>
                        <v-chip text-color="white" :color="statusIconColor(item.status)">
                            <v-avatar left v-if="item.status == 'pass'">
                                <v-icon color="green">mdi-checkbox-marked-circle</v-icon>
                            </v-avatar>
                            {{ item.status }}
                        </v-chip>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-col>

    </v-row>
</template>



<style scoped>
.text-green {
    color: green;
}

.text-red {
    color: red;
}
</style>
