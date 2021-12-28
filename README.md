# 🧑‍🍳Chef MSG *(Mono-Sodium Glutamate)*

# Info
This is a simple **pre-processing** tool for image.

1. Chop-Chop your image like **kkakdugi** (delicious kimchi that shape like cube.)
   1. ```python
      def kkakdugi(img_path: str, size: int = 256, overlap: int = 1):
          ...
      ```
2. Physically split and shuffle the data(copy) in the directory like salad.
   1. ```python
      def salad(img_dir_path: str, test_size: float = 0.2, seed: Optional[int] = None,
                dir_names: (str, str) = ('train', 'valid')):
          ...
      ```
# Usage
```python
from chef_msg import stock
stock.kkakdugi()
stock.salad()
```
   