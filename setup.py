from cmakebuild import CMakeExtension, get_build_class, Generators
from setuptools import setup, find_packages
import os

path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join('README.md')) as file:
    README = file.read()

cmake_builder = get_build_class(make_program='C:/mingw64/bin/mingw32-make.exe',
                                c_compiler='C:/mingw64/bin/gcc.exe',
                                cxx_compiler='C:/mingw64/bin/g++.exe',
                                generator=Generators.mingw)

setup(
    name='simulator',
    packages=find_packages('simulator'),
    package_dir={'': 'simulator'},
    python_requires=">3.4",
    install_requires=['setuptools>=38.6.0',
                      'wheel>=0.31.0',
                      'twine>=1.11.0',
                      'PySerialization',
                      'numpy',
                      'scipy',
                      'matplotlib'],
    version='1.0',
    author='Vincent',
    author_email='vince.shores@outlook.com',
    url='https://github.com/vinceshores/burridgeknopoffsimulator',
    description='Simulation of 2-dimensional Burridge-Knopoff System',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    ext_modules=[CMakeExtension('burridgeknopoff', source_dir='burridgeknopofflib')],
    cmdclass=dict(build_ext=cmake_builder)
)
