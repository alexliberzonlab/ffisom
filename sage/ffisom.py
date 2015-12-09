#from sage.env import sage_include_directories
#include_dirs = sage_include_directories(use_sources=True)
#import pyximport
#pyximport.install(setup_args={'include_dirs': include_dirs})

from rains import find_gens as find_gens_cyclo
from ellrains import find_gens as find_gens_ell
from pari_ffisom import find_gens as find_gens_pari
from javad_nmod import find_gens as find_gens_javad
