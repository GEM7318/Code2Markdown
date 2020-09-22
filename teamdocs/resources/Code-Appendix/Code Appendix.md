# Code Reference
- [Python](#python)
  - [`/Code2Markdown/Usage.py` ](#code2markdownusagepy-)
  - [Code2Markdown/code2markdown/Code \[\](#)(name=Code)](#code2markdowncode2markdowncode-namecode)
- [Toml](#toml)
  - [`Code2Markdown/pyproject.toml`](#code2markdownpyprojecttoml)
  - [`Code2Markdown/code2markdown/file-types.toml`](#code2markdowncode2markdownfile-typestoml)


##  Python
<br></br>
### `/Code2Markdown/Usage.py` 
```python


from code2markdown import Code
from pathlib import Path

# TODO: Next need to combine Code() and Index() and DirTree() and Index()
#   to create DirTree and Code Reference

# TODO:
#   - Export each code file as its own .md file into a 'Code Reference' folder
#   - Export an 'Index.md' file into it containing a default
#       hierarchy/order with placeholders for the script-markdown themselves
#   - This can then have the script markdown parsed into it and saved
#   separately once the user defines where their order (will have to
#   manually add additional scripts to it in the future)


# TODO: Don't forget that the DirIndex is supposed to determine what gets
#  synced back to teamdocs


code = Code.Code()
code.read_dir(Path.cwd())

exclude_dirs = [".eggs", "env", "project_env", "__pycache__", "_archive", "archive"]

len(code.markdown)
len(code.trash)

code.gather_exclusions(file_patterns=['__.*__.py'], dir_patterns=exclude_dirs)

len(code.trash)
code.remove_exclusions()
len(code.trash)
len(code.markdown)

output_base = Path.cwd().parent / 'Scratches' / 'Output'

all_markdowns = []
for path, md_str in code.markdown.items():
    to_write = f"### {path.name}\n{md_str}"
    all_markdowns.append(to_write)
    print(f"{path}:\n\t{md_str}")
    break

with open(output_base / 'Master.md', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(all_markdowns))

for k, v in file_ext_to_md_tag.items():
	print(f"{k} = '{v}'")

```
<br></br>
### Code2Markdown/code2markdown/Code [](#)(name=Code)

```python
from pathlib import Path
from typing import Generator
import re
import toml


class Code:
    """A simple class for collecting code files into a markdown collection."""

    file_ext_to_md_tag: dict = {
        "bashrc": "bash",
        "bat": "shell",
        "html": "html",
        "ini": "ini",
        "json": "json",
        "py": "python",
        "rst": "rst",
        "sh": "sh",
        "sql": "sql",
        "toml": "toml",
        "R": "R",
        "xml": "xml",
        "yml": "yaml"
    }

    def __init__(self):

        # with open(Path.cwd() / "file-types.toml", "r") as r:
        #     self.file_ext_to_md_tag = toml.load(r)
        """dict: Lookup of file extensions to backtick tag within .md file."""

        self.patterns = [f"**/*.{typ}" for typ in self.file_ext_to_md_tag.keys()]
        """list: Regex patterns for file types included in file-types.toml."""

        self.markdown: dict = {}
        """dict: Dictionary of {pathlib.Path(): markdown_str}, populated by
            .read() and .read_dir() methods."""

        self.trash: set = set()
        """set: Set of files to exclude based on file or directory patterns,
            populated by .gather_trash() method."""

    @staticmethod
    def _get_files(dir_path: Path, file_patterns: list) -> Generator:
        """Finds all code files in a directory provided a list of file patterns.

        Args:
            dir_path: Directory to traverse in search of code files.
            file_patterns: List of file (extension) patterns to search for.
        """
        for typ in file_patterns:
            yield from dir_path.glob(pattern=typ)

    @staticmethod
    def _as_md(code: str, md_tag: str):
        """Parses into markdown given a string of code & a markdown decorator for a given code type."""
        return f"""
​```{md_tag}
{code}
"""

    def read(self, path_to_code_file: Path) -> str:
        """Read in a file and returns the markdown if it's renderable.

        Args:
            path_to_code_file: Full pathlib.Path() to a code file.

        Returns:
            Markdown-renderable string of contents within code file.
        """
        _, ext = path_to_code_file.suffix.split(".")
        md_tag = self.file_ext_to_md_tag.get(ext)
        if md_tag:
            with open(path_to_code_file, "r", encoding="utf-8") as r:
                self.markdown[path_to_code_file] = self._as_md(r.read(), md_tag)
        else:
            return ""

    def read_dir(self, dir_path: Path, types: list = None) -> None:
        """Reads in all code files renderable in markdown.

        Args:
            dir_path: Directory to traverse for code files.
            types: Types to search for - defaults to all file types stored
                in file-types.toml.
        """
        types = self.patterns if not types else [f"**/*.{typ}" for typ in types]
        for p in self._get_files(dir_path, types):
            md = self.read(p)
            if md:
                self.markdown[p] = md

    def gather_trash(self, file_patterns: list = None, dirs: list = None) -> None:
        """Populates 'trash' attribute with a list of Path objects to
            exclude based on a list of file patterns or directories to exclude.

        Args:
            file_patterns: List of regex file patterns to exclude.
            dirs: List of plain text directory names to exclude.
        """
        assert self.markdown, "gather_trash() called prior to reading in files"
        assert (
            file_patterns or dirs
        ), "Please provide a list of file patterns or directory names to exclude"

        for k in self.markdown.keys():
            check_file = (
                False
                if not file_patterns
                else any(re.findall(p, k.name) for p in file_patterns)
            )
            check_dir = (
                False
                if not dirs
                else any(
                    re.findall(p, directory) for directory in k.parts for p in dirs
                )
            )
            if check_file or check_dir:
                self.trash.add(k)

    def empty_trash(self) -> None:
        """Removes all files collected by trash gathering from markdowns."""
        for path in self.trash:
            _ = self.markdown.pop(path)
        print(f"<removed {len(self.trash)} files from markdown collection>")
        self.trash.clear()
        
    def dump(self, output_dir: Path):
        self.read_dir(dir_path=output_dir)
        for path, md_str in self.markdown.items():
            file_stem, _ = path.name.split('.')
            with open(output_dir / f"{file_stem}.md", 'w') as f:
                f.write(md_str)
```

<br></br>
## Toml
<br></br>

### `Code2Markdown/pyproject.toml`

```toml
[build-system]
requires = ["flit_core >=2,<4"]
build-backend = "flit_core.buildapi"

[tool.flit.metadata]
module = "code2markdown"
author = "Grant Murray"
author-email = "gmurray203@gmail.com"
home-page = "https://github.com/GEM7318/Code2Markdown"
classifiers = ["License :: OSI Approved :: MIT License"]
description-file = "README.md"

[tool.flit.sdist]
include = ["code2markdown/.*"]

[tool.flit.scripts]
run = "code2markdown:main"

```

<br></br>

### `Code2Markdown/code2markdown/file-types.toml`

```toml

bashrc = 'bash'
bat = 'shell'
html = 'html'
ini = 'ini'
json = 'json'
py = 'python'
rst = 'rst'
sh = 'sh'
sql = 'sql'
toml = 'toml'
R = 'R'
xml = 'xml'
yml = 'yaml'

```
