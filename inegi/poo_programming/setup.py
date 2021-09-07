from setuptools import setup


setup(
    name='indicators-inegi',
    version='0.1',
    py_modules=['indicators-inegi'],
    install_requires=[
        'Click',
        'pandas',
        'tabulate',
    ],
    entry_points='''
        [console_scripts]
        indicators_inegi=indicators_inegi:ind
    ''',
)