import hashlib
import random

class CuckooFilter:
    def __init__(self, size, max_kicks=500):
        """
        Initialize Cuckoo Filter
        """
        self.size = size
        self.buckets = [None] * size
        self.max_kicks = max_kicks
    
    def _hash(self, item):
        """
        Generate primary hash
        """
        hash_value = hashlib.sha256(str(item).encode('utf-8')).hexdigest()
        return int(hash_value, 16) % self.size
    
    def _alt_hash(self, index):
        """
        Generate alternative hash index
        """
        hash_value = hashlib.sha256(str(index).encode('utf-8')).hexdigest()
        return int(hash_value, 16) % self.size
    
    def add(self, item):
        """
        Add item to Cuckoo Filter
        """
        index = self._hash(item)
        
        if self.buckets[index] is None:  # Try first bucket
            self.buckets[index] = item
            return True
        
        alt_index = self._alt_hash(index)  # Try alternate bucket
        if self.buckets[alt_index] is None:
            self.buckets[alt_index] = item
            return True
        
        for _ in range(self.max_kicks):  # Kickout strategy
            swap_index = index if random.random() < 0.5 else alt_index
            
            item, self.buckets[swap_index] = self.buckets[swap_index], item
            
            index = self._hash(item)
            alt_index = self._alt_hash(index)
            
            if self.buckets[index] is None:
                self.buckets[index] = item
                return True
            if self.buckets[alt_index] is None:
                self.buckets[alt_index] = item
                return True
        
        return False
    
    def __contains__(self, item):
        """
        Check probable membership
        """
        index = self._hash(item)
        alt_index = self._alt_hash(index)
        
        return (self.buckets[index] == item or 
                self.buckets[alt_index] == item)