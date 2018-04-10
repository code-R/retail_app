from setuptools import setup, find_packages

setup(
    name='retailstore',
    version='0.1',
    description='Retail Store Rest Api',
    url='http://github.com/code-R/retail_app',
    author='Vamsi - Vamsi Krishna',
    license='MIT',
    packages=find_packages(),
    package_data={
        '': ['data/*.csv'],
    },
    entry_points={
        'oslo.config.opts':
        'retailstore.conf = retailstore.conf.config:list_opts',
    },
)
