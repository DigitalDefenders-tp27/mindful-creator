"""Device selection helper."""
import torch

# Automatically pick CUDA > MPS > CPU
device = torch.device("cuda" if torch.cuda.is_available() else  
                     "mps" if torch.backends.mps.is_available() else  
                     "cpu")

# Alias for imports
DEVICE = device