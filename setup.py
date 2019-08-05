from setuptools import setup

setup(
    name="monstercat-cli",
    version="0.0.0",
    description="",
    author="Devin Packer",
    license="MIT",
    packages=["monstercat"],
    zip_safe=False,
    install_requires=[
        "click",
    ],
    entry_points="""
        [console_scripts]
        monstercat=monstercat.__main__:main
    """
)
