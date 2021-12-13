import os
import shutil
from glob import glob

import cv2 as cv
from PIL import Image, ImageEnhance, ImageOps

HIGH = './damage/high/'
MID = './damage/mid/'
LOW = './damage/low/'
basic_class = [HIGH, MID, LOW]


def classify_img(img_path: str):
    im = Image.open(img_path)
    w, h = im.size
    if w >= 1920:
        shutil.copy(img_path, HIGH + img_path.split('\\')[-1])
    elif 1280 <= w < 1920:
        shutil.copy(img_path, MID + img_path.split('\\')[-1])
    elif w < 1280:
        shutil.copy(img_path, LOW + img_path.split('\\')[-1])


def classify_precessing():
    img_list = glob('./damage/*.jpg') + glob('./damage/*.jpeg') + glob('./damage/*.png')
    print(len(img_list))

    if not (os.path.isdir(HIGH) and os.path.isdir(MID) and os.path.isdir(LOW)):
        print(':: not available folder => create folders')
        folders = [HIGH, MID, LOW]
        for fd in folders:
            try:
                os.mkdir(fd)
                print(':: now available folders')
            except FileExistsError:
                pass
    for img in img_list:
        classify_img(img)


def enhanced_processing(img_list: list, ehc_kind: str = None):
    i = 1
    for img_path in img_list:
        f_names = img_path.split('\\')[-1]
        enhanced_dir = img_path.split('\\')[0] + '/enhanced/'
        if not os.path.isdir(enhanced_dir):
            print(':: not available folder => create folders')
            os.mkdir(enhanced_dir)
            print(':: now available folder')

        sharp_dir = enhanced_dir + 'sharp/'
        clahe_dir = enhanced_dir + 'clahe/'
        if not os.path.isdir(sharp_dir):
            os.mkdir(sharp_dir)
        elif not os.path.isdir(clahe_dir):
            os.mkdir(clahe_dir)

        if ehc_kind.lower() == 'sharp':
            exif_im = ImageOps.exif_transpose(Image.open(img_path))
            ehc = ImageEnhance.Sharpness(exif_im)

            if os.path.isfile(sharp_dir + f_names):
                os.remove(sharp_dir + f_names)
            ehc.enhance(2.0).save(sharp_dir + f_names)
            print(f':: {i}/{len(img_list)}, {sharp_dir + f_names} {ehc_kind.lower()} enhanced and saved')
            i += 1
        elif ehc_kind.lower() == 'clahe':
            im = cv.imread(img_path)
            ycrcb = cv.cvtColor(im, cv.COLOR_BGR2YCrCb)
            y, cr, cb = cv.split(ycrcb)
            clahe = cv.createCLAHE()
            clahe_im = cv.merge([clahe.apply(y), cr, cb])
            clahe_result = cv.cvtColor(clahe_im, cv.COLOR_YCrCb2BGR)

            if os.path.isfile(clahe_dir + f_names):
                os.remove(clahe_dir + f_names)

            cv.imwrite(clahe_dir + f_names, clahe_result)
            print(f':: {i}/{len(img_list)}, {clahe_dir + f_names} {ehc_kind.lower()} enhanced and saved')
            i += 1


if __name__ == '__main__':
    # classify_precessing()
    # im = Image.open('./damage/1-00001.JPG')
    # enhancer = ImageEnhance.Sharpness(im)
    # enhancer.enhance(2.0).show('X2 Enhanced Sharpness')

    # test sharpness
    high_list = glob('./damage/high/*.*')
    enhanced_processing(high_list, ehc_kind='clahe')
