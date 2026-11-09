import sys
import numpy as np

print("Python version:", sys.version.split()[0])
print("NumPy version:", np.__version__)

data = np.array([0.1, 0.5, 0.9], dtype=np.float32)

print("Array:", data)
print("Mean:", np.mean(data))
print("Validation successful!")
