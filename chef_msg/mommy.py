from pathlib import Path

import cv2 as cv


def _check_path(img_path: str, save_dir_name: str = 'dish') -> (str, str):
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
    chop image
    """

    if _is_factor_positive(size, overlap):
        img_name, save_dir = _check_path(img_path)

        img = cv.imread(img_path)
        w, h, ch = img.shape
        print(f'[INFO::READ] {img_name} {img.shape}')

        max_w_count, max_h_count = int(w / size) * overlap, int(h / size) * overlap
        w_offset, h_offset = int((w - size) / max_w_count), int((h - size) / max_h_count)
        w_chop_count, h_chop_count = max_w_count + 1, max_h_count + 1

        for h in range(h_chop_count):
            h0 = h * h_offset
            h1 = h0 + size
            for w in range(w_chop_count):
                w0 = w * w_offset
                w1 = w0 + size
                region = img[h0:h1, w0:w1]
                try:
                    cv.imwrite(f'{save_dir}/{h:02d}_{w:02d}_{img_name}', region)
                except cv.error:
                    pass
                print(f'[WORK::SAVE] "{h:02d}_{w:02d}_{img_name}"')
