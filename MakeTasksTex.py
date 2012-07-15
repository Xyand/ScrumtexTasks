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
    """ Transforms parsed CSV task files into latex presentation files. The format of the
    input files is of the form:
    
    key_name1, key_name2, key_name3, ....
    val1, val2, val3, ...
    .
    .
    .

    The key names should match the template arguments of the form "$name" in the template file
    """

    def __init__(self, folder_out, file_header, file_template):
        """ Reads template files """

        self.folder_out = folder_out

        # Set header
        file_header = open(file_header, 'r');
        self.header = file_header.read();

        self.color = 0

        # Read frame template
        file_template_frame = open(file_template,'r')
        self.template_frame = Template(file_template_frame.read())
 
    def __set_color(self):
        """ Print the current color setting command and advance to the next color in a
        circular manner """

        self.tex_out.write(color_command.format(color=color_list[self.color]))
        self.color = (self.color + 1) % len(color_list)

    def __set_header(self):
        """ Print presentation header section """
        self.tex_out.write(self.header)
        self.__set_color()
        self.tex_out.write('\\begin{document}\n')

    def __end_document(self):
        """ Write the final close of the presentation tex file and close the file """
        self.tex_out.write('\\end{document}\n')
        self.tex_out.close()

    def __make_story(self, name_story, tasks):
        ''' Create a tex file for a specific user story given its name tasks and color '''

        self.tex_out = open('{}/{}.tex'.format(self.folder_out, name_story), 'w');
        self.__set_header()

        # Render tasks
        for fields in tasks:
            assert len(fields) == len(self.columns), \
                'Field number mismatch: ' + str(len(fields))
            fields = map(expand_itemize, fields)
            fields_cols = dict(zip(self.columns, fields))
            self.tex_out.write(self.template_frame.safe_substitute(fields_cols))

        # Close document
        self.__end_document()

    def process_csv(self, file_in):
        ''' Create all user story tex files by parsing CSV'''

        # Read column names
        line = file_in.readline()
        self.columns = map(str.strip, line.split(','))

        # Split tasks to user stories
        grouped_lines = defaultdict(list)
        for line in file_in:
            line_split = line.split(',')
            grouped_lines[line_split[0]].append(line_split)

        # Crate tex file for every user story
        for name_story in grouped_lines:
            self.__make_story(name_story, grouped_lines[name_story])

if __name__ == '__main__':
    tex_builder = ScrumtexBuilder(sys.argv[1], './TaskHeader.tex', './FrameTemplate.tex')
    tex_builder.process_csv(sys.stdin)
