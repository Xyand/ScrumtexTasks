rm -r $2
cat $1 | python ./MakeTasksTex.py
cd $2
find . -name "*.tex" -exec pdflatex {} \;
pdftk *.pdf cat output final.pdf
