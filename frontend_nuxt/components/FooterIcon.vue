<template>
    <v-btn icon :to="localePath(to)" :size="btnSize" variant="plain" @click="changeActiveIcon">
        <v-col align="center">
            <v-icon :color="color">{{ icon }}</v-icon>
            <p id="iconText" class="text-subtitle-2">{{ iconName }}</p>
        </v-col>
    </v-btn>
</template>
<script setup>
import { $emit } from 'vue-happy-bus'
const localePath = useLocalePath()
const active = ref('home')
const props = defineProps({
    to: String,
    btnSize: String,
    icon: String,
    color: String,
    iconName: String,
    iconId: String
})
const changeActiveIcon = () => {
    $emit('activeIcon', props.iconId)
}
</script>
<style scoped>
#iconText {
    color: v-bind('color');
}
</style>