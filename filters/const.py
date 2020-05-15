'''
定数定義
'''

FILTER_NAME2PK = {
    'blur': 2,
    'gray':3,
    } #nameとpkの対応表

FILTER_PK2NAME = {
    2: 'blur',
    3: 'gray',
}

BLUR = 'blur'
GRAY = 'gray'

#OTHER_ID = 24 
OTHER_ID = 4

SAMPLE_IMG_SRC = '/filters/image/sample/lena.jpg'

SAMPLE_IMG_OPT = {
    'blur': '/filters/image/sample/blur.jpg',
    'gray': '/filters/image/sample/gray.jpg',
    }

SUPPORT_EXT = [
    '.bmp', '.dib', '.pbm', '.pgm', '.ppm', '.pnm', '.sr',
    '.ras', '.jpeg', '.jpg', '.jpe', '.jp2', '.png', '.tiff', '.tif'
    ]