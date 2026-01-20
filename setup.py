"""
Hippo Memory Package Setup
해마 메모리 패키지 설치 파일
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hippo-memory",
    version="0.4.0-alpha",
    author="GNJz",
    author_email="",
    description="Hippocampus Memory Package - 완성된 해마 구조 독립 패키지",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qquartsco-svg/grid-engine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="hippocampus, memory, spatial memory, grid cells, place cells, ai, machine learning",
)

