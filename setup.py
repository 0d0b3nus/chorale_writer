from setuptools import setup

setup(name='regis',
      version='0.1',
      description='A basic music theory library',
      url='https://github.com/dtrifuno/regis',
      author='Darko Trifunovski',
      author_email='dtrifuno@gmail.com',
      license='GPL3',
      packages=['regis'],
      install_requires=[
        'mido'
      ],
      zip_safe=False)
