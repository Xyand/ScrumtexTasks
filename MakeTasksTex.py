import sys
from collections import defaultdict
from os import mkdir
from os.path import isdir

#TODO: Replace find and replace wit format
template_slide = r'''
\begin{frame}[t]{\LARGE \textbf{$story}}
\begin{block}{$task}
$details
\end{block}
\begin{block}{Done}
$done
\end{block}
\begin{tabular*}{0.9\textwidth}{@{\extracolsep{\fill}}  l  l  l  }
Assigned to: & Estimate: $estimate & Reviewer:
    \end{tabular*}
    \end{frame}
'''

color_list = ['red', 'green', 'blue', 'cyan', 
        'brown', 'orange', 'gray', 
        'teal', 'olive', 'magenta']

color_command = r'\usecolortheme[named={color}]{{structure}}'
list_delim = r'\item '

def expand_itemize(fields, index):
    text_var = fields[index].strip()
    items = text_var.split('#')
    if len(items) > 1:
        fields[index] = '\\begin{{itemize}}\n{}\\end{{itemize}}\n' \
            .format(list_delim + list_delim.join(items))

# TODO: Make it a class
def make_story(name_story, tasks, color, columns):
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

        slide = template_slide
        for i_field in xrange(len(fields)):
            expand_itemize(fields, i_field);
            slide = slide.replace('$' + columns[i_field], fields[i_field]);

        tex_out.write(slide)

    # Close document
    tex_out.write('\\end{document}\n')
    tex_out.close()

line = sys.stdin.readline()
columns = map(str.strip, line.split(','))

task_lines = sys.stdin.readlines()
grouped_lines = defaultdict(list)

for line in task_lines:
    line_split = line.split(',')
    grouped_lines[line_split[0]].append(line_split)


color = 0
for name_story in grouped_lines:
    make_story(name_story, grouped_lines[name_story], color_list[color], columns)
    color = (color + 1) % len(color_list)

