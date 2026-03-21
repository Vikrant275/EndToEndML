from setuptools import setup,find_packages
from typing import List


HYPEN_E_DOT='-e .'
def get_requirements(filename_path:str)->List[str]:
    '''This funtion reuire list of requirements from requirements.txt'''

    with open(filename_path, 'r') as file:
        requirements = file.read().splitlines()

    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)

    return requirements



print(get_requirements('requirements.txt'))

setup(
    name='end2endml',
    version='0.0.1',
    author='Vikrant',
    description='End2End Machine Learning for Python',
    packages=find_packages(),
    requires=get_requirements('requirements.txt')
)
