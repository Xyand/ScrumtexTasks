# TODO: Consider rewriting in python for windows sake

# Make sure output folder exists
mkdir -p $2

# Clear output folder contents
rm $2/*.*

# Generate tex fiels
cat $1 | python ./MakeTasksTex.py $2

# Generate PDF file
cd $2
find . -name "*.tex" -exec pdflatex {} \;

# Combine pdf files
pdftk *.pdf cat output final.pdf
