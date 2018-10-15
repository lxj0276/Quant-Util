from distutils.core import setup
from distutils.extension import Extension

import numpy
from Cython.Distutils import build_ext

ext_modules = [
    Extension("rolling",
              ["rolling.pyx"],
              # libraries = ["m"],
              language="c++"
              )
]

setup(

    name="rolling",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
    include_dirs=[numpy.get_include()]
)
