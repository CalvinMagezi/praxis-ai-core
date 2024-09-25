from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="praxis-ai",
    version="0.0.1",
    author="Calvin Magezi",
    author_email="calvin@mts-africa.tech",
    description="An advanced, scalable AI assistant for task management and problem-solving",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/calvinmagezi/praxis-ai-core",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "anthropic",
        "rich",
        "tavily-python",
        "ollama",
        "groq",
        "openai",
        "fastapi",
        "ell-ai",
        "python-dotenv",
        "uvicorn",
        "pydantic",
        "requests",
        "beautifulsoup4",
        "pytest",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "praxis=praxis_ai.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)