from setuptools import setup, find_packages

setup(
    name='questions',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask', 'flask_socketio'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
