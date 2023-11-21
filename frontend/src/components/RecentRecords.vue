<template>
  <v-row class="mt-6">
    <v-col>
      {{ $t('recent_records') }}
    </v-col>
  </v-row>
  <v-row v-if="loading"> 
    <v-col>Loading records ...
      <v-progress-linear indeterminate :color="themeColor"></v-progress-linear>
    </v-col>
  </v-row>
  <v-row>
    <v-col class="px-0">
      <v-card v-for="data in recordsFiltered" :key="data.id" class="my-3" min-height="30px" elevation="2">
        <v-card-text>
          <v-row class="mx-1">
            {{ data.username }}
            <v-spacer></v-spacer>
            {{ data.update_ts.replace('T', ' ') }} </v-row>

        </v-card-text>
        <v-card-text>{{ lang === "en" ? data.description_en : data.description }}</v-card-text>
        <v-card-text>
          <v-row class="px-3" align="center">
            {{ data.applied_date }} &nbsp; <v-icon>mdi-ray-start-arrow</v-icon>&nbsp; {{ data.status ==
              "pending" ? '' : data.closed_date }}
            <v-spacer></v-spacer>
            <v-chip :color="statusIconColor(data.status)" text-color="white">
              <v-avatar left v-if="data.status == 'pass'">
                <v-icon :color="statusIconColor(data.status)">mdi-checkbox-marked-circle</v-icon>
              </v-avatar>
              <v-avatar left v-if="data.status == 'rejected' && i18n.global.locale === 'zh'">
                <v-icon :color="statusIconColor(data.status)">mdi-close-circle</v-icon>
              </v-avatar>
              <v-avatar left v-if="data.status === 'pending' && i18n.global.locale === 'zh'">
                <v-icon :color="statusIconColor(data.status)">mdi-timelapse</v-icon>
              </v-avatar>
              {{ convertStatusLocale(data.status) }}</v-chip></v-row>
              
          <v-divider class="mt-6 mb-3"></v-divider>
          <v-row class="px-3" justify="end" align="center">
            <p v-if="data.duration > 0">waited for {{ (data.duration/30).toFixed(1) }} months</p>
            <v-spacer></v-spacer>
              <v-btn variant="text" size="small" icon="mdi-file-document-edit-outline" @click="openEditForm(data)"> </v-btn>
              <v-btn variant="text" size="small" icon="mdi-trash-can-outline" @click="openDelForm(data)"></v-btn>
          </v-row>

        </v-card-text>

      </v-card>
      <QuickActionDialog :theme-color="themeColor"></QuickActionDialog>
      
    </v-col>
  </v-row>
</template>

<script setup>
import { $emit, $on } from 'vue-happy-bus'
import { ref } from 'vue'
import { computed } from 'vue';
import { i18n } from '@/plugins/i18n';
import QuickActionDialog from './Dialogs/QuickActionDialog.vue';
const props = defineProps({
  records: Array,
  loading: Boolean,
  themeColor: String,
})
const statusIconColor = (x) => {
  let colors = {
    pass: 'green',
    rejected: 'red'}
  return colors[x] ?? 'primary'
}
const lang = ref('raw')
$on('lang', (x) => {
  lang.value = x
})

const recordsFiltered = computed(() => {
  if (lang.value == 'en'){
    const elms = props.records.filter(elm => elm.description_en != null)
    return elms.filter(elm => elm.description_en.length > 0 && elm.description != elm.description_en)
  } else {
    return props.records
  }
})

const convertStatusLocale = (status) => {
  const statusMap = {
    pass: "通过",
    pending: "等待",
    rejected: "杯具"
  }
  if(i18n.global.locale === 'zh'){
    return statusMap[status]
  } else {
    return status
  }
}

const openEditForm = (data) => {
  $emit('editForm', data.username)
}

const openDelForm = (data) => {
  $emit('delForm', data.username)
}
</script>

