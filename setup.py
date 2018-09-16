from setuptools import setup

setup(
    name='buslane',
    version='0.0.1',
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Konrad Hałas',
    author_email='halas.konrad@gmail.com',
    packages=['buslane'],
    license='MIT',
    url='https://github.com/konradhalas/buslane',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
