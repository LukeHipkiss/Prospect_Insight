from setuptools import find_packages, setup


setup(
    name="lighthouse",
    version="0.1.0",
    author="Lucas",
    packages=find_packages(),
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
    install_requires=open("requirements.txt").readlines(),
    entry_points={"console_scripts": ["runner=lighthouse.runner:main"]},
    setup_requires=[],
    tests_require=[],
)
