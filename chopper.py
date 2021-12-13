from pathlib import Path

import cv2 as cv


def cut(img_path: str, size=256, overlap_factor=1):
    img_name = Path(img_path).name
    save_dir = Path('./chopped') / img_name
    save_dir.mkdir(parents=True, exist_ok=True)

    img = cv.imread(img_path)
    w, h, ch = img.shape
    print(f':: image read {img.shape}')

    if overlap_factor > 0:
        max_h_count = int(w / size) * overlap_factor
        w_offset = int((w - size) / max_h_count)
        w_chop_count = max_h_count + 1

        max_h_count = int(h / size) * overlap_factor
        h_offset = int((h - size) / max_h_count)
        h_chop_count = max_h_count + 1

        for y in range(h_chop_count):
            y0 = y * h_offset
            y1 = y0 + size
            for x in range(w_chop_count):
                x0 = x * w_offset
                x1 = x0 + size
                region = img[y0:y1, x0:x1]
                try:
                    cv.imwrite(f'{save_dir}/{y:02d}_{x:02d}_{img_name}', region)
                except cv.error:
                    pass
                print(f':: "{y:02d}_{x:02d}_{img_name}" saved.')
