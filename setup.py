from setuptools import setup, find_packages

setup(
    name="task-cli",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click",
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "task-cli=task_cli.cli:cli",
        ]
    }
)