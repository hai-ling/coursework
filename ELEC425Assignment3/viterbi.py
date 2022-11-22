X = [4,6,3]
V, Ptr = 0, 1
FAIR, LOADED = 0, 1
states = [FAIR, LOADED]
def pi(z):
    return 0.5
def z(z1,z2):
    return 0.6 if z1 == z2 else 0.4
    #return 0.95 if z1 == z2 else 0.05

def e(z,x):
    if z is FAIR:
        return 1/6
    elif z is LOADED:
        return 0.5 if x is 6 else 0.1

# initialize bugs
V = [[e(z_i,X[0])*pi(z_i) for z_i in states]]
Ptr = [[-1 for z_i in states]]
print(V[-1])
print(Ptr[-1])
def decode():
    for t in range(1, len(X)):
        # iteration
        x = X[t]
        v_t, p_t = list(), list()
        for z_k in states:
            candidates = list()
            for prev_z_k, a_k in enumerate(V[-1]):
                prob = e(z_k, x) * z(prev_z_k, z_k) * a_k
                candidates.append(prob)
            v_t.append(max(candidates))
            p_t.append(candidates.index(max(candidates)))
        print(v_t)
        print(p_t)
        V.append(v_t)
        Ptr.append(p_t)

def traceback():
    k = V[-1].index(max(V[-1]))
    path = list()
    for t in range(len(V)-1, -1, -1):
        k = Ptr[t][k]
        path.append(k)
    
    path.reverse()
    print(path)

decode()
traceback()
X = [6,3,1,2,4]
Z = [LOADED, FAIR, FAIR, LOADED, LOADED]
# X = [1, 2, 1, 5, 6, 2, 1, 5, 2, 4]
# Z = [FAIR for i in range(len(X))]

def calculate_probability():
    def s(x):
        return "LOAD" if x else "FAIR"
    prob = e(Z[0], X[0]) * pi(Z[0])
    print(f'1/2 * P({X[0]}|{s(Z[0])})', end='')
    for t in range(1, len(X)):
        print(f' * P({X[t]}|{s(Z[t])}) * P({s(Z[t])}|{s(Z[t-1])})', end='')
        prob *= e(Z[t], X[t]) * z(Z[t], Z[t-1])
    print(f' = {prob}')
#calculate_probability()
