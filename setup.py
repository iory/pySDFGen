from __future__ import print_function

import shlex
import subprocess
import sys

from setuptools import find_packages


version = '0.2.1'


if sys.argv[-1] == 'release':
    # Release via github-actions.
    commands = [
        'git tag v{:s}'.format(version),
        'git push origin main --tag',
    ]
    for cmd in commands:
        print('+ {}'.format(cmd))
        subprocess.check_call(shlex.split(cmd))
    sys.exit(0)

setup_requires = [
]

install_requires = [
    'trimesh>=3.5.20'
]

setup_params = dict(
    name="pysdfgen",
    version=version,
    description="SDFGen for Python",
    author='iory',
    author_email='ab.ioryz@gmail.com',
    url='https://github.com/iory/pySDFGen',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=find_packages(include=["pysdfgen", "pysdfgen.*"]),
    package_data={'pysdfgen': ['__init__.py', 'SDFGen']},
    setup_requires=setup_requires,
    install_requires=install_requires,
    include_package_data=False,
)


def main():
    import skbuild  # NOQA

    skbuild.setup(**setup_params)


if __name__ == '__main__':
    main()
