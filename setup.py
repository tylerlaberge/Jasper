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
    description='An asynchronous behaviour-driven development framework',
    keywords='python async asynchronous test-driven behaviour-driven development framework '
             'unittest testing assertion library bdd tdd tests test behaviour',
    url='https://github.com/tylerlaberge/Jasper',
    license='MIT'
)
