import sys
from string import Template
from collections import defaultdict
from os import mkdir
from os.path import isdir

#TODO: Replace find and replace with format

color_list = ['red', 'green', 'blue', 'cyan', 'brown', 'orange', 'gray',  'teal', 
              'olive', 'magenta']

color_command = r'\usecolortheme[named={color}]{{structure}}'
list_delim = r'\item '

def expand_itemize(field):
    items = field.strip().split('#')
    if len(items) <= 1:
        return field.strip();

    return '\\begin{{itemize}}\n{}\\end{{itemize}}\n' \
            .format(list_delim + list_delim.join(items))

# TODO: Make it a class
def make_story(name_story, tasks, color, columns, template):
    name_folder = sys.argv[1]
    if not isdir(name_folder): 
        mkdir(name_folder)
    tex_out = open('{}/{}.tex'.format(name_folder, name_story), 'w');

    # Print header
    file_header = open('TaskHeader.tex', 'r')
    tex_out.writelines(file_header)
    # Choose color
    tex_out.write(color_command.format(color=color))

    # Begin document
    tex_out.write('\\begin{document}\n')

    # Render tasks
    for fields in tasks:
        if not len(fields) == len(columns):
            sys.stderr.write('Field number mismatch: ' + str(len(fields)) + '\n')
            sys.exit(1)

        fields = map(expand_itemize, fields)
        tex_out.write(template.safe_substitute(dict(zip(columns, fields))))

    # Close document
    tex_out.write('\\end{document}\n')
    tex_out.close()

# Read frame template
frame_template_file = open('./FrameTemplate.tex','r')
frame_template = Template(frame_template_file.read())

line = sys.stdin.readline()
columns = map(str.strip, line.split(','))

task_lines = sys.stdin.readlines()
grouped_lines = defaultdict(list)

for line in task_lines:
    line_split = line.split(',')
    grouped_lines[line_split[0]].append(line_split)

color = 0
for name_story in grouped_lines:
    make_story(name_story, 
            grouped_lines[name_story], 
            color_list[color], 
            columns, 
            frame_template)

    color = (color + 1) % len(color_list)
