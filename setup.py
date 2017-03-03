from setuptools import setup
setup(
    name="Jasper",
    version="0.1",
    packages=['jasper'],
    entry_points={
        'console_scripts': [
            'jasper = jasper.entrypoints:jasper'
        ]
    },
    install_requires=['click==6.7', 'termcolor==1.1.0', 'tqdm==4.11.2', 'colorama==0.3.7'],
    author='Tyler LaBerge',
    author_email='tyler.laberge@maine.edu',
    description='An asynchronous behavior-driven development framework',
    keywords='python async asynchronous test test-driven-development behavior behavior-driven-development tdd bdd '
             'testing test-automation test-framework testing-tools tests framework library',
    url='https://github.com/tylerlaberge/Jasper',
    license='MIT'
)

