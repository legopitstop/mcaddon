import setuptools
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

required_modules = ['mclang']

setuptools.setup(
    name='mcaddon',
    version='0.0.1',
    author='Legopitstop',
    description='Minecraft: Bedrock Edition development kit',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/legopitstop/mcaddon/',
    packages=setuptools.find_packages(),
    install_requires=required_modules,
    license='MIT',
    keywords=['Minecraft: Bedrock Edition', 'mcpack', 'mcaddon', 'behaviorpack', 'resourcepack', 'JSON'],
    author_email='officiallegopitstop@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.6'
)