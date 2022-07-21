from setuptools import setup

setup(name='pytest-loop',
      version="1.0.3",
      description='pytest plugin for looping tests',
      long_description=open('README.rst').read(),
      author='Adam Nogowski',
      author_email='anogowski@live.com',
      url='https://github.com/anogowski/pytest-loop',
      py_modules=['pytest_loop'],
      entry_points={'pytest11': ['loop = pytest_loop']},
      setup_requires=['setuptools_scm'],
      install_requires=['pytest>=6'],
      license='Mozilla Public License 2.0 (MPL 2.0)',
      keywords='pytest pytest loop',
      python_requires='>=3.6',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Framework :: Pytest',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Utilities',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
      ])
