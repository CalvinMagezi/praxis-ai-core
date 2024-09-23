from setuptools import setup

setup(
    name="praxis-ai",
    version="0.0.1",
    packages=["praxis_ai"],
    entry_points={
        "console_scripts": [
            "praxis-ai=main:main",
        ],
    },
)