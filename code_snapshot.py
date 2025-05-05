import os
import pathlib


def create_project_description(project_name, project_root):
    """Generates a detailed project description header."""
    return f""""
    This is a assignemnt project to merger pdfs files.
    The project uses django and bootstrap

===== INSTRUCTIONS FOR LLM =====
When analyzing this codebase:
1. Focus on the overall architecture and patterns
2. Identify potential improvements or bugs
3. Provide specific, actionable suggestions
4. Reference files by their relative paths when making comments

===== FILE LISTING BEGINS BELOW =====
Each file is delimited by markers showing its relative path.
Files are shown in alphabetical order within each directory.
"""


def create_codebase_snapshot(
    project_root,
    output_file,
    project_name,
    excluded_dirs=None,
    excluded_extensions=None,
):
    """
    Creates a consolidated file containing all code from a Django project with a descriptive header.
    """
    if excluded_dirs is None:
        excluded_dirs = [
            "__pycache__",
            "migrations",
            "venv",
            "env",
            ".git",
            "node_modules",
            "staticfiles",
            "media",
            ".idea",
            ".vscode",
            "dist",
            "build",
        ]

    if excluded_extensions is None:
        excluded_extensions = [
            ".pyc",
            ".sqlite3",
            ".db",
            ".jpg",
            ".png",
            ".gif",
            ".ico",
            ".env",
            ".zip",
            ".tar",
            ".gz",
        ]

    included_extensions = [
        ".py",
        ".html",
        ".js",
        ".css",
        ".txt",
        ".md",
        ".json",
        ".yml",
        ".yaml",
        ".sh",
    ]

    try:
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write(create_project_description(project_name, project_root))

            script_name = os.path.basename(__file__)

            for root, dirs, files in os.walk(project_root):
                dirs[:] = [d for d in dirs if d not in excluded_dirs]

                for file in sorted(files):
                    file_path = pathlib.Path(root) / file
                    rel_path = file_path.relative_to(project_root)

                    if (
                        file_path.name == os.path.basename(output_file)
                        or file_path.name == script_name
                    ):
                        continue

                    if file_path.name == os.path.basename(output_file):
                        continue

                    if file_path.suffix in excluded_extensions:
                        continue

                    if included_extensions and not file_path.suffix:
                        continue

                    if (
                        included_extensions
                        and file_path.suffix not in included_extensions
                    ):
                        continue

                    try:
                        with open(file_path, "r", encoding="utf-8") as infile:
                            content = infile.read()

                            outfile.write(f"\n\n===== BEGIN FILE: {rel_path} =====\n\n")
                            outfile.write(content)
                            outfile.write(f"\n\n===== END FILE: {rel_path} =====\n\n")

                    except UnicodeDecodeError:
                        print(f"Skipping binary file: {rel_path}")
                    except Exception as e:
                        print(f"Error reading {rel_path}: {str(e)}")

        print(f"Successfully created consolidated file at: {output_file}")

    except Exception as e:
        print(f"Error creating consolidated file: {str(e)}")


if __name__ == "__main__":
    DJANGO_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FILE = "snapshot.txt"
    PROJECT_NAME = "quickpoll"

    create_codebase_snapshot(DJANGO_PROJECT_ROOT, OUTPUT_FILE, PROJECT_NAME)
