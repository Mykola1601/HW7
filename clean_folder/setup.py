from setuptools import setup

setup(name='clean_folder',
      version='0.1.16',
      description='useful code',
      url='https://github.com/Mykola1601/HW7/tree/main/clean_folder',
      author='MIKOLA',
      # license='MIT',
      packages=['clean_folder'],
      entry_points = {'console_scripts':['go = clean_folder.sort:sort' ]  }
      )