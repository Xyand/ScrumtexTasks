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


class ScrumtexBuilder:

    def __init__(self, columns, folder_out, file_header, file_template):
        self.folder_out = folder_out
        if not isdir(folder_out): 
            mkdir(folder_out)

        # Set header
        file_header = open(file_header, 'r');
        self.header = file_header.read();

        self.columns = columns
        self.color = 0

        # Read frame template
        file_template_frame = open(file_template,'r')
        self.template_frame = Template(file_template_frame.read())
 
    def set_color(self):
        self.tex_out.write(color_command.format(color=color_list[self.color]))
        self.color = (self.color + 1) % len(color_list)

    def set_header(self):
        self.tex_out.write(self.header)

    def begin_document(self):
        self.tex_out.write('\\begin{document}\n')

    def end_document(self):
        self.tex_out.write('\\end{document}\n')
        self.tex_out.close()

    def make_story(self, name_story, tasks):
        ''' Create a tex file for a specific user story given its name tasks and color '''

        self.tex_out = open('{}/{}.tex'.format(self.folder_out, name_story), 'w');

        self.set_header()
        self.set_color()
        self.begin_document()

        # Render tasks
        for fields in tasks:
            assert len(fields) == len(self.columns), \
                'Field number mismatch: ' + str(len(fields))
            fields = map(expand_itemize, fields)
            fields_cols = dict(zip(self.columns, fields))
            self.tex_out.write(self.template_frame.safe_substitute(fields_cols))

        # Close document
        self.end_document()

def main():
    ''' Create all user story tex files '''

    # Read column names
    line = sys.stdin.readline()
    columns = map(str.strip, line.split(','))

    # Initialize tex builder
    tex_builder = ScrumtexBuilder(columns, \
            sys.argv[1], \
            './TaskHeader.tex', \
            './FrameTemplate.tex')

    # Split tasks to user stories
    grouped_lines = defaultdict(list)
    for line in sys.stdin:
        line_split = line.split(',')
        grouped_lines[line_split[0]].append(line_split)

    # Crate tex file for every user story
    color = 0
    for name_story in grouped_lines:
        tex_builder.make_story(name_story, grouped_lines[name_story])

if __name__ == '__main__':
    main()
