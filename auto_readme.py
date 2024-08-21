# Author: Lintao
import argparse
import json
import logging
import os
from llm_api import get_model_answer

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class AutoReadme:
    def __init__(self, program_name, program_dir, author, model_name=None,
                 dependency_dir=None, readme_path=None, program_description=None, config_dir=None):
        self.program_name = program_name
        self.program_dir = program_dir
        self.program_description = program_description
        self.program_author = author
        if not model_name:
            model_name = "gpt-4o"
        self.out_put_dir = os.path.join(ROOT_DIR, 'output', program_name).__str__()
        os.makedirs(self.out_put_dir, exist_ok=True)

        if dependency_dir is None:
            dependency_dir = os.path.join(self.out_put_dir, "dependency")
            os.makedirs(dependency_dir, exist_ok=True)
        if readme_path is None:
            readme_path = os.path.join(self.out_put_dir, "README.md")
        if not config_dir:
            config_dir = os.path.join(ROOT_DIR, "config")
            os.makedirs(config_dir, exist_ok=True)
        self.config_dir = config_dir
        self.model = model_name
        self.dependency_dir = dependency_dir
        self.readme_path = readme_path
        logging.info(
            f"AutoReadme initialized for {program_name}, Program directory: {program_dir}, Author: {author}, Config directory: {config_dir}")
        logging.info(f'  Model: {model_name}')

    def generate_dependency(self):
        program_structure = self.generate_project_structure(self.program_dir)
        logging.info(f'Project structure: \n{program_structure}')
        scripts_description = self.generate_description_of_all_scripts()
        save_content_to_file("\n".join(program_structure), os.path.join(self.dependency_dir, "PROJECT_STRUCTURE.md"))
        save_content_to_file(json.dumps(scripts_description, indent=4),
                             os.path.join(self.dependency_dir, "SCRIPT_DESCRIPTION.json"))

    def find_all_scripts(self):
        logging.info(f"Finding all scripts in {self.program_dir}")
        scripts = []
        for root, dirs, files in os.walk(self.program_dir):
            for file in files:
                if file.endswith(".py") or file.endswith(".sh") or file.endswith(".bash"):
                    scripts.append(os.path.join(root, file))
        logging.info(f"Found {len(scripts)} scripts")
        logging.debug(f"Scripts: {scripts}")
        return scripts

    def generate_description_of_all_scripts(self):
        logging.info("Generating description of all scripts")
        scripts = self.find_all_scripts()
        script_description = {}
        for script in scripts:
            description = self.generate_file_description(script)
            script_description[script] = description
            logging.info(f"Description of {script}: {str(description)[:10]}...{str(description)[-10:]}")
        return script_description

    def generate_project_structure(self, dir_path, indent_level=0):
        markdown_lines = []
        for item in sorted(os.listdir(dir_path)):
            item_path = os.path.join(dir_path, item)
            if os.path.isdir(item_path):
                markdown_lines.append(f"{'  ' * indent_level}- **{item}/**")
                markdown_lines.extend(self.generate_project_structure(item_path, indent_level + 1))
            else:
                markdown_lines.append(f"{'  ' * indent_level}- {item}")
        return markdown_lines

    def generate_file_description(self, script_path):
        with open(script_path, "r") as f:
            script_content = f.read()
        sys_instruction = (
            'Please generate a summarized description that outlines the functionality of the following code/script,'
            ' including its input and output parameters, key algorithms or logic.'
            ' Ensure the description is clear and concise, suitable for technical documentation or code comments.'
        )
        prompt = [{"role": "system", "content": sys_instruction}, {"role": "user", "content": script_content}]
        logging.debug(f'prompt: {prompt}')
        answer = get_model_answer(model_name=self.model, inputs_list=prompt, config_dir=self.config_dir)
        logging.debug(f'***** description of {script_path} *****')
        logging.debug(f'{answer}')
        logging.debug(f'*****')
        return answer

    def get_dependency_content(self):
        logging.info("Reading dependency content")
        files = os.listdir(self.dependency_dir)
        if files == []:
            return {}
        dependency_content = {}
        for file in files:
            with open(os.path.join(self.dependency_dir, file), "r") as f:
                content = f.read()
            dependency_content[file.title()] = content
        logging.debug(dependency_content)
        return dependency_content

    def generate_readme(self):
        sys_instruction = (
            "Please generate a README file for this project that includes the following sections, and if specific details are unknown, set <> as placeholders: "
            "1. Project Title: The name of the project."
            "2. Description: A brief overview of the project's purpose, features, and key functionalities."
            "3. Installation: Step-by-step instructions on how to install and set up the project, including any dependencies."
            "4. Output: The expected output position and data formats of the output."
            "4. Usage: Examples of how to use the project, including any command-line instructions or code snippets."
            "5. Configuration: Information on any configuration files or environment variables required."
            "6. Contributing: Guidelines for contributing to the project, including any coding standards or pull request procedures."
            "7. License: The license under which the project is distributed."
            "8. Contact Information: How to reach the maintainers or developers for support or inquiries."
            "Ensure that the README is clear, well-organized, and helpful for both new users and contributors."
        )
        dependencies = self.get_dependency_content()
        if dependencies == {}:
            logging.error("No dependency files found. Please run 'generate_dependency' first.")
            return
        query = (
            'The information of this program is as follows:\n'
            f'program_name: {self.program_name}\n'
            f'program_author: {self.program_author}\n'
            f'program_short_description: {self.program_description}\n'
        )
        for title, content in dependencies.items():
            query += f"\n\n{title}:\n{content}"
        prompt = [{"role": "system", "content": sys_instruction}, {"role": "user", "content": query}]
        logging.debug(f'prompt: {prompt}')
        answer = get_model_answer(model_name=self.model, inputs_list=prompt, config_dir=self.config_dir)
        logging.debug(f'***** README *****')
        logging.debug(f'{answer}')
        logging.debug(f'*****')
        save_content_to_file(answer, self.readme_path)
        logging.info(f"README has been generated and saved to {self.readme_path}")


def save_content_to_file(content, file_path):
    with open(file_path, "w") as f:
        f.write(content)
        logging.info(f"Content has been saved to {file_path}")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Generate README and dependencies using AutoReadme.")

    # Required arguments with default values
    parser.add_argument('--program_name', type=str, help="Name of the program.")
    parser.add_argument('--program_dir', type=str, help="Directory of the program.")
    parser.add_argument('--author', type=str, help="Author of the program.")

    # Optional arguments with defaults set to None
    parser.add_argument('--model_name', type=str, default=None, help="Model name for AutoReadme.")
    parser.add_argument('--dependency_dir', type=str, default=None, help="Directory for dependencies.")
    parser.add_argument('--readme_path', type=str, default=None, help="Path to the README file.")
    parser.add_argument('--program_description', type=str, default=None, help="Description of the program.")
    parser.add_argument('--config_dir', type=str, default=None, help="Directory for configuration files.")

    # Parse the arguments
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Initialize AutoReadme with the provided arguments
    auto_readme = AutoReadme(
        program_name=args.program_name,
        program_dir=args.program_dir,
        author=args.author,
        model_name=args.model_name,
        dependency_dir=args.dependency_dir,
        readme_path=args.readme_path,
        program_description=args.program_description,
        config_dir=args.config_dir
    )

    # Generate dependency and README files
    auto_readme.generate_dependency()
    auto_readme.generate_readme()
