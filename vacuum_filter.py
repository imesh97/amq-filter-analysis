import numpy as np
import hashlib

class VacuumFilter:
    def __init__(self, size, num_hashes=3, load_factor=0.95):
        """
        Initialize Vacuum Filter
        """
        self.size = size
        self.num_hashes = num_hashes
        self.load_factor = load_factor
        self.count_array = np.zeros(size, dtype=np.uint8)
        self.item_count = 0
    
    def _hash(self, item, seed):
        """
        Generate hash for item
        """
        hash_input = f"{seed}{item}".encode('utf-8')
        return int(hashlib.sha256(hash_input).hexdigest(), 16) % self.size
    
    def add(self, item):
        """
        Add item to Vacuum Filter
        """
        if self.item_count / self.size > self.load_factor:  # Check if resize is needed
            self._resize()
        
        added = False
        for i in range(self.num_hashes):  # Add item using multiple hash functions
            index = self._hash(item, i)
            if self.count_array[index] < 255:  # Prevent overflow
                self.count_array[index] += 1
                added = True
        
        if added:
            self.item_count += 1
        
        return added
    
    def _resize(self):
        """
        Resize the filter when load factor is exceeded
        """
        new_size = int(self.size * 1.5)
        new_count_array = np.zeros(new_size, dtype=np.uint8)
        
        for i in range(self.size):  # Rehash existing items
            if self.count_array[i] > 0:
                for _ in range(self.count_array[i]):  # Recreate an item for each count
                    rehash_item = f"rehash_{i}"
                    for j in range(self.num_hashes):
                        index = int(hashlib.sha256(f"{j}{rehash_item}".encode('utf-8')).hexdigest(), 16) % new_size
                        if new_count_array[index] < 255:
                            new_count_array[index] += 1
                            break
        
        self.size = new_size
        self.count_array = new_count_array
    
    def __contains__(self, item):
        """
        Check probable membership
        """
        return all(
            self.count_array[self._hash(item, i)] > 0
            for i in range(self.num_hashes)
        )