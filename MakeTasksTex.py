import sys

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

color_command = r'\usecolortheme[named={color}]{{structure}}'
list_delim = r'\item '

def expand_itemize(fields, index):
    text_var = fields[index].strip()
    items = text_var.split('#')
    if len(items) > 1:
        fields[index] = '\\begin{itemize}\n' + \
                      list_delim + list_delim.join(items) + \
                      '\\end{itemize}\n'

# Print header
file_header = open('TaskHeader.tex', 'r')
for line in file_header:
    print line

print color_command.format(color='green')
print r'\begin{document}'

line = sys.stdin.readline()
columns = map(str.strip, line.split(','))

for line in sys.stdin:
    fields = map(str.strip, line.split(','))

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
