# Deep semantic parsing 

This repository includes the code and data related to the **"Deep semantic parsing with upper ontologies"** paper.

One-minute video to understand what it's all about (take a book text and generate a 3D scene ).

https://youtu.be/tl2sTSFBebU


## Motivation

Creating 3D scenes using only natural language can be a challenging task. Animat-ing 3D scenes using natural language adds an additional level of complexity to this task. 
And yet, over the past 50 years, starting with the pioneering work on the SHRDLU system there were many systems that have attempted to manipulate computer graphics objects using natural language. Many of these systems accept few sentences as input and try to identify physical objects that are relevant to the 3D scene. Systems such as SceneSeer leverage spatial knowledge priors to infer implicit constraints and resolve spatial relations.

In this project we take a rather different approach. We explicitly focus on fiction books as input to our system. There are two reasons why we make emphasis on fiction books. For once, there is a complex world and rich semantic information that can be understood only by analyzing the long distance relations between text phrases and logical inference about salient objects in the scene. The second reason for us to focus on fiction was the gamification of the annotation process. It is much more fun to interact with a program about the meaning of the text in your favorite book than annotating long boring documents drafted by some administra-tive office. 

## Dataset Description

The GAP dataset release comprises three .tsv files, each with eleven columns.

The files are:
 * **test** 4,000 pairs, to be used for official evaluation
 * **development** 4,000 pairs, may be used for model development
 * **validation** 908 pairs, may be used for parameter tuning

The columns contain:

Column | Header         | Description
:-----:|----------------|--------------------------------------------
1      | ID             | Unique identifer for an example (two pairs)
2      | Text           | Text containing the ambiguous pronoun and two candidate names. About a paragraph in length
3      | Pronoun        | The pronoun, text
4      | Pronoun-offset | Character offset of Pronoun in Column 2 (Text)
5      | A ^            | The first name, text
6      | A-offset       | Character offset of A in Column 2 (Text)
7      | A-coref        | Whether A corefers with the pronoun, TRUE or FALSE
8      | B ^            | The second name, text
9      | B-offset       | Character offset of B in Column 2 (Text)
10     | B-coref        | Whether B corefers with the pronoun, TRUE or FALSE
11     | URL ^^         | The URL of the source Wikipedia page

^ Please note that systems should detect mentions for inference automatically, and access labeled spans only to output predictions.

^^ Please also note that there are two task settings, *snippet-context* in which the URL column may **not** be used, and *page-context* where the URL, and the denoted Wikipedia page, may be used.

## Benchmarks

Performance on GAP may be benchmarked against the syntactic parallelism baseline from our above paper on the test set:

Task Setting      | M    | F    |  B     | O
:----------------:|------|------|--------|------
*snippet-context* | 69.4 | 64.4 | *0.93* | 66.9
*page-context*    | 72.3 | 68.8 | *0.95* | 70.6

where the metrics are F1 score on **M**asculine and **F**eminine examples, **O**verall, and a **B**ias factor calculated as **F** / **M**.

## Contact
To contact us, please use gap-coreference@google.com
