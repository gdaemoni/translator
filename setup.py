from setuptools import setup, find_packages

setup(
	name='translator',
	description='Translates words and sentences using Google Translator. Formats the translated words and saves them to a file for import into anki.',
	version='0.1',
	packages=find_packages(),
	url='',
	license='',
	author='gdaemoni',
	author_email='kon4ena.rega@gmail.com',
	entry_points={
					'console_scripts': [ 
						'translator = translator.main:main'
						]
					},
)
