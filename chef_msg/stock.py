import os
import shutil
from pathlib import Path
from typing import Optional

import cv2 as cv
import numpy as np


def _check_kkakdugi_path(img_path: str, save_dir_name: str = 'dish') -> tuple(str, str):
    img_name = Path(img_path).name
    save_path = Path(save_dir_name) / img_name
    save_path.mkdir(parents=True, exist_ok=True)
    return img_name, save_path


def _is_factor_positive(size: int, overlap: int) -> bool:
    if size > 0 and overlap > 0:
        return True
    else:
        raise Exception('The factor(size, overlap) cannot be negative.')


def kkakdugi(img_path: str, size: int = 256, overlap: int = 1):
    """
    Cut the image into cubes like a kkakdugi.
    default size is 256px, overlap is 1 that meaning how much the image will overlap until the next image is cut.
    """

    if _is_factor_positive(size, overlap):
        img_name, save_dir = _check_kkakdugi_path(img_path)

        img = cv.imread(img_path)
        h, w, ch = img.shape
        print(f'[::INFO:: READ] {img_name} {img.shape}')

        max_w_count = int(w / size) * overlap
        max_h_count = int(h / size) * overlap
        w_offset = int((w - size) / max_w_count)
        h_offset = int((h - size) / max_h_count)
        w_chop_count, h_chop_count = max_w_count + 1, max_h_count + 1

        for h in range(h_chop_count):
            h0 = h * h_offset
            h1 = h0 + size
            for w in range(w_chop_count):
                w0 = w * w_offset
                w1 = w0 + size
                region = img[h0:h1, w0:w1]
                try:
                    cv.imwrite(
                        f'{save_dir}/{h:02d}_{w:02d}_{img_name}', region)
                except cv.error:
                    pass
                print(f'[::WORK:: SAVE] "{h:02d}_{w:02d}_{img_name}"')


def salad(img_dir_path: str, test_size: float = 0.2, seed: Optional[int] = None,
          dir_names: tuple(str, str) = ('train', 'valid')):
    """
    Physically split and shuffle the data(copy) in the directory like salad.
    default test size is 20%(0.2), seed is optional, default directory names 'train' and 'valid'.
    """
    path = Path(img_dir_path)
    files = list(path.glob('*.*'))

    if seed is not None:
        np.random.seed(seed)
    np.random.shuffle(files)
    test_index = np.round(len(files) * test_size)
    print(f'[::INFO:: {test_size * 100}% FILES : {int(test_index)}]')
    print(
        f'[::INFO:: {(1 - test_size) * 100}% FILES : {int(np.round(len(files))) - int(test_index)}]')

    for dir_name in dir_names:
        if not os.path.isdir(f'{dir_name}'):
            os.mkdir(f'{dir_name}')

    for i, file_path in enumerate(files):
        train_path = os.path.join(dir_names[0], Path(file_path).name)
        valid_path = os.path.join(dir_names[1], Path(file_path).name)
        if int(test_index) > i:
            shutil.copy(file_path, valid_path)
            print(f'[::WORK:: COPY "{file_path}" to "{valid_path}"]')
        else:
            shutil.copy(file_path, train_path)
            print(f'[::WORK:: COPY "{file_path}" to "{train_path}"]')
