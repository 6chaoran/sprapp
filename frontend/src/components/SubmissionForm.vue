<script setup>
import { fetchData, postData } from '@/assets/js/apis';
import { onMounted } from 'vue';
import { ref, watch } from 'vue'
const props = defineProps({
    themeColor: String,
    formType: String, // add | edit
    desc: String,
})
const emit = defineEmits([
    'ready-to-submit', 
    'edited-item'
])
const editFormValid = ref(null);
const userVerified = ref(false);

if (props.formType === 'add'){
    watch([editFormValid], () => {
        emit('ready-to-submit', editFormValid.value)
    })
} else {
    watch([editFormValid, userVerified], () => {
        emit('ready-to-submit', editFormValid.value && userVerified.value)
    })
}

const editedItem = ref({
    username: '',
    password: '',
    description: props.desc,
    status: 'pending',
    applied_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
    closed_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
})

onMounted( () => {
    emit('edited-item', editedItem.value)
})

const formVariant = "underlined";
const rules = {
    required: value => !!value || 'Required.',
    counter: value => value.length <= 20 || 'Max 20 characters',
    email: value => {
        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return pattern.test(value) || 'Invalid e-mail.'
    },
}

const verifyUser = () => {
    postData('api/v1/verify_user', {
        username: editedItem.value.username,
        password: editedItem.value.password
    }).then(resp => {
        if (resp) {
            editedItem.value.email = resp['email']
            editedItem.value.description = resp['description']
            editedItem.value.applied_date = resp['applied_date']
            editedItem.value.closed_date = resp['closed_date']
            editedItem.value.status = resp['status']
            userVerified.value = true
        } else {
            window.alert("Invalid username and password combination")
            userVerified.value = false
        }
    })
}
</script>


<template>
    <v-form v-model="editFormValid">
        <v-container>
            <v-row class="mb-3">
                Please provide a valid email to recieve a reminder to update your
                status. 
            </v-row>
            <v-row>
                <v-text-field :variant="formVariant" :disabled="userVerified" label="User Name"
                    v-model="editedItem.username" :rules="[rules.required]"></v-text-field>
            </v-row>
            <v-row align="center">
                <v-col cols='8' class="px-0">
                    <v-text-field :variant="formVariant" :disabled="userVerified" label="Password"
                        v-model="editedItem.password"
                        hint="used for editing your record, can be as simple as your DOB in form of mmdd" type="password"
                        :rules="[rules.required]"></v-text-field>
                </v-col>
                <v-col cols='2' v-if="formType == 'edit'">
                    <v-btn 
                        :disabled="userVerified" 
                        rounded
                        @click="verifyUser" 
                        :color="themeColor">verify</v-btn>
                </v-col>
            </v-row>
            <v-row>
                <v-text-field :variant="formVariant" :disabled="userVerified" v-model="editedItem.email" label="Email"
                    :rules="[rules.required, rules.email]"></v-text-field>
            </v-row>
            <v-row>
                <v-textarea :variant="formVariant" auto-grow clearable rows="1" row-height="15"
                    v-model="editedItem.description" label="Description"></v-textarea>
            </v-row>
            <v-row>
                <v-text-field type="date" :variant="formVariant" v-model="editedItem.applied_date"
                    label="Applied Date" :rules="[rules.required]"> </v-text-field>
            </v-row>
            <v-row>
                <v-select :items="['pending', 'pass', 'rejected']" label="Status" :variant="formVariant"
                    v-model="editedItem.status" :rules="[rules.required]"></v-select>
            </v-row>
            <v-row v-if="editedItem.status != 'pending'">
                <v-text-field type="date" :variant="formVariant" v-model="editedItem.closed_date"
                    label="Closed Date" :rules="[rules.required]"></v-text-field>
            </v-row>
        </v-container>
    </v-form>
</template>