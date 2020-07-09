# evaluation script for the dataset
# report results as Levenshtein Edit Distance

import re
import os
import editdistance

# whether to use katex to normalize math latex
# this requires nodejs
katex_normalization = True

filenames = [str(i) for i in range(1, 103)]

def normalize(content, infty_mode=False):
    # only keep the main body tex
    if '\\begin{document}' in content:
        s, e = content.find('\\begin{document}'), content.find('\\end{document}')
        content = content[s + 16:e]
    content = content.lower()
    # replace all math declaration with $..$
    content = re.sub(r'\\begin{equation\*?}', '$', content)
    content = re.sub(r'\\end{equation\*?}', '$', content)
    content = re.sub(r'\\begin{align\*?}', '$', content)
    content = re.sub(r'\\end{align\*?}', '$', content)
    content = re.sub(r'\\begin{eqnarray\*?}', '$', content)
    content = re.sub(r'\\end{eqnarray\*?}', '$', content)
    content = re.sub(r'\\begin{gather\*?}', '$', content)
    content = re.sub(r'\\end{gather\*?}', '$', content)
    content = re.sub(r'\\begin{alignat\*?}', '$', content)
    content = re.sub(r'\\end{alignat\*?}', '$', content)
    content = re.sub(r'\\begin{multline}', '$', content)
    content = re.sub(r'\\end{multline}', '$', content)
    # for infty reader
    if infty_mode:
        content = re.sub(r'\$\$', '$', content)
        content = re.sub(r'\\begin{center}', '', content)
        content = re.sub(r'\\end{center}', '', content)
    # for non-infty
    else:
        content = re.sub(r'\\begin{center}', '$', content)
        content = re.sub(r'\\end{center}', '$', content)


    # content = re.sub(r'\\begin{array}', '$', content)
    # content = re.sub(r'\\end{array}', '$', content)

    content = removeTitle(content, '\\paragraph')
    content = removeTitle(content, '\\section')
    content = removeTitle(content, '\\subsection')
    content = removeTitle(content, '\\subsubsection')

    content = re.sub(r' ', '', content)
    content = re.sub(r'\\\\', '', content)
    content = re.sub(r'\t', '', content)
    content = re.sub(r'\n', '', content)
    content = re.sub(r'\\small', '', content)
    content = re.sub(r'\\normalsize', '', content)
    content = re.sub(r'\\nonumber', '', content)
    content = re.sub(r'\\allowdisplaybreaks', '', content)
    content = re.sub(r'\\setcounter{.*?}{\d+}', '', content)
    content = re.sub(r'\\iffalse', '', content)
    content = re.sub(r'\\item', '', content)
    content = re.sub(r'\\begin{enumerate}', '', content)
    content = re.sub(r'\\end{enumerate}', '', content)
    content = re.sub(r'\\begin{itemize}', '', content)
    content = re.sub(r'\\end{itemize}', '', content)
    content = re.sub(r'\\doublespacing', '', content)
    content = re.sub(r'\\pagestyle{plain}', '', content)
    return content

def removeTitle(content, title):
    # remove the title claimer, for example:
    # \section{something} -> something
    idx = content.find(title)
    if idx == -1:
        return content
    close = idx + len(title) + 1
    while content[close] != '}':
        close += 1
        if close == len(content):
            return content
    return content[:idx] + content[idx + len(title) + 1: close] +\
            removeTitle(content[close+1:], title)

def katex_normalize(sentences):
    # use katex to normalize latex
    # input are sentences separated by splitMathFromText
    tmp_math = ''
    tmp_idx = []
    for i, s in enumerate(sentences):
        if not s: continue
        if s[0] == '$':
            tmp_math += s + '\n'
            tmp_idx.append(i)
    f = open("tmp_before.txt", "w", encoding="utf-8")
    f.write(tmp_math)
    f.close()
    os.system(
        '"C:\Program Files/nodejs/node" latex_normalizer/tokenize_latex.js normalize tmp_before.txt > tmp_after.txt')
    with open('tmp_after.txt', encoding="utf-8") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip().replace(" ", "") for x in content]

    os.remove("tmp_before.txt")
    os.remove("tmp_after.txt")
    for i, s in enumerate(content):
        # skip the failure conversions
        if not content[i]: continue
        sentences[tmp_idx[i]] = content[i]
    sentence = ''.join(sentences)
    return sentence, sentences

def splitMathFromText(text):
    # given a string of text, separate the math from text
    # return a list of sentences
    separator = []
    sentences = []
    for i in range(len(text)):
        if text[i] == '$':
            separator.append(i)
    assert(len(separator) % 2 == 0)
    idx = 0
    for i in range(int(len(separator)/2)):
        sentences.append(text[idx:separator[i*2]])
        sentences.append(text[separator[i*2]:separator[i*2+1]+1])
        idx = separator[i*2+1]+1
    sentences.append(text[idx:-1])

    return sentences

dist = dist_text = dist_math = 0
edit_rates, edit_rates_text, edit_rates_math = [], [], []
total_words = total_words_math = total_words_text = 0
gt_math_char = gt_text_char = gt_math_count = 0

for filename in filenames:
    print(filename)
    gt_file = 'evaluation/' + filename + '_gt.tex'
    # pred_file = 'evaluation/' + filename + '_infty.tex'
    # infty_mode = True
    pred_file = 'E:\zelun\output_bleu_model_spellchecker/' + filename + '.txt'
    infty_mode = False

    with open(gt_file, 'r', encoding="utf8") as file:
        gt = file.read().replace('\n', ' ')
    with open(pred_file, 'r', encoding="utf8") as file:
        pred = file.read().replace('\n', ' ')

    gt_normalized = normalize(gt)
    pred_normalized = normalize(pred, infty_mode)

    # split the evaluation into text part and math part
    gt_sentences = splitMathFromText(gt_normalized)
    pred_sentences = splitMathFromText(pred_normalized)

    # normalize latex with katex
    if katex_normalization:
        gt_normalized, gt_sentences = katex_normalize(gt_sentences)
        pred_normalized, pred_sentences = katex_normalize(pred_sentences)

    gt_text, gt_math = '', ''
    pred_text, pred_math = '', ''

    for s in gt_sentences:
        if not s: continue
        if s[0] == '$':
            gt_math += s
            gt_math_char += len(s)-2
            gt_math_count += 1
        else:
            gt_text += s
            gt_text_char += len(s)
    for s in pred_sentences:
        if not s: continue
        if s[0] == '$':
            pred_math += s
        else:
            pred_text += s

    dist += editdistance.eval(gt_normalized, pred_normalized)
    dist_math += editdistance.eval(gt_math, pred_math)
    dist_text += editdistance.eval(gt_text, pred_text)

    total_words += len(gt_normalized)
    total_words_math += len(gt_math)
    total_words_text += len(gt_text)

print('raw edit dist: ' + str(dist))
print('total number of characters: ' + str(total_words))
print('edit dist rate: ' + str(1-dist/total_words))
print('edit dist rate (math): ' + str(1-dist_math/total_words_math))
print('edit dist rate (text): ' + str(1-dist_text/total_words_text))


