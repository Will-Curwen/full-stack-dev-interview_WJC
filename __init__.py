from IPython import get_ipython
from IPython.core.magic import register_line_magic
import re


@register_line_magic('answer')
def answer(inputs):
    '''
    This is a cell magic called answer that allows tutorial goers to import the correct answer from the key. 
    '''
    words = []
    for word in inputs.split(' '):
        if not word.startswith('#') and len(word) != 0:
            words.append(word)
        else:
            break

    flag = False
    if len(words) == 2:
        if words[1] == '-e':
            flag = True
        else:
            filepath = words[0]
            cell_number = int(words[1])

            with open(filepath, 'r') as file:
                lines = file.readlines()

            pattern = r'# %%\s+(.+)\s+(\d+)'
            start_line = None
            end_line = None

            for i, line in enumerate(lines):
                if re.match(pattern, line):
                    match = re.search(pattern, line)
                    if match and int(match.group(2)) == cell_number:
                        start_line = i + 1
                        break
            if start_line is not None:
                for i in range(start_line, len(lines)):
                    if re.match(pattern, lines[i]):
                        end_line = i
                        break
                else:
                    end_line = len(lines)

            if start_line is not None and end_line is not None:
                code_chunk = f"#| export\n# %answer {inputs}\n\n" + ''.join(lines[start_line:end_line])
                code_chunk = code_chunk.rstrip("\n")
                get_ipython().set_next_input(code_chunk, replace=True)
            else:
                raise Exception(f"Cell number {cell_number} not found in the Python file.")

    if len(words) == 1 or words[1] == '-e':
        filepath = words[0]
        with open(filepath, 'r') as file:
            lines = file.readlines()
        code_chunk = ''.join(lines[:])
        if flag:
            code_chunk = f"# %%export {filepath}\n\n" + code_chunk
        else: 
            code_chunk = f"# %answer {filepath}\n\n" + code_chunk
        get_ipython().set_next_input(code_chunk, replace=True)

    with open(filepath, 'r') as file:
        lines = file.readlines()
