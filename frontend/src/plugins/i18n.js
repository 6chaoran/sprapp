import { createI18n, useI18n } from 'vue-i18n'


const messages = {
    raw: {
        button: {
            add: 'add my record',
            edit: 'edit my record',
            cancel: 'cancel',
            save: 'save',
        },
        search: {
            title: 'Search your similar profile',
            label: 'Enter your profile here',
            hint: 'You are free to input any languages that best describe your profile of Singapore PR application.'
        },
        recent_records: 'Recent Records:'
    },
    en: {
        button: {
            add: 'add my record',
            edit: 'edit my record',
            cancel: 'cancel',
            save: 'save',
        },
        search: {
            title: 'Search your similar profile',
            label: 'Enter your profile here',
            hint: 'You are free to input any languages that best describe your profile of Singapore PR application.'
        },
        recent_records: 'Recent Records:'
    },
    zh: {
        button: {
            add: '添加记录',
            edit: '修改记录',
            cancel: '取消',
            save: '保存',
        },
        search: {
            title: '搜索与您相似的案例',
            label: '输入您的申请情况',
            hint: '您可以自由地输入任何言语来描述您的申请详情。'
        },
        recent_records: '最近的记录：'
    }
}

const i18n = createI18n({
    legacy: true, // you must set `false`, to use Composition API
    locale: 'en', // set locale
    fallbackLocale: 'en', // set fallback locale
    messages, // set locale messages
    // If you need to specify other options, you can set other options
    // ...
  })

export { i18n } ;