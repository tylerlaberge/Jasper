from setuptools import setup
setup(
    name="Jasper",
    version="0.1",
    packages=['jasper',
              'features', 'features.arithmetic', 'features.arithmetic.steps'],
    entry_points={
        'console_scripts': [
            'jasper = jasper.entrypoints:jasper'
        ]
    }
)
