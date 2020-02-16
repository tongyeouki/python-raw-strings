from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [elem.strip() for elem in open('requirements.txt', 'r').readlines()]

setup_requirements = []

test_requirements = []

setup(
    author="p2m3ng",
    author_email='contact@p2m3ng.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python tool to handle raw strings",
    entry_points={
        'console_scripts': [
            'cli=cli:cli',
        ],
    },
    install_requires=requirements,
    include_package_data=True,
    keywords='',
    license=open("LICENSE").read(),
    long_description=readme + "\n\n",
    platforms='any',
    name='python-raw-strings',
    packages=find_packages(include=['raw_strings', "tests"]),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/p2m3ng/python-raw-strings',
    version="1.0.0",
    zip_safe=False,
)
