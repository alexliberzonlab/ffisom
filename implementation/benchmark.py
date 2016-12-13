from sage.rings.infinity import Infinity
from sage.arith.all import is_prime, is_prime_power
from sage.rings.integer_ring import ZZ
from sage.rings.finite_rings.integer_mod import Mod
from sage.rings.finite_rings.finite_field_constructor import GF

import sys
from sage.misc.misc import walltime, cputime

from ffisom import *
from sage.interfaces.magma import Magma

# p n (o, c) magma rains conic elliptic pari kummer
def benchmark(pbound = [3, 2**10], nbound = [3, 2**8], cbound = [1, Infinity], obound = [1, Infinity], loops = 10, tmax = Infinity, prime = False, even = False, check = False, fname = None, write = False, overwrite = False, verbose = True, skip_pari = False, skip_magma = False, skip_rains = False, skip_kummer = False):
    if write:
        mode = 'w' if overwrite else 'a'
        f = open(fname, mode, 0)
    else:
        f = sys.stdout
    pmin, pmax = pbound
    nmin, nmax = nbound
    omin, omax = obound
    cmin, cmax = cbound
    for p in xrange(pmin, pmax):
        p = ZZ(p)
        if not p.is_prime():
            continue
        for n in xrange(nmin, nmax):
            n = ZZ(n)
            if (prime == 1 and not is_prime(n)) or (prime == 2 and not is_prime_power(n)):
                continue
            if n % p == 0:
                continue
            if (not even) and (n % 2 == 0):
                continue
            q = p**n
            k = GF(q, name='z')
            kk = GF(q, modulus='random', name='z')
            k_flint = GF_flint(p, k.modulus(), name='z')
            o, G = find_root_order(p, [n, n], n, verbose=False)
            m = G[0][0].parent().order()
            c = Mod(p,n).multiplicative_order()
            if verbose:
                print("p = {}, n = {}, (o = {}, c = {})".format(p, n, o, c))
            # Magma
            tloops = 0
            for l in xrange(loops):
                if skip_magma:
                    break
                if (o > omax) or (o == p):
                    break
                # let's assume that launching a new Magma instance is cheaper
                # than computing random irreducible polynomials
                M = Magma()
                try:
                    k_magma = M(k)
                    kk_magma = M(kk)
                    t = walltime()
                    k_magma.Embed(kk_magma, nvals=0)
                    tloops += walltime(t)
                except TypeError:
                    # sage/magma interface sometimes gets confused
                    pass
                finally:
                    M.quit()
                if tloops > tmax:
                    break
            tmagma = tloops / (l+1)
            # Rains algorithms
            trains = []
            tloops = 0
            for l in xrange(loops):
                if skip_rains:
                    break
                if (o > omax) or (o == p):
                    break
                try:
                    t = walltime()
                    a, b = find_gens_cyclorains(k_flint, k_flint, use_lucas = False)
                    tloops += walltime(t)
                except RuntimeError:
                    pass
                if check and (l == 0 or check > 1):
                    g = a.minpoly()
                    if g.degree() != n:
                        raise RuntimeError("wrong degree")
                    if g != b.minpoly():
                        raise RuntimeError("different minpolys")
                if tloops > tmax:
                    break
            trains.append(tloops / (l+1))
            tloops = 0
            for l in xrange(loops):
                if skip_rains:
                    break
                if (o != 2) or (o > omax) or (o == p):
                    break
                try:
                    t = walltime()
                    a, b = find_gens_cyclorains(k_flint, k_flint, use_lucas = True)
                    tloops += walltime(t)
                except RuntimeError:
                    pass
                if check and (l == 0 or check > 1):
                    g = a.minpoly()
                    if g.degree() != n:
                        raise RuntimeError("wrong degree")
                    if g != b.minpoly():
                        raise RuntimeError("different minpolys")
                if tloops > tmax:
                    break
            trains.append(tloops / (l+1))
            tloops = 0
            for l in xrange(loops):
                if skip_rains:
                    break
                try:
                    t = walltime()
                    a, b = find_gens_ellrains(k_flint, k_flint)
                    tloops += walltime(t)
                except RuntimeError:
                    pass
                if check and (l == 0 or check > 1):
                    g = a.minpoly()
                    if g.degree() != n:
                        raise RuntimeError("wrong degree")
                    if g != b.minpoly():
                        raise RuntimeError("different minpolys")
                if tloops > tmax:
                    break
            trains.append(tloops / (l+1))
            # PARI/GP
            tloops = 0
            for l in xrange(loops):
                if skip_pari:
                    break
                if c < cmin or c > cmax:
                    break
                t = walltime()
                a, b = find_gens_pari(k, k)
                tloops += walltime(t)
                if check and (l == 0 or check > 1):
                    g = a.minpoly()
                    if g.degree() != n:
                        raise RuntimeError("wrong degree")
                    if g != b.minpoly():
                        raise RuntimeError("different minpolys")
                if tloops > tmax:
                    break
            tpari = tloops / (l+1)
            # Kummer algorithms
            tkummer = []
            # only linalg and modcomp implemented for c==1
            for algo in kummer_algolist[2*(c==1):-2*(c==1)-1]:
                tloops = 0
                for l in xrange(loops):
                    if skip_kummer:
                        break
                    if c < cmin or c > cmax:
                        break
                    t = walltime()
                    a, b = find_gens_kummer(k_flint, k_flint, n, algo)
                    tloops += walltime(t)
                    if check and (l == 0 or check > 1):
                        g = a.minpoly()
                        if g.degree() != n:
                            raise RuntimeError("wrong degree")
                        if g != b.minpoly():
                            raise RuntimeError("different minpolys")
                    if tloops > tmax:
                        break
                tkummer.append(tloops / (l+1))
            tkummer = 2*(c == 1)*[0] + tkummer + 2*(c == 1)*[0]
            f.write(("{} {} ({}, {})" + " {}" + " {}"*len(trains) + " {}" + " {}"*len(tkummer)+"\n").format(p, n, o, c, *([tmagma] + trains + [tpari] + tkummer)))
    if write:
        f.close()
