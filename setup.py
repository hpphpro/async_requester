# -*- coding: utf-8 -*-
from pathlib import Path 
from setuptools import setup

setup_requirements = Path('requirements.txt').read_text(encoding='utf-8').split()

setup(
    name='async_requester',
    version='0.1',
    author='hpph',
    author_email='',
    packages=['async_requester'],
    url='https://github.com/hpphpro/async_requester',
    description='Asynchronous requests template',
    keywords=['asyncio', 'aiohttp', 'io', 'requests'],
    long_description=Path('README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown', 
    zip_safe=False,
    include_package_data=True,
    python_requires='>=3.10',
    use_scm_version=True,
    setup_requires=setup_requirements + ['setuptools_scm']
)