<template>
        <v-row justify="space-evenly" style="height: 64px;">
            <v-btn icon to="/" :size="btnSize" variant="plain" @click="active='home'">
                <v-icon :color="active === 'home' ? themeColor : inactiveColor">mdi-home</v-icon>
            </v-btn>
            <v-btn icon to="/insights" :size="btnSize" variant="plain" @click="active='insights'">
                    <v-icon :color="active === 'insights' ? themeColor : inactiveColor">mdi-lightbulb-on-outline</v-icon>

            </v-btn>
            <v-btn icon to="/search" :size="btnSize" variant="plain" @click="active='search'">
                    <v-icon :color="active === 'search' ? themeColor : inactiveColor">mdi-magnify</v-icon>

            </v-btn>
        </v-row>
</template>

<script setup>
const btnSize = 'large'
const active = ref('home')
const inactiveColor = 'grey-darken-3'
const props = defineProps(
    {
        themeColor: String
    }
)
</script>