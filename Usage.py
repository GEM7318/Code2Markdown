

from src.code2markdown import Code
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
