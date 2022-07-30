from setuptools import setup, find_packages
exec(open('venra/version.py').read())

setup(
  name = 'venra',
  packages = find_packages(exclude=[]),
  version = __version__,
  license='MIT',
  description = 'venra',
  author = 'Cody Collier',
  author_email = 'cody@telnet.org',
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/codycollier/venra',
  keywords = [
    'artificial intelligence',
    'information retrieval',
    'machine learning',
    'search',
  ],
  install_requires=[
    'packaging',
    'requests',
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
