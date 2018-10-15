from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension( "rolling",
               ["rolling.pyx"],
               libraries = ["m"],
               language  = "c++"
    )
]

setup(
    name        = "rolling",
    cmdclass    = {"build_ext": build_ext},
    ext_modules = ext_modules,
)
