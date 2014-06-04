from setuptools import setup, find_packages


requires = [
]


setup(
    name='pypnm',
    version='',
    packages=find_packages(),
    url='',
    license='Apache v2',
    author='cocu',
    author_email='cocu.436f6375@gmail.com',
    description='',
    test_suite='tests',
    extras_require = {
        'for fast calculation': ['numpy']
    }
)
