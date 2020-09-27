from setuptools import find_packages, setup


setup(
    name="prospects_insight",
    version="0.1.0",
    author="Luke",
    packages=find_packages(),
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
    install_requires=open("requirements.txt").readlines(),
    setup_requires=[],
    tests_require=[],
)
