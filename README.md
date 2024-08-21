# AutoReadme

The README file is generated by AutoReadme.😊 This project serves as a starting point for generating project
documentation. Feel free to use and contribute.

本文档是由 AutoReadme 自动生成的。😊 本项目作为抛砖引玉，欢迎大家使用和贡献。

## Description

AutoReadme is a tool that automatically generates README files and dependencies, such as project structure and
requirements.txt, for a given project directory. It aims to simplify the documentation process by analyzing the project
and producing comprehensive documentation with minimal user intervention. If any information is missing, it will be
filled in with placeholders (`<>`).

AutoReadme 是一款基于 Python 的工具，旨在自动生成项目文档，包括 README 文件、requirements.txt和项目结构描述。 该工具利用语言模型 API
生成脚本和项目细节描述，一键生成，省心省力。任何未知信息将按照`<>`填充。

## Installation

To install and set up AutoReadme, follow these steps:

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Create a virtual environment and activate it:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Output

The expected output includes:

- A README.md file generated in the specified output directory.
- A PROJECT_STRUCTURE.md file detailing the project's structure.
- A requirements.txt file listing the project's dependencies.
- Script descriptions in JSON format.

## Usage

You can use AutoReadme by running the `auto_readme.py` script with the necessary command-line arguments. Below is an
example:

```sh
python auto_readme.py --project_name <Project_Name> --project_dir <Project_Directory> --project_description <Project_Description> --project_author <Author_Name>
```

Example usage in Python code:

```python
from auto_readme import AutoReadme

auto_readme = AutoReadme(
    project_name="MyProject",
    project_dir="./",
    project_description="This is my project.",
    project_author="Your Name"
)
auto_readme.generate_readme()
```

## Configuration

AutoReadme requires a configuration file `llm_config.json` located in the `config` directory. This file should contain
the necessary settings for the language model, including API keys and other parameters.

Example `llm_config.json`:

```json
{
  "OPENAI_CONFIG": {
    "OPENAI_KEYS_BASES": [
      {
        "OPENAI_KEY": "<your_openai_key>",
        "OPENAI_BASE": "<your_openai_base>"
      }
    ],
    "OPENAI_MAX_TOKENS": 1000,
    "OPENAI_TEMPERATURE": 0.7
  }
}
```

## Contributing

We welcome contributions to AutoReadme! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```sh
   git checkout -b feature/my-feature
   ```
3. Commit your changes:
   ```sh
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```sh
   git push origin feature/my-feature
   ```
5. Open a pull request with a detailed description of your changes.

Please adhere to the following coding standards:

- Write clear and concise commit messages.
- Follow PEP 8 guidelines for Python code.
- Ensure that your code passes all tests.

## License

This project is licensed under the MIT License.

## Contact Information

For support or inquiries, please contact Lintao at lint22@mails.tsinghua.edu.cn.