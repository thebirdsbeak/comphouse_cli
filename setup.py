from setuptools import setup

setup(
    name="compad",
    version='0.1',
    py_modules=[''],
    install_requires=[
        'Click',
        'pyperclip',
        'requests',
        'bs4',
    ],
    entry_points='''
        [console_scripts]
        compad=compad:company_details
    ''',
)
