function H_a(m, K):
    """Hash function"""
    return int(hashlib.sha256(str(m | K).encode()).hexdigest(), 16)

function generate_large_prime(n):
    """This function generates a large prime number of n bits"""
    return randprime(2^(n-1), 2^n)

function encryption(m, r, g, h, n, K):
    """Encryption function"""
    return (pow(g, H_a(m, K), n^2) * pow(h, r, n^2)) % n^2

function initialize_bloom_filter(m_l, m_u, g, n, K):
    """Initialize bloom filter"""
    bloom_filter = set()
    for i in range(m_l, m_u + 1):
        bloom_filter.add(pow(g, H_a(i, K), n^2))
    return bloom_filter

function niec(m1, m2, kappa, m_l, m_u):
    """NIEC protocol"""
    p = generate_large_prime(kappa)
    q = generate_large_prime(kappa)
    n = p * q
    g = random_integer(1, n^2)
    h = pow(g, q, n^2)
    K = random_integer(1, 2^kappa)

    bloom_filter = initialize_bloom_filter(m_l, m_u, g, n, K)

    r1 = random_integer(1, n-1)
    r2 = random_integer(1, n-1)
    
    c1 = encryption(m1, r1, g, h, n, K)
    c2 = encryption(m2, r2, g, h, n, K)
    
    # Preprocessing
    c = (c1 * pow(c2, n^2 - 2, n^2)) % n^2
    
    # Comparison
    C = pow(c, p, n^2)
    
    if C == 1:
        return "m1 = m2"
    elif C in bloom_filter:
        return "m1 > m2"
    else:
        return "m1 < m2"


