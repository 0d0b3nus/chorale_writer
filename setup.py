from setuptools import setup

setup(name='regis',
      version='0.1',
      description='',
      url='https://github.com/dtrifuno/regis',
      author='Darko Trifunovski',
      author_email='dtrifuno@gmail.com',
      license='GPL3',
      packages=['regis'],
      install_requires=[
        'markovify',
        'PyQt5',
        'mido'
      ],
      zip_safe=False)
