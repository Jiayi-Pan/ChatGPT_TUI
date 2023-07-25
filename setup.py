from setuptools import setup, find_packages

setup(
    name="chatgpt_tui",
    version="0.7.0",
    author="Jiayi Pan",
    author_email="i@jiayipan.me",
    description="A simple TUI interface for ChatGPT.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jiayi-Pan/ChatGPT_TUI",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["chatbot", "tui", "chatgpt", "chatgpt_tui"],
    packages=find_packages(),
    install_requires=["textual==0.13", "httpx", "pyperclip"],
    entry_points={
        "console_scripts": [
            "catui = chatgpt_tui.app:run"
        ]
    },
    package_data={'': ['*.css']}
)
