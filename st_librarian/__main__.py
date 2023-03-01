from pathlib import Path

import fire

from st_librarian import DocGenerator, Renamer, SQLTaskLib


def generate_docs(library=None):
    library_path = Path(library)
    library = SQLTaskLib(library_path)

    DocGenerator(library).generate(library_path / "templates.md")


def rename(old_name, new_name, library):
    library_path = Path(library).absolute()
    library = SQLTaskLib(library_path)
    Renamer(library).rename(old_name, new_name)


if __name__ == "__main__":
    fire.Fire({"generate_docs": generate_docs, "rename": rename})
