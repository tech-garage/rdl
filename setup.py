from setuptools import setup, find_packages

setup(
    name='questions',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask', 'flask_socketio', 'csv', 'random', 'json', 'jinja2', 'urllib.request', 'codecs',
    ],
)
