import os
from setuptools import setup, find_packages


dependency_path = os.getcwd() + "\\requirements.txt"
print(dependency_path)

dependencies = []
with open(dependency_path, encoding="utf-8") as f:
    dependencies = f.readlines()

setup(
    name="crawl_for_fine_proverbs",
    version="1.0.0",
    packages=find_packages(),  # 패키지 폴더 안에서 자동으로 패키지 찾기
    install_requires=dependencies,
    author="Nenda",
    author_email="jooeon1104@gmail.com",
    description="Description of your package",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
