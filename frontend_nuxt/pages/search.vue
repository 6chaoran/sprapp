<template>
    <h2>{{ $t('search.title') }}</h2>
    <QueryMatches :theme-color="themeColor"/>
</template>
<script setup>
const themeColor = '#00C16A'
</script>