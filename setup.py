from cx_Freeze import setup, Executable
import sys

build_exe_options = {

    'zip_include_packages': ['pygame==2.5.2'],
    'include_files': ['config.json', 'data', 'icon.png', 'sound'],
    'build_exe': 'build/usr/local/games/snakeOdyssey'

}

setup(

    name='snakeOdyssey',
    version='1.0.0',
    options={'build_exe': build_exe_options},
    executables=[Executable('main.py', base='gui')]

)