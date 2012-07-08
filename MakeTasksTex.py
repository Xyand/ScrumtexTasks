import sys
from string import Template
from collections import defaultdict
from os import mkdir
from os.path import isdir

color_list = ['red', 'green', 'blue', 'cyan', 'brown', 'orange', 'gray',  'teal', 
              'olive', 'magenta']

color_command = r'\usecolortheme[named={color}]{{structure}}'
list_delim = r'\item '

def expand_itemize(field):
    ''' Expand field text to a latex \\itemize clause. Items are to be delimited with #'''

    items = field.strip().split('#')
    if len(items) <= 1:
        return field.strip();

    return '\\begin{{itemize}}\n{}\\end{{itemize}}\n' \
            .format(list_delim + list_delim.join(items))

# TODO: Make it a class
def make_story(name_story, tasks, color, columns, template):
    ''' Create a tex file for a specific user story given its name tasks and color '''

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
        assert len(fields) == len(columns), 'Field number mismatch: ' + str(len(fields))
        fields = map(expand_itemize, fields)
        tex_out.write(template.safe_substitute(dict(zip(columns, fields))))

    # Close document
    tex_out.write('\\end{document}\n')
    tex_out.close()

def main():
    ''' Create all user story tex files '''

    # Read frame template
    frame_template_file = open('./FrameTemplate.tex','r')
    frame_template = Template(frame_template_file.read())

    # Read column names
    line = sys.stdin.readline()
    columns = map(str.strip, line.split(','))

    # Split tasks to user stories
    grouped_lines = defaultdict(list)
    for line in sys.stdin:
        line_split = line.split(',')
        grouped_lines[line_split[0]].append(line_split)

    # Crate tex file for every user story
    color = 0
    for name_story in grouped_lines:
        make_story(name_story, 
                grouped_lines[name_story], 
                color_list[color], 
                columns, 
                frame_template)

        color = (color + 1) % len(color_list)


if __name__ == '__main__':
    main()
