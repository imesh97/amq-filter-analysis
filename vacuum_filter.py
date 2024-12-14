import numpy as np
import hashlib

class VacuumFilter:
    def __init__(self, n, load_factor=0.95):
        """
        Initialize Vacuum Filter
        """
        self.slots_per_bucket = 4  # Initialize parameters (load factor is 0.95 by default)
        self.n = n
        self.load_factor = load_factor
        
        self.alternate_ranges = self._init_alternate_ranges(n, load_factor)
        self.m = int(np.ceil(self._calculate_buckets(n, load_factor)))  # Calculate number of buckets (using int casting)
        self.table = [[] for _ in range(self.m)]
    
    def _hash(self, item):
        """
        Generate hash for an item using SHA-256
        """
        hash_obj = hashlib.sha256(str(item).encode())
        return int.from_bytes(hash_obj.digest()[:4], byteorder='big')
    
    def _fingerprint(self, item):
        """
        Generate fingerprint for an item
        """
        hash_obj = hashlib.sha256(str(item).encode())
        return int.from_bytes(hash_obj.digest()[:4], byteorder='big')
    
    def _init_alternate_ranges(self, n, load_factor):
        """
        Initialize alternate ranges
        """
        alternate_ranges = []
        for i in range(4):
            ar = self._range_selection(n, load_factor, 1 - i/4)  # Calculate alt ranges for different groups of items
            alternate_ranges.append(ar)
        
        alternate_ranges[3] *= 2  # Double the smallest alt range to avoid failures
        
        return alternate_ranges
    
    def _range_selection(self, n, load_factor, ratio):
        """
        Select appropriate alt range size
        """
        L = 1
        while not self._load_factor_test(n, load_factor, ratio, L):
            L *= 2
        return L
    
    def _load_factor_test(self, n, load_factor, ratio, L):
        """
        Test if a given alt range can achieve target load factor
        """
        m = int(np.ceil(n / (4 * load_factor * L))) * L  # Number of buckets (using int casting)
        c = m // L  # Number of chunks
        D = (n / c) + 1.5 * np.sqrt(2 * (n / c) * np.log(c))  # Estimated max load
        P = 0.97 * 4 * L  # Capacity lower bound of each chunk
        
        return D < P
    
    def _calculate_buckets(self, n, load_factor):
        """
        Calculate the number of buckets needed
        """
        L = self.alternate_ranges[0]  # Select largest alt range for calculation
        return np.ceil(n / (4 * load_factor * L)) * L
    
    def _map(self, x, m):
        """
        Uniformly maps hash value from 0 to m-1
        """
        return ((x * m) >> 32) % m
    
    def _alternate(self, bucket, fingerprint):
        """
        Compute current alt bucket
        """
        l = self.alternate_ranges[fingerprint % 4]  # Current alt range
        delta_hash = hashlib.sha256(str(fingerprint).encode())  # Calculate delta
        delta = int.from_bytes(delta_hash.digest()[:4], byteorder='big') % l
        
        return (bucket ^ delta) % self.m  # XOR to get alternate bucket
    
    def _alternate_small_key(self, bucket, m):
        """
        Alt function for small number of keys (< 2^18)
        """
        delta_hash = hashlib.sha256(str(bucket).encode())  # Calculate delta
        delta = int.from_bytes(delta_hash.digest()[:4], byteorder='big') % m
        
        b_prime = (bucket - delta) % m  # Calculate alt bucket index
        b_prime = (m - 1 - b_prime + delta) % m
        
        return b_prime
    
    def insert(self, item):
        """
        Insert an item into the Vacuum Filter
        """
        f = self._fingerprint(item)  # Generate fingerprint and initial buckets
        b1 = self._map(self._hash(item), self.m)
        b2 = self._alternate(b1, f)
        
        
        if len(self.table[b1]) < self.slots_per_bucket:  # If either bucket is empty, then insert
            self.table[b1].append(f)
            return True
        if len(self.table[b2]) < self.slots_per_bucket:
            self.table[b2].append(f)
            return True
        
        max_evicts = 500  # Eviction process (max = 500 to avoid infinite loop)
        current_bucket = np.random.choice([b1, b2])  # Randomly select bucket B1 or B2
        current_fingerprint = f
        
        for _ in range(max_evicts):
            for existing_f in self.table[current_bucket]:  # Extend search scope
                alt_bucket = self._alternate(current_bucket, existing_f)
                if len(self.table[alt_bucket]) < self.slots_per_bucket:
                    self.table[alt_bucket].append(existing_f)  # Evict existing fingerprint
                    self.table[current_bucket].remove(existing_f)
                    self.table[current_bucket].append(current_fingerprint)
                    return True
            
            evict_index = np.random.randint(0, self.slots_per_bucket)  # Random eviction if no empty slots found
            evicted_f = self.table[current_bucket][evict_index]
            self.table[current_bucket][evict_index] = current_fingerprint
            
            current_bucket = self._alternate(current_bucket, evicted_f)  # B = Alt(B, f)
            current_fingerprint = evicted_f
        
        return False
    
    def delete(self, item):
        """
        Delete an item from the Vacuum Filter
        """
        f = self._fingerprint(item)  # Generate fingerprint and candidate buckets
        b1 = self._map(self._hash(item), self.m)
        b2 = self._alternate(b1, f)
        
        if f in self.table[b1]:  # If fingerprint exists in two candidate buckets, then delete
            self.table[b1].remove(f)
            return True
        if f in self.table[b2]:
            self.table[b2].remove(f)
            return True
        
        return False
    
    def __contains__(self, item):
        """
        Check probable membership
        """
        f = self._fingerprint(item)  # Generate fingerprint
        b1 = self._map(self._hash(item), self.m)  # Calculate two candidate buckets
        b2 = self._alternate(b1, f)
        
        return f in self.table[b1] or f in self.table[b2]  # Check if fingerprint found in either candidate bucket