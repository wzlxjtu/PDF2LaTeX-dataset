# PDF2LaTeX-102 Dataset

PDF2LaTeX-102 is a dataset with 102 single-page PDF documents and their LaTeX ground truth markups. This dataset can be used to evaluate the performance of the PDF2LaTeX task, i.e., reverting PDF documents to their LaTeX sources.

Each PDF page in this dataset is either single column or double column, containing a mixture of text and math expressions. These pages are generated using the real-world publications on arXiv, mostly in STEM fields. Figures, tables, references, and footnotes are removed from the original documents. The evaluation is based on the Levenshtein Edit Distance between the ground truth LaTeX and the predicted LaTex.

This dataset also contains baselines generated from the InftyReader software. The baselines are files ending with "_infty.tex". The ground truth files are those ending with "_gt.tex". The evaluation software is written in Python, and can be exectued by "python evaluate.py".

For more details about this dataset, please refer to our paper:
 - Z Wang and J Liu, "PDF2LaTeX: A Deep Learning System to Convert Mathematical Documents from PDF to LaTeX", Proceedings of the ACM Symposium on Document Engineering 2020.

License
----
/* Copyright (c) 2017-2019, Texas Engineering Experiment Station (TEES), a component of the Texas A&M University System.
    All rights reserved.
    The information and source code contained herein is the exclusive property of TEES and may not be disclosed, examined or reproduced in whole or in part without explicit written authorization from TEES.
 */