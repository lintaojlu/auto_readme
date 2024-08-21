# Author: Lintao
import os


def generate_project_structure(dir_path, indent_level=0):
    markdown_lines = []
    for item in sorted(os.listdir(dir_path)):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            markdown_lines.append(f"{'  ' * indent_level}- **{item}/**")
            markdown_lines.extend(generate_project_structure(item_path, indent_level + 1))
        else:
            markdown_lines.append(f"{'  ' * indent_level}- {item}")
    return markdown_lines


def save_markdown_structure(dir_path, output_file="PROJECT_STRUCTURE.md"):
    project_structure = generate_project_structure(dir_path)
    with open(output_file, "w") as f:
        f.write("# Project Structure\n\n")
        f.write("\n".join(project_structure))
    print(f"Project structure has been saved to {output_file}")


# Example usage
if __name__ == "__main__":
    project_directory = "./"  # Replace with your project directory
    save_markdown_structure(project_directory)
