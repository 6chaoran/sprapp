<template>
    <v-row justify="space-around" style="height: 64px; margin-left: auto; margin-right: auto; max-width: 1200px;" >
        <FooterIcon to="/" :btnSize="btnSize" icon="mdi-home-outline" iconName="Home" iconId="home"
            :color="activeIconId === 'home' ? themeColor : inactiveColor" />
        <FooterIcon to="/search" :btnSize="btnSize" icon="mdi-magnify" iconName="Search" iconId="search"
            :color="activeIconId === 'search' ? themeColor : inactiveColor" />
        <FooterIcon to="/insights" :btnSize="btnSize" icon="mdi-lightbulb-on-outline" iconName="Insights" iconId="insights"
            :color="activeIconId === 'insights' ? themeColor : inactiveColor" />
    </v-row>
</template>

<script setup>
import { $on } from 'vue-happy-bus';
const btnSize = 'large'
const inactiveColor = 'grey-darken-3'
const activeIconId = ref('home')
const localePath = useLocalePath()
const props = defineProps(
    {
        themeColor: String
    }
)
$on('activeIcon', (iconId) => {
    activeIconId.value = iconId
})
</script>