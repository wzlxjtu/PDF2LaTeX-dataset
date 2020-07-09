This software is modified from KaTeX and https://github.com/harvardnlp/im2markup

This is a node.js based software to tokenize latex source code. This also serve the purpose to normalize LaTeX.

An example command line:
node tokenize_latex.js normalize data/source.txt > data/target.txt

To debug node, run in Visual Studio Code:
inspect tokenize_latex.js normalize data/source.txt