win = {
    '7':{
        'ie':['8','9','10','11'],
        'firefox':[str(x) for x in range(16,36)],
        'safari':['5.1'],
        'chrome':[str(x) for x in range(22,40)],
        'opera':['12.15','12.16']
    },  
    'xp':{
        'ie':['7','8'],
        'firefox':[str(x) for x in range(16,36)],
        'safari':['5.1'],
        'chrome':[str(x) for x in range(22,40)],
        'opera':['12.15','12.16']
    },  
    '8':{
        'ie':['10'],
        'firefox':[str(x) for x in range(16,36)],
        'safari':['5.1'],
        'chrome':[str(x) for x in range(22,40)],
        'opera':['12.15','12.16']
    },  
    '8_1':{
        'ie':['11'],
        'firefox':[str(x) for x in range(16,36)],
        'safari':['5.1'],
        'chrome':[str(x) for x in range(22,40)],
        'opera':['12.15','12.16']
    },
    'res':[('1024','768'),('1280','800'),('1280','1024'),('1366','768'),('1440','900'),('1680','1050'),('1600','1200'),('1920','1200'),('1920','1080'),('2048','1536')]
}
osx = {
    'yosemite':{
        'firefox':['3.6'] + [str(x) for x in range(4,36)],
        'safari':['8.0'],
        'chrome':[str(x) for x in range(14,40)],
        'opera':['12.15']
    },
    'mavericks':{
        'firefox':['3.6'] + [str(x) for x in range(4,36)],
        'safari':['7.0'],
        'chrome':[str(x) for x in range(14,40)],
        'opera':['12.15']
    },
    'mountain lion':{
        'firefox':['3.6'] + [str(x) for x in range(4,36)],
        'safari':['6.1'],
        'chrome':[str(x) for x in range(14,40)],
        'opera':['12.15']
    },
    'lion':{
        'firefox':['3.6'] + [str(x) for x in range(4,36)],
        'safari':['6.0'],
        'chrome':[str(x) for x in range(14,40)],
        'opera':['12.15']
    },
    'snow leopard':{
        'firefox':['3.6'] + [str(x) for x in range(4,36)],
        'safari':['5.1'],
        'chrome':[str(x) for x in range(14,40)],
        'opera':['12.15']
    },
    'res': [('1024','768'),('1280','960'),('1280','1024'),('1600','1200'),('1920','1080')]
}
ios = {
    'mobile':['iPhone 5S','iPhone 5C','iPhone 5'],
    'tablet':['iPad mini Retina','iPad Air','iPad 4th Gen']
}
android = {
   'mobile': {   'Google': ['Nexus 6', 'Nexus 5', 'Nexus 4', 'Nexus'],
                  'HTC': ['One M8', 'One X'],
                  'Motorola': ['Razr', 'Razr Maxx HD'],
                  'Samsung': [   'Galaxy S5',
                                 'Galaxy S4',
                                 'Galaxy S3',
                                 'Galaxy Note 2',
                                 'Galaxy Note 3',
                                 'Galaxy S5 Mini'],
                  'Sony': ['Xperia Tipo']},
    'tablet': {   'Amazon': [   'Kindle Fire 2',
                                'Kindle Fire HD 8.9',
                                'Kindle Fire HDX 7'],
                  'Google': ['Nexus 9', 'Nexus 7'],
                  'Samsung': ['Galaxy Tab 4 10.1', 'Galaxy Note 10.1']}}

tablet = {
    'Apple': ['iPad mini Retina','iPad Air','iPad 4th Gen'],
    'Amazon': [   'Kindle Fire 2',
                'Kindle Fire HD 8.9',
                'Kindle Fire HDX 7'],
   'Google': ['Nexus 9', 'Nexus 7'],
   'Samsung': ['Galaxy Tab 4 10.1', 'Galaxy Note 10.1']
}

mobile = {
    'Apple':['iPhone 5S','iPhone 5C','iPhone 5'],
    'Google': ['Nexus 6', 'Nexus 5', 'Nexus 4', 'Nexus'],
    'HTC': ['One M8', 'One X'],
    'Motorola': ['Razr', 'Razr Maxx HD'],
    'Samsung': [   'Galaxy S5',
                     'Galaxy S4',
                     'Galaxy S3',
                     'Galaxy Note 2',
                     'Galaxy Note 3',
                     'Galaxy S5 Mini'],
    'Sony': ['Xperia Tipo']
}
