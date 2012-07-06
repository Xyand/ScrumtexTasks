import sys
from collections import defaultdict

#TODO: Replace find and replace wit format
template_slide = r'''
\begin{frame}[t]{$story}
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

color_list = ['red', 'green', 'blue', 'black', 
        'brown', 'orange', 'greenyellow', 
        'sepia', 'grey', 'magenta']

color_command = r'\usecolortheme[named={color}]{{structure}}'
list_delim = r'\item '

def expand_itemize(fields, index):
    text_var = fields[index].strip()
    items = text_var.split('#')
    if len(items) > 1:
        fields[index] = '\\begin{itemize}\n' + \
                      list_delim + list_delim.join(items) + \
                      '\\end{itemize}\n'

# TODO: Make it a class

def make_story(name_story, tasks, color, columns):

    # Print header
    file_header = open('TaskHeader.tex', 'r')
    for line in file_header:
        print line

    # Choose color
    print color_command.format(color=color)

    # Begin document
    print r'\begin{document}'

    # Render tasks
    for fields in tasks:
        if not len(fields) == len(columns):
            sys.stderr.write('Field number mismatch\n')
            sys.exit(1)

        slide = template_slide
        for i_field in xrange(len(fields)):
            expand_itemize(fields, i_field);
            slide = slide.replace('$' + columns[i_field], fields[i_field]);

    print slide

    # Close document
    print r'\end{document}'

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

