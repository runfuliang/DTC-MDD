from sympy import isprime, randprime
from random import randint
import hashlib
import numpy as np

def H_a(m, K):
    """Hash function"""
    return int(hashlib.sha256((str(m) + str(K)).encode()).hexdigest(), 16)

def H_j(j, e, N):
    return int(hashlib.sha256((str(j) + str(e)).encode()).hexdigest(), 16) % N

def generate_large_prime(n):
    return randprime(2 ** (n-1), 2 ** n)

def encryption(m, r, g, h, n, K):
    return (pow(g, H_a(m, K), n**2) * pow(h, r, n**2)) % n**2

def initialize_bloom_filter(m_l, m_u, g, p, n, K, N, k):
    A = np.zeros(N, dtype=int)
    for m1 in range(m_l, m_u + 1):
        for m2 in range(m_l, m_u + 1):
            if m1 > m2:
                e = pow(g, p * (H_a(m1, K) - H_a(m2, K)), n**2)
                for j in range(1, k + 1):
                    A[H_j(j, e, N)] = 1
    return A

def compare(c1, c2, p, n, BF, N, k):
    c = (c1 * pow(c2, -1, n**2)) % n**2
    C = pow(c, p, n**2) % n**2
    if C == 1:
        return "m1 = m2"
    else:
        for j in range(1, k + 1):
            if BF[H_j(j, C, N)] == 0:
                return "m1 < m2"
        return "m1 > m2"

kappa = 256
m_l = 1
m_u = 100
N = 100
k = 5

p = generate_large_prime(kappa)
q = generate_large_prime(kappa)
n = p * q
g = n + 1
h = pow(g, q, n**2) 
K = randint(1, 2**kappa)

BF = initialize_bloom_filter(m_l, m_u, g, p, n, K, N, k)

m1 = 10
m2 = 11
r1 = randint(1, n-1)
r2 = randint(1, n-1)
c1 = encryption(m1, r1, g, h, n, K)
c2 = encryption(m2, r2, g, h, n, K)
