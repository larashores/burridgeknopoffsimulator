import os
import subprocess
import enum

from setuptools import Extension
from setuptools.command.build_ext import build_ext


class Generators(enum.Enum):
    mingw = 'MinGW Makefiles'
    code_blocks_mingw = 'CodeBlocks - MinGW Makefiles'
    code_lite_mingw = 'CodeLite - MinGW Makefiles'
    sublime_mingw = 'Sublime Text 2 - MinGW Makefiles'
    kate_mingw = 'Kate - MinGW Makefiles'
    eclipse = 'Eclipse CDT4 - MinGW Makefiles'


class CMakeExtension(Extension):
    def __init__(self, name, *, target='all', source_dir=''):
        Extension.__init__(self, name, sources=[])
        self.source_dir = os.path.abspath(source_dir)
        self.target = target


def get_build_class(make_program, c_compiler, cxx_compiler, generator, commands=[]):
    class CMakeBuild(build_ext):
        def run(self):
            try:
                subprocess.check_output(['cmake', '--version'])
            except OSError:
                extensions_string = ", ".join(e.name for e in self.extensions)
                raise RuntimeError("CMake must be installed to build the following extensions: " + extensions_string)

            self.build_extensions()

        def build_extension(self, ext):
            build_type = 'Debug' if self.debug else 'Release'
            build_directory = os.path.join(ext.source_dir, 'cmake-build-' + build_type)
            if not os.path.exists(build_directory):
                os.mkdir(build_directory)

            cmake_args = ['cmake']
            cmake_args.append('-DCMAKE_BUILD_TYPE=' + build_type)
            cmake_args.append('-DCMAKE_MAKE_PROGRAM=' + make_program)
            cmake_args.append('-DCMAKE_C_COMPILER=' + c_compiler)
            cmake_args.append('-DCMAKE_CXX_COMPILER=' + cxx_compiler)
            cmake_args.append('-G "{}"'.format(generator.value))
            cmake_args.extend(commands)
            cmake_args.append('"{}"'.format(ext.source_dir))

            build_args = ['cmake']
            build_args.append('--build "{}"'.format(build_directory))
            build_args.append('--target {}'.format(ext.target))
            build_args.append('--')
            build_args.append('-j 4')

            install_args = ['cmake']
            install_args.append('--build "{}"'.format(build_directory))
            install_args.append('--target install')
            install_args.append('--')
            install_args.append('-j 4')

            cmake_command = ' '.join(cmake_args)
            build_command = ' '.join(build_args)
            install_command = ' '.join(install_args)

            subprocess.check_call(cmake_command, cwd=build_directory)
            subprocess.check_call(build_command, cwd=build_directory)
            subprocess.check_call(install_command, cwd=build_directory)

    return CMakeBuild
