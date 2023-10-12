<template>
    <v-row class="mt-9 mx-3">
        <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ attrs }">
                <v-row>
                    <v-btn :color="themeColor" dark v-bind="attrs" @click="update">
                        {{ buttonText }}
                    </v-btn>
                </v-row>
            </template>
            <template v-slot:default="{ isActive }">
                <v-card>
                    <v-card-title>
                        <span class="text-h5">{{ cardText }}</span>
                    </v-card-title>
                    <v-card-text>
                        <submission-form 
                            :formType="formType"
                            :themeColor="themeColor" 
                            :desc = "desc"
                            @edited-item = "updateEditedItem"
                            @ready-to-submit="checkFormReadiness" />
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn :color="themeColor" text @click="close">
                            Cancel
                        </v-btn>
                        <v-btn v-if="formType === 'edit'" :color="themeColor" text @click="saveEditRow" :disabled="!readyToSubmit">
                            Save
                        </v-btn>
                        <v-btn v-if="formType === 'add'" :color="themeColor" text @click="saveAddRow" :disabled="!readyToSubmit">
                            Save
                        </v-btn>
                    </v-card-actions>
                </v-card>

            </template>

        </v-dialog>
    </v-row>
</template>
<script setup>
import { ref } from 'vue';
import SubmissionForm from './SubmissionForm.vue';
import { postData } from '@/assets/js/apis';
const props = defineProps({
    themeColor: String,
    buttonText: String,
    cardText: String,
    formType: String,
    desc: String,
})

const emit = defineEmits([
    'edited-item'
])

const dialog = ref(false);
const readyToSubmit = ref(false);
const editedItem = ref({})
const updateEditedItem = (x) => {
    editedItem.value = x
}
const update = () => {
    dialog.value = true
    console.log('editRecordUpdate');
}
const checkFormReadiness = (x) => {
    readyToSubmit.value = x
}

const close = () => {
    dialog.value = false;
    readyToSubmit.value = false
}

const ingestToPineCone = async () => {
    if (editedItem.value.status == "pending") {
        console.log("pending result => skip ingestion")
    } else {
        const now = (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
        postData('api/v1/ingest', {
                username: editedItem.value.username,
                text: editedItem.value.description,
                status: editedItem.value.status,
                applied_date: editedItem.value.applied_date,
                closed_date: editedItem.value.closed_date,
                update_time: now
            }).then(() => {
            console.log('ingest to vectordb')
        }).catch(e => {
            console.log(e)
        }).finally(() => { })
    }
}


const saveAddRow = () => {
    postData('api/v1/add_record', {
        username: editedItem.value.username,
        password: editedItem.value.password,
        text: editedItem.value.description,
        email: editedItem.value.email,
        status: editedItem.value.status,
        applied_date: editedItem.value.applied_date,
        closed_date: editedItem.value.closed_date
    }).then((data) => {
        console.log("adding record to db");
        console.log(data);
        if (data != "ok") {
            window.alert(data)
        } else {
           close()
           emit('edited-item', editedItem.value)
           ingestToPineCone()
           sendEmail()
        }

    }).catch(e => { }).finally(() => { })
    dialog.value = false;
}

const saveEditRow = () => {
    postData('api/v1/edit_record', {
        username: editedItem.value.username,
        password: editedItem.value.password,
        text: editedItem.value.description,
        email: editedItem.value.email,
        status: editedItem.value.status,
        applied_date: editedItem.value.applied_date,
        closed_date: editedItem.value.closed_date
    }).then((data) => {
        console.log("edit record in db");
        console.log(data);
        if (data != "ok") {
            window.alert(data)
        } else {
           close()
           emit('edited-item', editedItem.value)
           ingestToPineCone()
        }

    }).catch(e => { }).finally(() => { })
    dialog.value = false;
}


const sendEmail = () => {
    postData('/api/v1/send_email', {
        recipient_email: editedItem.value.email,
            username: editedItem.value.username,
            password: editedItem.value.password,
            applied_date: editedItem.value.applied_date,
            description: editedItem.value.description,
            closed_date: editedItem.value.closed_date,
            status: editedItem.value.status,
    }).then(() => {
        console.log("email sent");
    }).catch(e => { console.log(e) }).finally(() => { })
}

</script>