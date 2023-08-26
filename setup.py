from setuptools import setup, find_packages

exec(open('venra/__version__.py').read())

with open("README.md", mode="r", encoding="utf-8") as f:
    readme_contents = f.read()


setup(
  name = 'venra',
  packages = find_packages(exclude=[]),
  version = __version__,
  license='MIT',
  description = 'Venra provides a simple, high-level api for vespa.ai.',
  author = 'Cody Collier',
  author_email = 'cody@telnet.org',
  long_description=readme_contents,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/codycollier/venra',
  keywords = [
    'artificial intelligence',
    'information retrieval',
    'machine learning',
    'search',
  ],
  python_requires=">=3.8, <4",
  install_requires=[
    'packaging',
    'requests',
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)
