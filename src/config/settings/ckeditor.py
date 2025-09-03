customColorPalette = [
    {
        'color': 'hsl(0, 0%, 0%)',
        'label': 'Black'
    },
    {
        'color': 'hsl(0, 0%, 30%)',
        'label': 'Dark Grey'
    },
    {
        'color': 'hsl(0, 0%, 60%)',
        'label': 'Grey'
    },
    {
        'color': 'hsl(0, 0%, 90%)',
        'label': 'Light Grey'
    },
    {
        'color': 'hsl(0, 0%, 100%)',
        'label': 'White'
    },
    {
        'color': 'hsl(0, 75%, 60%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(30, 75%, 60%)',
        'label': 'Orange'
    },
    {
        'color': 'hsl(60, 75%, 60%)',
        'label': 'Yellow'
    },
    {
        'color': 'hsl(90, 75%, 60%)',
        'label': 'Light Green'
    },
    {
        'color': 'hsl(120, 75%, 60%)',
        'label': 'Green'
    },
    {
        'color': 'hsl(150, 75%, 60%)',
        'label': 'Aquamarine'
    },
    {
        'color': 'hsl(180, 75%, 60%)',
        'label': 'Turquoise'
    },
    {
        'color': 'hsl(210, 75%, 60%)',
        'label': 'Light Blue'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
    {
        'color': 'hsl(240, 75%, 60%)',
        'label': 'Navy'
    },
    {
        'color': 'hsl(270, 75%, 60%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(300, 75%, 60%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(330, 75%, 60%)',
        'label': 'Magenta'
    }
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', '|',
                        'imageStyle:alignLeft', 'imageStyle:alignRight',
                        'imageStyle:alignCenter', 'imageStyle:side', '|',
                        'resizeImage:50', 'resizeImage:75', 'resizeImage:original'],
            'styles': ['alignLeft', 'alignRight', 'alignCenter', 'full', 'side'],
            'resizeOptions': [
                {
                    'name': 'resizeImage:original',
                    'value': None,
                    'icon': 'original'
                },
                {
                    'name': 'resizeImage:50',
                    'value': '50',
                    'icon': 'small'
                },
                {
                    'name': 'resizeImage:75',
                    'value': '75',
                    'icon': 'medium'}
            ]
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells', '|',
                'tableProperties', 'tableCellProperties'
            ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette,
                'defaultProperties': {
                    'alignment': 'center',
                    'width': '100%',
                    'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderColor': 'hsl(207, 90%, 54%)',  # Default blue
                    'backgroundColor': 'hsl(0, 0%, 100%)'  # Default white
                }
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette,
                'defaultProperties': {
                    'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderColor': 'hsl(0, 0%, 90%)'  # Default light grey
                }
            }
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'},
                {'model': 'heading4', 'view': 'h4', 'title': 'Heading 4', 'class': 'ck-heading_heading4'},
                {'model': 'heading5', 'view': 'h5', 'title': 'Heading 5', 'class': 'ck-heading_heading5'},
                {'model': 'heading6', 'view': 'h6', 'title': 'Heading 6', 'class': 'ck-heading_heading6'},
            ]
        },  # Corrected missing comma
        'codeBlock': {
            'languages': [
                {'language': 'plaintext', 'label': 'Plain text'},
                {'language': 'javascript', 'label': 'JavaScript'},
                {'language': 'python', 'label': 'Python'},
                {'language': 'html', 'label': 'HTML'},
                {'language': 'css', 'label': 'CSS'},
            ]
        },
        'list': {
            'properties': {
                'styles': 'true',
                'startIndex': 'true',
                'reversed': 'true',
            },
        },
    },
}
