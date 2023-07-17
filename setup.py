import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='alphatrade',
    packages=setuptools.find_packages(),
    version='1.0.0',
    include_package_data=True,
    description='Python APIs for SAS Online Alpha Trade Web Platform',
    long_description=long_description,
    long_description_content_type='text/markdown',  author='Algo 2 Trade',
    author_email='help@algo2.trade',
    url='https://github.com/algo2t/alphatrade',
    install_requires=['setuptools==57.5.0','requests', 'websocket_client', 'protlib', 'pandas','pyotp'],
    keywords=['alphatrade', 'alpha-trade', 'sasonline',
              'python', 'sdk', 'trading', 'stock markets'],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries'
    ],
)
