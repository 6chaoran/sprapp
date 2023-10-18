<template>
    <v-row>
        <v-col class="ma-3 mb-9">
            Actions:
            <v-row class="mb-3 mx-3">
                <Dialog :theme-color="themeColor" :button-text="$t('button.edit')" :card-text="$t('button.edit')"
                    formType="edit" desc="" btn-width="100%" />
            </v-row>
            <v-row class="mb-3 mx-3">
                <Dialog :theme-color="themeColor" :button-text="$t('button.del')" :card-text="$t('button.del')"
                    formType="del" desc="" btn-width="100%" />
            </v-row>

        </v-col>
    </v-row>
    <v-row>
        <v-col>
            <v-divider></v-divider>
        </v-col>
    </v-row>
    <v-row>
        <v-col class="mx-3">
            Useful Links:
            <v-list>
                <v-list-item v-for="(item, id) in usefulLinks" :key="id">
                    <v-btn variant="text" :href="item.url" target="_blank"><v-icon class="mr-3" :color="themeColor">{{
                        item.icon }} </v-icon>{{ item.title }}</v-btn>
                </v-list-item>
            </v-list>
        </v-col>

    </v-row>
    <v-row>
        <v-col>
            <v-divider></v-divider>
        </v-col>
    </v-row>
    <v-row style="position: fixed; left: 9px; bottom: 18px; justify-content: center;">
        <v-col>
            <a href="https://www.buymeacoffee.com/chaoran"><img
                    src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=chaoran&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>
        </v-col></v-row>
</template>

<script setup>
import Dialog from './Dialog.vue';
const props = defineProps({
    themeColor: String
})

const usefulLinks = [
    {
        url: 'https://www.ica.gov.sg/reside/PR/apply',
        title: 'ICA PR Website',
        icon: 'mdi-flag'
    }
]

</script>