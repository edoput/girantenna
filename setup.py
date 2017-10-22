from setuptools import setup

setup(
    name='girantenna',
    version='0.0.0',
    description='web interface to a stepper motor',
    author='Edoardo Putti',
    url='https://github.com/EdoPut/girantenna',
    license='GPL3',
    packages=[
        'girantenna',
    ],
    install_requires=[
        'flask-wtf',
        'wiringpi',
    ],
    zip_safe=False
)
