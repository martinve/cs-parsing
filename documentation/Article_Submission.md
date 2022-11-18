# Enriching AMR parse trees with UD Graphs for Automated Knowledge Base Construction

One of the crucial tasks for constructing a knowledge base for commonsense question answering is to automate extracting background knowledge from unstructured sources. While structured data sources like ConceptNet, Quasimodo, Atomic and ontologies like WordNet provide facts and simple rules, they contain a lot of un-parsed English phrases and also lack most of the common everyday knowledge that everyone is expected to know. For both enriching these knowledge bases and asking questions using natural language, we need to perform semantic parsing of natural language phrases and sentences in a way that would be compatible with the structured data sources used.

The contribution of this paper is combining AMR and UD notations to perform the said task - extracting the meaning from unstructured texts and representing it as knowledge graphs that are transformed to first-order logic formulae that are then used for answering questions on the provided passage.

The paper provides an example for such an experimental system using the Graph Knowledge (gk) logic engine.

**Keywords:** knowledge extraction, natural language understanding, commonsense reasoning, meaning representations.





## Introduction

Humans are capable of solving tasks that need reasoning based on often incomplete information. That is possible due to having prior commonsense knowledge - facts about the everyday world everyone is expected to know. 







A crucial task for any reasoning system is collect



Question-answering systems that rely purely on vector-based approaches struggle with answering questions based on commonsense knowledge, the most apparent shortcoming being a lack of transparency and interpretability while performing inference. The results obtained may be caused either by actual correlations or superficial cues that have been demonstrated to exist in commonsense reasoning benchmarks. 

On the other hand, humans are capable of solving tasks that need reasoning based on often incomplete information. That is possible due to having prior commonsense knowledge - facts about the everyday world everyone is expected to know. Natural language is the medium of capturing such knowledge. Such representations capture the meaning of a sentence as understood by a native speaker to the point where it can be used to train a system for automated reasoning. The paper describes one such system used for constructing such a knowledge base. In addition, the paper describes experiments conducted measure the suitability such system.



##  The Task of Semantic Parsing

Semantic parsing, a sub-field of natural language understanding that maps natural-language utterances to detailed representations of their meaning. Such representations reflect the meaning of a sentence as understood by a native speaker to the point where it can be used for question answering or automated reasoning - one of such systems being **GK** \cite{Tammet2020}. 

