from setuptools import setup

setup ( name='clean_folder',
      version='0.1.15',
      version='0.1.4',
      description='useful code',
      url='https://github.com/Mykola1601/HW7/tree/main/clean_folder',
      author='MIKOLA',
      # author_email='fly@example.com',
      license='MIT',
      packages=['clean_folder']
      entry_points = {'console_scripts':['go = clean_folder.sort:sort' ]  }
      )