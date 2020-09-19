from setuptools import setup, find_packages

setup(
  name='EpidemicEnv',
  version='0.0.1',
  description='Multi-Agent Epidemic Environment',
  url='https://github.com/covidmulator/EpidemicEnv',
  author='Taegeon Go',
  author_email='19sunrin134@sunrint.hs.kr',
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  install_requires=['gym', 'numpy-stl', 'ray']
)
