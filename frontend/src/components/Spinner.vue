<template>
    <v-row class="progress-container" align="center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <span class="progress-text mx-3">{{ spinnerMessage }}</span>
    </v-row>
</template>
<script>
export default {
    props: {
        spinnerMessage: String,
    }
}
</script>