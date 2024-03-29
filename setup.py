import setuptools

with open('README.md', encoding='UTF-8') as f:
    long_description = f.read()
with open('requirements.txt', encoding='UTF-8') as f:
    requires = f.read().splitlines()

setuptools.setup(
    name='spys',
    version='1.1.0',
    author='Nikita (NIKDISSV)',
    author_email='nikdissv@proton.me',
    description='Python API for spys.one/spys.me proxies',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NIKDISSV-Forever/PySpysAPI',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Typing :: Typed',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
    ],
    python_requires='>=3.8',
)
