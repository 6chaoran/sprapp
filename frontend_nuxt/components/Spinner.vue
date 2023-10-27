<template>
    <v-row class="progress-container" align="center">
        <v-progress-circular indeterminate :color="themeColor" size="25" class="ml-3"></v-progress-circular>
        <span class="progress-text mx-3">{{ spinnerMessage }}</span>
    </v-row>
</template>
<script>
export default {
    props: {
        spinnerMessage: String,
        themeColor: String,
    }
}
</script>