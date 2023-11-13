<template>
    <v-dialog v-model="dialog" max-width="500px" :fullscreen="mobile">
        <template v-slot:activator="{ attrs }">
            <v-row>
                <v-btn :color="themeColor" dark v-bind="attrs" @click="update" variant='text'>
                    {{ $t('button.lazy') }} <p style="font-size: 2rem">😜</p>
                </v-btn>
            </v-row>
        </template>
        <template v-slot:default="{ isActive }">
            <v-card>
                <v-card-title>
                    <span class="text-h5">{{ $t('form.title') }}</span>
                </v-card-title>
                <v-card-text>
                    <v-form>
            {{ profileMsg }}
            <v-list>
                <v-list-item v-for="item, key in items" :key="key">
                    <v-text-field v-if="item.type == 'text'" :label="item.title" variant="underlined" v-model="item.selected">
                    </v-text-field>
                    <v-select v-if="item.type == 'select'" :label="item.title" :items="item.items" v-model = "item.selected" variant="underlined"></v-select>
                </v-list-item>
            </v-list>
        </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn :color="themeColor" text @click="close">
                        {{ $t('button.cancel') }}
                    </v-btn>
                    <v-btn :color="themeColor" text @click="save">
                        {{ $t('button.save') }}
                    </v-btn>
                </v-card-actions>
            </v-card>

        </template>

    </v-dialog>
</template>

<script setup>
import { i18n } from '@/plugins/i18n';
import { computed } from 'vue';
import { ref } from 'vue'
import { $emit } from 'vue-happy-bus';
import { useDisplay } from 'vuetify/lib/framework.mjs';
const props = defineProps({
    themeColor: String,
})
const dialog = ref(false)
const update = () => {
    dialog.value = true
}
const save = () => {
    $emit('profileMsg', profileMsg.value)
    dialog.value = false
}
const close = () => {
    dialog.value = false
}


const profileMsg = computed( () => {
    const age = items.value[0].selected
    const gender = items.value[1].selected
    const nationality = items.value[2].selected
    const occupation = items.value[3].selected
    const income = items.value[4].selected
    const kids = items.value[5].selected
    const yearsg = items.value[6].selected
    const yearworking = items.value[7].selected


    const ageString = age.length > 0 ? `${age} years old, ` : ''
    const genderString = gender.length > 0 ? `${gender}, ` : ''
    const nationalityString = nationality.length > 0 ? `${nationality} nationality, ` : ''
    const occupationString = occupation.length > 0 ? `working as ${occupation}, ` : ''
    const incomeString = String(income).length > 0 ? `monthly salary ${income}, ` : ''
    const yearsgString = yearsg.length > 0 ? `has been in Singapore for ${yearsg} years, ` : ''
    const yearworkingString = yearworking.length > 0 ? `has been working for ${yearworking} years, ` : ''
    const kidsString = kids.length > 0 && kids === "yes" ? `applied with kids, ` : ''


    return ageString + genderString + nationalityString + occupationString + incomeString + yearsgString + yearworkingString + kidsString

})

const { width, mobile } = useDisplay

const items = ref([
    {
        title: "Age",
        selected: '',
        type: 'text'
    },
    {
        title: "Gender",
        type: 'select',
        selected: '',
        items: ['male', 'female']
    },
    {
        title: "Nationality",
        type: 'select',
        selected: '',
        items: ['Chinese', 'Malaysian', 'Indian', 'Others']
    },
    {
        title: "Occupation",
        type: 'text',
        selected: ''
    },
    {
        title: "Income per Month",
        type: 'select',
        selected: '',
        items: Array.from(Array(20).keys()).map( i =>  (i + 3) * 1000)
    },
    {
        title: "With Kids",
        type: 'select',
        selected: '',
        items: ['yes', 'no']
    },
    {
        title: "Years in Singapore",
        type: 'text',
        selected: ''    
    },
    {
        title: "Years of working",
        type: 'text',
        selected: ''    
    },
])

</script>