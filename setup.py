from setuptools import setup
setup(
    name="Jasper",
    version="0.1",
    packages=['jasper'],
    entry_points={
        'console_scripts': [
            'jasper = jasper.entrypoints:jasper'
        ]
    }
)
