from setuptools import setup

with open('pypi_desc.md') as f:
    long_description = f.read()

setup(
    name='banyanmonitorgui',
    version='1.0',
    packages=[
        'banyanmonitorgui',
    ],
    install_requires=[
        'pyzmq',
        'msgpack-python',
        'numpy>=1.9',
        'msgpack-numpy',
    ],

    entry_points={
        'console_scripts': [
            'bmg = banyanmonitorgui.banyan_monitor_gui:start_gui'
        ]
    },

    url='https://github.com/NoahMoscovici/banyanmonitorgui',
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    author='Noah Moscovici',
    author_email='noah.moscovici@gmail.com',
    description='A Graphical Monitor For Banyan Messages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['python banyan',],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Education',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: System :: Hardware'
    ],
)
