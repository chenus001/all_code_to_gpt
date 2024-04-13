Introduction

In modern software development, efficiently communicating the entirety of a project's structure to AI models like ChatGPT is crucial for leveraging their capabilities in code generation and problem-solving. I encountered a significant challenge: how to provide a complete, organized snapshot of the codebase to the AI without manual intervention. This tool directly addresses that need by automating the preparation of your codebase in a format that AI models can readily understand.
Purpose

The Directory Structure and Code Exporter serves as a bridge between complex codebases and AI understanding, formatting the entire project's code in a structured manner that can be easily ingested by ChatGPT. This enables the AI to assist in project development more effectively by having a full grasp of the code’s layout and logic.
Features

Automatically generates a detailed directory tree and code content.
Exports clean code files without comments to streamline AI analysis.
Ignores non-code files to focus on critical information.
Provides a simple GUI for easy interaction and process management.

Requirements

Python 3.x
Tkinter (included with Python in most distributions)
Webbrowser (part of Python's standard library)

Installation

No additional installation is required if Python is already set up on your machine. Just ensure all script files are located in the same directory.
Usage

Launch the script using Python.
Through the GUI:
Select the source directory where your code is stored.
Choose the destination for the output file that will store the directory tree and code.
Use the "Open Output Directory" button to immediately view the results after processing.
The tool generates a .txt file with the organized directory structure and code, facilitating effective communication with AI models.

Contribution

Your contributions are welcome! Fork this repository, propose changes through pull requests, or report issues and suggestions on GitHub.

引言

在现代软件开发中，有效地向诸如ChatGPT之类的AI模型传达项目的全部结构至关重要，这有助于利用它们在代码生成和问题解决方面的能力。我面临一个重大挑战：如何在无需手动干预的情况下，向AI提供一个组织有序的代码库快照。此工具直接满足了这一需求，通过自动化方式准备您的代码库，使其格式符合AI模型的易理解性。
目的

目录结构和代码导出工具充当复杂代码库与AI理解之间的桥梁，以结构化方式格式化整个项目的代码，便于ChatGPT等AI模型轻松吸收。这使得AI能够通过完全掌握代码的布局和逻辑，更有效地协助项目开发。
功能

自动生成详细的目录树和代码内容。
导出无注释的清洁代码文件，以简化AI分析。
忽略非代码文件，专注于关键信息。
提供简单的图形用户界面，易于交互和过程管理。

系统要求

Python 3.x
Tkinter（大多数Python发行版已包含）
Webbrowser（Python标准库的一部分）

