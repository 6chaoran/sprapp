<template>
    <v-row class="mt-9 mx-3">
        <v-dialog v-model="dialog" max-width="500px" :fullscreen="mobile">
            <template v-slot:activator="{ attrs }">
                <v-row>
                    <v-btn :color="themeColor" dark v-bind="attrs" @click="update" :width="btnWidth">
                        {{ buttonText }}
                    </v-btn>
                </v-row>
            </template>
            <template v-slot:default="{ isActive }">
                <v-card>
                    <v-card-title>
                        <span class="text-h5">{{ cardText.toUpperCase() }}</span>
                    </v-card-title>
                    <v-card-text>
                        <submission-form 
                            :formType="formType"
                            :themeColor="themeColor" 
                            :desc = "desc"
                            @edited-item = "updateEditedItem"
                            @ready-to-submit="checkFormReadiness" />
                    </v-card-text>
                    <v-card-actions class="mb-12">
                        <v-spacer></v-spacer>
                        <v-btn :color="themeColor" text @click="close">
                            {{ $t('button.cancel') }}
                        </v-btn>
                        <v-btn v-if="formType === 'edit'" :color="themeColor" text @click="saveEditRow" :disabled="!readyToSubmit">
                            {{ $t('button.save') }}
                        </v-btn>
                        <v-btn v-if="formType === 'add'" :color="themeColor" text @click="saveAddRow" :disabled="!readyToSubmit">
                            {{ $t('button.save') }}
                        </v-btn>
                        <v-btn v-if="formType === 'del'" :color="themeColor" text @click="saveDelRow" :disabled="!readyToSubmit">
                            {{ $t('button.del') }}
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
import { delData, postData, putData } from '@/assets/js/apis';
import { $emit } from 'vue-happy-bus';
import { useDisplay } from 'vuetify'
const { width, mobile } = useDisplay()
const props = defineProps({
    themeColor: String,
    buttonText: String,
    cardText: String,
    formType: String,
    desc: String,
    btnWidth: String,
})

const emit = defineEmits([
    'add-item', 'edit-item'
])

const dialog = ref(false);
const readyToSubmit = ref(false);
const editedItem = ref({})
const updateEditedItem = (x) => {
    editedItem.value = x
}
const update = () => {
    dialog.value = true
    // console.log('editRecordUpdate');
}
const checkFormReadiness = (x) => {
    readyToSubmit.value = x
}

const close = () => {
    dialog.value = false;
    readyToSubmit.value = false
}

const ingest = async (userId) => {
    const now = (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 19)
    putData('/ingest', {
        id: userId,
        text: editedItem.value.description
    }).then(() => {
        console.log('ingest to vectordb')
    }).catch(e => {
        console.log(e)
    }).finally(() => { })

}


const saveAddRow = () => {
    postData('/add_record', {
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
        const status = data.status
        const userId = data.id
        if (status === "ok") {
           close()
           const update_ts = (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 19)
           editedItem.value['update_ts'] = update_ts
           $emit('add-item', editedItem.value)
           ingest(userId)
           sendEmail()
        } else {
           window.alert(status)
        }

    }).catch(e => { }).finally(() => { })

}

const saveEditRow = () => {
    putData('/edit_record', {
        username: editedItem.value.username,
        password: editedItem.value.password,
        text: editedItem.value.description,
        email: editedItem.value.email,
        status: editedItem.value.status,
        applied_date: editedItem.value.applied_date,
        closed_date: editedItem.value.closed_date
    }).then((data) => {
        // console.log("edit record in db");
        // console.log(data);
        const status = data.status
        const userId = data.id
        if (status === "ok") {
           close()
           const update_ts = (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 19)
           editedItem.value['update_ts'] = update_ts
           $emit('edit-item', editedItem.value)
           ingest(userId)
        } else {
            window.alert(status)
        }

    }).catch(e => { }).finally(() => { })
    
}

const saveDelRow = () => {
    delData('/delete_record', [editedItem.value.id]).then((data) => {
        // console.log("edit record in db");
        // console.log(data);
        const status = data.status
        if (status === "ok") {
            window.alert('deleted')
           close()
        } else {
            window.alert(status)
        }

    }).catch(e => { }).finally(() => { })
    
}

const sendEmail = () => {
    postData('/send_email', {
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