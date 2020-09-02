from setuptools import setup

setup(
    name='jack_web',
    version='0.0.3',
    packages=['jack_web'],
    author="Lukas Jurk",
    author_email="ljurk@pm.me",
    description="a webinterface to patch jack connections",
    long_description=open('readme.md').read(),
    long_description_content_type="text/markdown",
    license="GPLv3",
    keywords="jack jack2 patchbay",
    url="https://github.com/ljurk/jack-web-patchbay",
    entry_points={
        'console_scripts': ['jack_web=jack_web.__main__:main']
    },
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-restful"
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ]
)
