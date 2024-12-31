import unittest

import numpy as np

from py_limit_memory import limit_memory


class Test(unittest.TestCase):
    def test(self):
        """check if decorator works only for the function it decorates"""

        size_in_bytes = 2 * 1024**3  # 2 GB in bytes
        dtype_size = np.dtype(np.float64).itemsize
        num_elements = size_in_bytes // dtype_size

        @limit_memory("1GB")
        def f1():
            array = np.empty(num_elements, dtype=np.float64)

        def f2():
            array = np.empty(num_elements, dtype=np.float64)

        f2()

        self.assertRaises(MemoryError, f1)


if __name__ == "__main__":
    unittest.main()
