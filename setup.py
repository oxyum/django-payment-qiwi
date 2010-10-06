
from setuptools import setup

setup(
    name='django-payment-qiwi',
    version=__import__('qiwi').__version__,
    description='Qiwi SOAP Interface support for Django.',
    author='Ivan Fedorov',
    author_email='oxyum@oxyum.ru',
    url='http://code.google.com/p/django-payment-qiwi/',
    packages=['qiwi',],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires=[
      'django',
      'suds',
      'soaplib',
    ],
    include_package_data=True,
    zip_safe=False,
)
