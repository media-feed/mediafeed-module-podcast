from setuptools import find_packages, setup


version = __import__('mediafeed_module_podcast').__version__
with open('README.rst', 'rb') as f:
    long_description = f.read().decode('utf-8')


setup(
    name='mediafeed-module-podcast',
    version=version,
    packages=find_packages(),

    install_requires=[
        'feedparser',
        'MediaFeed',
    ],

    author='Eduardo Klosowski',
    author_email='eduardo_klosowski@yahoo.com',

    description='Download de podcasts para o Media Feed',
    long_description=long_description,
    license='MIT',
    url='https://github.com/eduardoklosowski/mediafeed-module-podcast',

    entry_points={
        'console_scripts': [
            'mediafeed-module-podcast = mediafeed_module_podcast:main',
        ],
    },
)
