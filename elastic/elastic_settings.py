
stopwords = 'а,без,более,бы,был,была,были,было,быть,\
            в,вам,вас,весь,во,вот,все,всего,всех,вы,где,да,даже,для,до,\
            его,ее,если,есть,еще,же,за,здесь,и,из,или,им,их,к,как,ко,когда,кто,\
            ли,либо,мне,может,мы,на,надо,наш,не,него,нее,нет,ни,них,но,ну,\
            о,об,однако,он,она,они,оно,от,очень,по,под,при,с,со,\
            так,также,такой,там,те,тем,то,того,тоже,той,только,том,ты,\
            у,уже,хотя,чего,чей,чем,что,чтобы,чье,чья,эта,эти,это,я,\
            a,an,and,are,as,at,be,but,by,for,if,in,into,is,it,no,not,of,on,or,\
            such,that,the,their,then,there,these,they,this,to,was,will,with'

elastic_settings = {

    'settings': {
        'analysis': {

            'filter': {
                'ru_stopwords': {
                    'type': 'stop',
                    'stopwords': stopwords,
                },
                'en_stopwords': {
                    'type': 'stop',
                    'stopwords': '_english_',
                },
                'word_delimiter': {
                    'catenate_all': True,
                    'type': 'word_delimiter',
                    'preserve_original': True,
                },
            },

            'char_filter': {
                'yo_filter': {
                    'type': 'mapping',
                    'mappings': [
                        'ё => е',
                        'Ё => Е',
                    ],
                },
            },

            'analyzer': {
                'ru_en_analyzer': {
                    'type': 'custom',
                    'tokenizer':  'standard',
                    'char_filter': ['yo_filter'],
                    'filter': [
                        'lowercase',
                        'russian_morphology',
                        'english_morphology',
                        'word_delimiter',
                        'ru_stopwords',
                        'en_stopwords',
                    ],
                },
            },
        },
    },

    'mappings': {
        'properties': {
            'description': {
                'type': 'text',
                'analyzer': 'ru_en_analyzer',
            },

            'tags': {
                'type': 'text',
                'analyzer': 'ru_en_analyzer',
            },

            'custom_description': {
                'type': 'text',
                'analyzer': 'ru_en_analyzer',
            },

            'custom_tags': {
                'type': 'text',
                'analyzer': 'ru_en_analyzer',
            },

            'project_name': {
                'type': 'keyword',
            },

            'lang': {
                'type': 'keyword',
            },

            'path': {
                'type': 'keyword',
            },

            'image_uuid': {
                'type': 'keyword',
            },
        },
    },
}
