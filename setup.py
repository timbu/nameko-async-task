from setuptools import setup, find_packages

setup(
    name='nameko-async-task',
    version='0.0.1',
    description='Async task utility for nameko services',
    author='timbu',
    url='http://github.com/timbu/nameko-async-task',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        "nameko==3.0.0-rc5",  # TODO: require nameko 3 only when released
    ],
    extras_require={
        'dev': [
            "coverage==4.0.3",
            "flake8==2.5.4",
            "pylint==1.5.5",
            "pytest==3.0.5",
        ]
    },
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