Given a passage, it is transformed to a graph representation via the task of semantic parsing. As in general current semantic parsers use sentence as an unit of information, sentence segmentation task is performed. A context is created during the enhancement and transformation phase to overcome that limitation. The intermediate semantic parse result is enriched either with external information - e.g. Quasimodo \footnote{\url{https://quasimodo.mpi-inf.mpg.de/}}, DBpedia \footnote{\url{https://github.com/dbpedia/}}, Wikidata \footnote{\url{https://www.wikidata.org/}} or any other structured datasource. The representations are converted to first-order-logic formulate that can be saved and restored to be run on automated reasoner for question answering.



## Methodology

Prior to the experiment, a literature survey was conducted to identify the current state-of-the art in semantic representations of text and initial experiments were conducted to evaluate the suitability of said frameworks.

For constructing the experimental system, the following methodology was used:

1. Inputs and outputs were chosen for said system: Given a passage in English, syntactic and semantic information is being extracted and transformed to clauses JSON-LD-LOGIC. 

2. Validation methodology was developed and validation datasets chosen.

3. As a result the parsers and models were chosen: AMR for semantic representation and UD for syntactic and dependency parse trees. As both AMR and UD use sentence as a unit of meaning, a context was constructed that refers to the whole discourse.

4. An evaluation metric was chosen to measure the results of the parse. 

5. For constructing the context, three classes of  sentences were identified: conceptual, that do not describe specific situations but general concepts; factual that describe named entities and situational - describing concrete situations. A dictionary was constructed to map PropBank roles to predicates based on the sentence type. In addition a question transformer was constructed.

6. Logical forms in JSON-LD-LOGIC were constructed based on the sentences provided and an optional question answered.

7. Experiments were conducted on a corpus based on CommonsenseQA and the metrics were calculated. Further development goals of said system were identified.

8. The performance of the system was measured against the TPTP system to validate the whole workflow.

   

## Experiment Setup

This section describes the experimental settings used for conversion.

### Formats and Standards

Due to the ambiguous nature of natural language no unified framework or notation exists that is capable of capturing different attributes of spoken language. The author conducted a survey and comparative evaluation for existing state-of-the art semantic parsing frameworks \cite{Verrev2021}.

**AMR** is a notation based on on propositional logic and neo-Davidsonian semantics. AMR encodes the semantics of a sentence into a directed graph. Nodes in the graph represent terms in the sentence and the edges identify the semantic relations between nodes. Concepts can be either English verbs, PropBank framesets, or specific keywords. AMR includes frame arguments based on Propbank conventions, general semantic relations; and relations for quantities, date-entities, and lists. It lacks universal quantifiers and support for inflectional morphology. Annotations do not link between concept and original span -- thus input needs to be aligned first \cite{Chen2017}. AMR 3.0 has two aligned corpora publicly available. 

**Universal Dependencies** is a framework for consistent annotation of grammar. It solves the problem of different corpora having different tagsets and annotation schemes \cite{Zeman2008} by providing universal scheme and category set: suitable for parser development, cross-lingual support and language parsing, allowing language-based extensions if necessary \cite{Haverinen2014}. It combines Stanford Dependencies, Google universal part-of-speech tags, and Interset interlingua\footnote{\url{https://ufal.mff.cuni.cz/interset}} for morphosyntactic tagsets - e.g. encoding additional morphological information to the syntactic form \cite{Nivre2020}. UD corpora consist of over 200 treebanks in over 100 languages. 

\textbf{JSON-LD-LOGIC} \url{https://github.com/tammet/json-ld-logic} is a notation combining first-order logic with JSON that is compatible with both JSON-LD standard and TPTP format. This enables the programmatic management of logical problems and provides a specification for output format for the knowledge base so created. The format thus allows to encode knowledge from different sources in unified format.

\textbf{TPTP} is comprehensive library of test problems for automated theorem proving (ATP) systems. We will use the TPTP PUZ001+1.p theorem was chosen for final evaluation of the system.

### Choice of Technologies

Amrlib, a Python module for parsing AMR graphs from English sentences was chosen with Parse T5 0.20.0 model6. Stanza 7, a Python NLP toolkit was
used for text processing tasks: text tokenization, named entity recognition, partof-speech tagging, constituency parsing, dependency parsing and lemmatization.



### Evalutation Datasets and Metrics

The following evaluation metrics were indentified from \cite{Santos2020}:

\emph{Smatch} score \cite{Cai2013} is an evaluation metric for comparing two whole-sentence AMR graphs.  An AMR graph can be viewed as conjunction of logical triples. Smatch score computes the maximum match number of triples among all possible variable mappings and gets the F-score, precision, and recall.

General Language Understanding Evaluation \textbf{(GLUE)} \cite{Wang2019} and SuperGLUE \cite{Wang2020} are  model-agnostic benchmarks for natural language understanding. not tailored to specific domain or dataset. The datasets contain both word knowledge, common sense and logical entailments \url{https://super.gluebenchmark.com/diagnostics/}.

Bilingual Evaluation Understudy \emph{(BLEU)} \cite{Papineni2002} is a metric for evaluating machine translated text from one natural language to another. SEMBLEU \cite{Song2019} is an extension of BLEU metric

Complementary Commonsense \textbf{(COM2SENSE)} \cite{Singh2021} is a commonsense reasoning benchmark of 4000 natural language sentence pairs that can be either true or false. The dataset is constructed across both knowledge domains (physical, social, temporal) and resasoning scenarios (causal, comparative)

\textbf{CommonsenseQA} \cite{Talmor2019} is a multiple choice multiple-choice question answering dataset that requires commonsense knowledge based on ConceptNet relations

## Extracting the Logical Form

Given the input passage - it is split to sentences. Given a compound sentence it is further split and added to sentence stack. Each sentence is classified per type. If no type can be determined given the sentence is ignored. Logical form is constructed for a sentence and added to the context. The system measures if the last given sentence in a passage is a question. If a question is presented a type of question is determined and the system attempts to answer it based on the context given.

### Sentence Classification

We classify the sentence into three categories: 
#### Conceptual statements

Conceptual statements do not describe a specific situation and are not dependent on uncommon circumstances. Typically they describe concepts or relations between concepts.

``

#### Fact Statements

Fact statements describe named entities and are also not dependent on uncommon circumstances.


#### Situational statements
Situational statements describe a concrete situation and events happening within this situation.


To validate the classification accuracy an experiment was constructed. A dataset was chosen for each individual sentence type. Heuristics based on UD were constructed to classify the sentences. A classifier was constructed and \emph{F1} score calculated to verify the accuracy of the classifier. 

\begin{table}[ht]
    \begin{tabular}{llr}
        \hline
        Sentence Type & Dataset & F1 Score \\
        \hline
        Conceptual & OpenbookQA \tablefootnote{\url{ https://ai2-public-datasets.s3.amazonaws.com/open-book-qa/OpenBookQA-V1-Sep2018.zip}} & 0.00 \\
        Fact &  DBPedia 1.4 \tablefootnote{\url{https://huggingface.co/datasets/p}} & 0.00 \\ 
        Situational &  Winograd \tablefootnote{\url{Winograd & https://huggingface.co/datasets/winograd\textunderscorewscp}} & 0.00 \\
        \hline
    \end{tabular}
    \caption{Sentence classification evaluation results}
\end{table}


### Question Identification and Classification

The system answers three types of questions based on the context. (a) \emph{Boolean} questions return a truth value based on the generated knowledge base. (b) \emph{Object-by-property} questions return an object having a given property. (c) \emph{Property-by-object} questions describe a given object and given or derived properties of said object. 

% The type of each sentence is determined (conceptual, fact, situational). In addition a question may be added to the % passage. The question can be of three types: returning true/false based on previous facts, returning an object by a % property or returning an object by a property.

To validate question type classification a set of questions were constructed for each type and conversion results observed. 

### Ontology Construction

A minimal ontology was constructed to provide interoperability across several contexts. Based on sentence class, mappings were generated for AMR core attributes. The following rules were applied

1. For verbs, lemmatized version was used as a predicate: 'walk-01' -> 'walk'
2. For custom AMR predicates, e.g `have-org-role-91` a mapping to `property` predicate was created
3. Sentence class based semantic role mappings were applied, e.g. ARG0 means agent in general but instrument in other contexts (TODO: Example).

### Context Creation

To keep track of entities in passage and a sequence of events,context placeholder was created. For describing situations it was assumed that the sequence of sentences follows the sequence of events. Additionally the context keeps track of concepts and named entities: having "John" occurring in a passage and later "he" we can assume that "he" refers to "John" when answering questions.

The purposes of context object are:

- Keeping track of named entities. 
- Keeping track of events. 
- Keeping track of quantifiers. This information is lost via AMR parse. 




### AMR to Logic Transformation

Construction of logical form consists of the following steps:

1. Find predicates, specify their arguments (number, type)
   1.1 Concepts and events - predicate/1
   1.2 Roles - predicate/2
2. Construct corresponding atoms
3. Divide atoms on same level into groups
4. Specify connectives between atoms of each group and construct corresponding formulas.
5. Divide formulas and/or any of the remaining atoms of the same level into groups. If there are no groups go to step 7
6. Specify connectives between elements of each group
7. Specify quantifers for the variables.
8. Construct final FOL formula.

\subsection{Limitations of pure AMR-based approach}

AMR parse graphs are represented in Penman notation with well formed results that can easily parsed to first order logic \cite{Bos2016} as demonstrated by \emph{amr2fol} \footnote{\url{https://github.com/papagandalf/amr2fol}} project. Still, AMR has several constraints when parsing natural language and fails unexpectedly. This is not due to the limitations of AMR itself but more due to the ambiguous nature of natural language. Given general domain it is not possible to craft the rules or train the model that covers the full scope of the language.

Two types of inconsistencies were recognized when conducting the preliminary experiments:
\begin{itemize}
    \item \textbf{Informational} where incorrect or wrong type information is inferred. 
    \item \textbf{Structural} where the structure of the parse tree does not reflect its true meaning.
\end{itemize}

In addition it was recognized that AMR does not support scenes (in contrast to UCCA), thus manual context creation similar to the approach described here: http://arxiv.org/abs/2112.08513. 


 ### Examples of Informational Inconsistencies

$$
::snt Brutus and Caesar are Romans.
 (p / person
      :mod (c / country
            :name (n / name :op1 "Roman"))
      :domain (a / and
            :op1 (p2 / person :name (n2 / name :op1 "Brutus"))
            :op2 (p3 / person :name (n3 / name :op1 "Caesar"))))
$$

$$
 # ::snt Romans can stab.
(p / possible-01
      :ARG1 (s / stab-01
            :ARG0 (p2 / person
                  :mod (c / country :name (n / name :op1 "Romania")))))
$$

For given sentence country name is extracted. The information is not correct as country with name \emph{Roman} does not exits. Given the second sentence, \emph{Romania} is inferred as a country name. Both assumptions are not correct. The same can be noted with the parse for \emph{The colors for flag of Latvia are red. and white} where the country name is stated as \emph{Lettonia} or \emph{Lebanon}.

$$
# ::snt Percy is a cat.
(c / cat
      :domain (p / person
            :name (n / name
                  :op1 "Percy")))
$$

While it is explicitly stated that type of Percy is cat, AMR maps it to generic \emph{person} entity. The graph can pe interpreted as: \emph{Person having a name Percy is a cat}.

 ### Examples of Structural Inconsistencies

$$
# ::snt The colors of Estonian flag are blue, black and white.
(c / color-01
      :ARG1 (f / flag
            :mod (c2 / country
                  :name (n / name
                        :op1 "Estonia")))
      :ARG2 (a / and
            :op1 (b / blue)
            :op2 (b2 / black-and-white)))
\end{verbatim}

Given the colors black and white are not recognized as list but a phrase \emph{black-and-white} is extracted.
$$

$$
 # ::snt Agatha, the butler, and Charles live in Dreadbury Mansion, and are the only people who live therein.
...
      :op1 (l / live-01
            :ARG0 (a2 / and
                  :op1 (p / person
                        :name (n / name
                              :op1 "Agatha")
                        :ARG0-of (h / have-org-role-91
                              :ARG2 (b / butler)))
                  :op2 (p2 / person
                        :name (n2 / name
                              :op1 "Charles")))
...
$$

Fragment of a parse. Agatha and Charles are recognized as participants in the scene, but \emph{Butler} is assumed to be the role of Agatha.





## Results 

A pilot system was constructed to extract logical representations from text. The system consists of a server that initializes the models. Client is used to perform the parse and fetch the results from server. 



% TODO: Examples where UD and AMR do not perform as well separately as together.

% CAT EXAMPLE - SOME EXTRA STUFF
% BRUTUS EXAMPLE


The pipeline is the following:
1. Given a passage tokenize it to sentences.
2. For each sentence analyze the semantic and syntactic structure 
3. Combine the context
4. Given question parse the question and answer it on generated clauses. 



\section{Dreadbury Mansion Example}

To verify the performance of the whole workflow, Dreadbury Mansion example (@article Seventy-five problems for testing automatic theorem provers. https://sci-hub.se/10.1007/bf02432151), (@code TPTP Problem File TPTP Problem File: PUZ001+1.p http://tptp.cs.miami.edu/cgi-bin/SeeTPTP?Category=Problems&Domain=PUZ&File=PUZ001+1.p) was chosen. 

\say{Someone who lives in Dreadbury Mansion killed Aunt Agatha. Agatha, the butler, and Charles live in Dreadbury Mansion, and are the only people who live therein. A killer always hates his victim, and is never richer than his victim. Charles hates no one that Aunt Agatha hates. Agatha hates everyone except the butler. The butler hates everyone not richer than Aunt Agatha. The butler hates everyone Aunt Agatha hates. No one hates everyone. Agatha is not the butler.}

The original passage was modified:

* Sentence 2: `the` omitted from butler. Now butler is recognized as individual entity. 
* Sentence 1: removed and question added at the end of sentence: `Who killed Aunt Agatha`

The individual sentence was parsed and context created:

### {Modified Passage}


1. Agatha, butler, and Charles live in Dreadbury Mansion, and are the only people who live therein. (type=sit)
    2.1 Agatha, butler, and Charles live in Dreadbury Mansion. (type=sit)
    2.2 Agatha, butler, and Charles are the only people who live therein. (type=fact) 

2. A killer always hates his victim, and is never richer than his victim. 
    2.1 A killer always hates his victim (type=concept)
    2.2 A killer is never richer than his victim (type=concept)
    

Comment: Sentence split if AMR root == and    

3. Charles hates no one that Aunt Agatha hates. (type=fact)

4. Agatha hates everyone except the butler. (type=sit)

5. The butler hates everyone not richer than Aunt Agatha. (type=sit)

6. The butler hates everyone Aunt Agatha hates. (type=sit)

7. No one hates everyone. (type=sit)

7. Agatha is not the butler. (type=fact)

8. Who killed Aunt Agatha? (type=ques)


\section{Limitations}

\begin{itemize}
    \item \emph{Compound sentences.} Given compound sentences they were split prior to parsing
    \item \emph{Context order.} It is assumed the events in passage occur in the order the sequence of sentences provided.
    \item \emph{Question detection and scope. } It is assumed the questions are provided at the end of the passage. The naive approach assumes that question ends with a question mark or starts with one of the seven question words in English.
\end{itemize}




\section{Future Work}
	
[TBC]






\section{Discussion}

Discussion of examples.

