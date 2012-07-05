import sys

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


list_delim = r'\item '

# TODO: Extract automatically from header
var_map = { '$story' : 0,
        '$task' : 1,
        '$details' : 2,
        '$done' : 3,
        '$estimate' : 4}

def expand_itemize(fields, key):
    text_var = fields[key].strip()
    items = text_var.split('#')
    if len(items) > 1:
        fields[key] = '\\begin{itemize}\n' + \
                      list_delim + list_delim.join(items) + \
                      '\\end{itemize}\n'

# Print header
file_header = open('TaskHeader.tex', 'r')
line = file_header.readline();
while line:
    print line
    line = file_header.readline()

line = sys.stdin.readline()
line = sys.stdin.readline()
while line:
    fields = line.split(',')
    slide = template_slide
    for key in var_map:
        expand_itemize(fields, var_map[key]);
        slide = slide.replace(key, fields[var_map[key]]);

    print slide
    line = sys.stdin.readline()

# Close document
print r'\end{document}'
