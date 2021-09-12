# Deep semantic parsing 

This repository includes the code and data related to the **"Deep semantic parsing with upper ontologies"** paper.


## Example: 10 minute video.

https://www.youtube.com/50ee1281-65c9-49bd-b9e2-fa449f00ce59


## Old one-minute video to understand what it's all about (take a book text and generate a 3D scene ).

https://youtu.be/tl2sTSFBebU


## Motivation

Creating 3D scenes using only natural language can be a challenging task. Animating 3D scenes using natural language adds an additional level of complexity to this task. 
And yet, over the past 50 years, starting with the pioneering work on the SHRDLU system there were many systems that have attempted to manipulate computer graphics objects using natural language. Many of these systems accept few sentences as input and try to identify physical objects that are relevant to the 3D scene. Systems such as SceneSeer leverage spatial knowledge priors to infer implicit constraints and resolve spatial relations.

In this project we take a rather different approach. We explicitly focus on fiction books as input to our system. There are two reasons why we make emphasis on fiction books. For once, there is a complex world and rich semantic information that can be understood only by analyzing the long distance relations between text phrases and logical inference about salient objects in the scene. The second reason for us to focus on fiction was the gamification of the annotation process. It is much more fun to interact with a program about the meaning of the text in your favorite book than annotating long boring documents drafted by some administra-tive office. 

## Dataset Description

The SUMO SRL dataset release comprises two .json files: sentences.json and srl_physics.json.

The files are:
 * **sentences.json** sentences
 * **srl_physics.json** sentences that are anotated with labels PropBank, FrameNet, WordNet and SUMO SRL systems
 
The columns contain:

Column | Header                   | Description
:-----:|----------------          |--------------------------------------------
1      | rid                      | Unique identifer for an example 
2      | sentence                 | Text from book 
3      | it_is_OK                 | Marker that shows that anotations has been manually verified
4      | chapter_nr               | Chapter number from the book
5      | paragraph_nr             | Paragraph number. Starts from 1 for each chapter
6      | sentence_nr              | Sentence number in the paragraph
7      | it_is_dialogue           | Whether sentence belongs to dialog part or narator paer
8      | verb_id                  | Vern number in the sentence
9      | verb                     | Verb word
10     | frame                    | FrameNet frame name
11     | verb_WN                  | WordNet sysnset for the verb
12     | WebotsClass_verb         | SUMO SRL label (can be Motion , InMotion or NoMotion)
13     | WebotsClass_srl_ARG0     | SUMO SRL label for PropBank role ARG0
13     | WebotsClass_srl_ARG1     | SUMO SRL label for PropBank role ARG1
13     | WebotsClass_srl_ARG2     | SUMO SRL label for PropBank role ARG2


^ Please note that we are planning to change the data structure in future releases. 

^^ Also note that there are two types of entries, it_is_OK = 1 indicates that the record has been reviewed by a human editor and modified if necessary. We report the classification accuracy in the paper based on these records.

## SEMAFOR results


SEMAFOR: is a tool for automatic analysis of the frame-semantic structure. https://github.com/Noahs-ARK/semafor-semantic-parser
The SEMAFOR_results directory contains three text files for analysis results with this tool. 

Nr     | File name                           | Description
:-----:|-------------------------------------|--------------------------------------------
1      | SEMAFOR_frames.rpt                  | Sentences with a unique identifer. 
2      | SEMAFOR_sentences.rpt               | Frame targets (words that trigger the frame). 
3      | SEMAFOR_frames_annotations.rpt      | Frame anotations.

These files are used as a benchmark for the frame parsing. 



