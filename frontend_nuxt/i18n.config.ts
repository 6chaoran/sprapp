export default defineI18nConfig(() => ({
    // We'll fill this in momentarily
    legacy: false,
    messages: {
        // raw: {
        //     button: {
        //         add: 'add my record',
        //         edit: 'edit my record',
        //         cancel: 'cancel',
        //         save: 'save',
        //         del: 'delete my record',
        //         lazy: 'lazy typing? click me',
        //         action: 'Actions',
        //         insight: 'Show me insights'
        //     },
        //     status: {
        //         pass: 'pass',
        //         rejected: 'rejected',
        //         pending: 'pending'
        //     },
        //     form: {
        //         title: 'Profile template',
        //         age: 'Age',
        //         gender: 'Gender',
        //         nat: 'Nationality',
        //         occ: 'Occupation',
        //         income: 'Income',
        //         kid: 'With Kids',
        //         yrsg: 'Years in Singapore',
        //         yrwork: 'Years of working'  
        //     },
        //     search: {
        //         title: 'Search your similar profile',
        //         label: 'Enter your profile here to evaluate',
        //         hint: 'You are free to input any languages that best describe your profile of Singapore PR application.'
        //     },
        //     recent_records: 'Navigate Recent Records:',
        //     query: {
        //         progress: 'Query In Progres ...'
        //     },
        //     links: {
        //         useful: 'Useful Links',
        //         ica: 'ICA PR Webiste',
        //     }
        // },
        en: {
            title: {
                name: 'SGPRProfile',
                slogan: 'A Singapore PR Profile Evaluator',
                subtitle: 'navigate your PR journey with confidence'
            },
            button: {
                add: 'add my record',
                edit: 'edit my record',
                cancel: 'cancel',
                save: 'save',
                del: 'delete my record',
                lazy: 'lazy typing? click me',
                action: 'Actions',
                insight: 'Show me insights'
            },
            status: {
                pass: 'pass',
                rejected: 'rejected',
                pending: 'pending'
            },
            form: {
                title: 'Profile Template',
                age: 'Age',
                gender: 'Gender',
                nat: 'Nationality',
                occ: 'Occupation',
                income: 'Income',
                kid: 'With Kids',
                yrsg: 'Years in Singapore',
                yrwork: 'Years of working'  
            },
            search: {
                title: 'Search your similar profile',
                label: 'Enter your profile here',
                hint: 'You are free to input any languages that best describe your profile of Singapore PR application.'
            },
            recent_records: 'Recent Records',
            query: {
                progress: 'Query In Progres ...'
            },
            links: {
                useful: 'Useful Links',
                ica: 'ICA PR Webiste',
            }
        },
        zh: {
            title: {
                name: 'SGPRProfile',
                slogan: '新加坡永居申请评估引擎',
                subtitle: '让您自信从容地了解永居申请机会'
            },
            button: {
                add: '添加我的记录',
                edit: '修改我的记录',
                cancel: '取消',
                save: '保存',
                del: '删除我的记录',
                lazy: '懒得打字？ 戳我',
                action: '我的操作',
                insight: '显示过往趋势'
            },
            search: {
                title: '搜索与您相似的案例',
                label: '输入您的申请情况',
                hint: '您可以自由地输入任何言语来描述您的申请详情。'
            },
            recent_records: '最近的记录',
            query: {
                progress: '查询记录中。。。'
            },
            status: {
                pass: '通过',
                rejected: '杯具',
                pending: '等待'
            },
            form: {
                title: '从模板选择您的申请详情',
                age: '年龄',
                gender: '性别',
                nat: '国籍',
                occ: '职业',
                income: '收入',
                kid: '带娃一起？',
                yrsg: '来坡多久',
                yrwork: '工作多久'  
            },
            links: {
                useful: '常用链接',
            }
        }
    },

  }))