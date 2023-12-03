<template>
    <div v-if="mobile">
        <h1 style="color:#00C16A">SGPRProfiler</h1>
        <p class="text-h6 text-black">{{ $t('title.slogan') }}</p>
        <p>{{ $t('title.subtitle') }}</p>
    </div>
    <div v-else>
        <h1 class="text-grey-darken-3"><span style="color:#00C16A;">SGPRProfiler</span> | {{ $t('title.slogan') }}</h1>
        <p class="text-h5">{{ $t('title.subtitle') }}</p>
    </div>
    <div class="mt-3">
        This site intend to be a place for us to share PR application experience and present the trend for your better reference.
    </div>
</template>

<script setup>
import { useDisplay } from 'vuetify'
const { mobile } = useDisplay()
</script>