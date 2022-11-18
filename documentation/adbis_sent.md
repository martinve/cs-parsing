\section{Introduction}\noindent
We are surrounded by intelligent and sophisticated technologies that are ”smart” in the sense that they excel in performing domain-specific tasks but are often found lacking where general knowledge is required. On the other hand, humans are capable of solving tasks that need reasoning — the capacity of making sense of things, applying logic, adapting to or justifying practices and beliefs based on often incomplete information. It is possible due to having prior commonsense knowledge - facts about the everyday world everyone is expected to know.  Natural language is the medium that captures such knowledge. 

While there have been noteworthy advancements in the field of natural language understanding, e.g. commonsense transformer models, the question-answering systems rely purely on vector-based approaches struggle with answering questions based on commonsense knowledge, most apparent shortcoming being a lack of transparency and interpretability. The results obtained may be caused either by actual correlations but also due to superficial cues that have been demonstrated to exist in CSR benchmarks \cite{Kavumba2019}. An efficient method needs to be developed to extract, parse, and store knowledge from existing sources to train a system capable of logical inference, otherwise, we do not have a large enough training corpus for such a system. 

The current paper focuses on semantic parsing, a sub-field of natural language understanding, concerned with mapping natural-language utterances to detailed representations of their meaning in formalized representation languages - having an ontology of types, properties, and relations. Representations thus generated go beyond shallow identification of roles and objects in a sentence and reflect the meaning of a sentence as understood by the native speakers of the said language, being both machine and human-readable. 

While numerous meaning representation notations exist, none of them has been universally accepted. \cite{Kamath2019} Several technologies exist that all seem to capture various aspects of the meaning but fail in different, often unexpected contexts. Therefore it is crucial to investigate and conduct experiments on existing technologies and provide a systemic approach for evaluating such technologies. 

A question arises if semantic parsing, being is such an ambiguous field, is needed at all. It may be possible to capture the meaning by combining machine learning methods with those of syntactic parsing. While sufficient for capturing shallow relationships, syntactic parsing is not enough. Let us consider the following sentences: \emph{“A man opened the door”} and \emph{“A key opened the door”}. While syntactically similar, the role of participants is different - agent as an instigator in case of \emph{man} and patient, entity undergoing the effect of an action in case of \emph{key}. Thus the meaning of the sentence is entirely different, and to understand it, we must go beyond the syntactic level of language. 


\begin{figure*}[ht]
\resizebox{\textwidth}{!}{
\begin{tikzpicture}[%
    node distance=4cm, auto, text centered
    edge from parent/.style={draw,latex-},
    round/.style = {circle, draw=black, minimum size=2.5cm},
    square/.style={rectangle, minimum size=2cm},
    every node/.style = {align=center, scale=0.8}
    ]
    
    % Nodes
    \node[square](cs_knowledge)[text width=3cm]{\small\uppercase{Commonsense Knowledge}};
    \node[round](parsing)[text width=2cm, right of=cs_knowledge]{Semantic Parsing};
    \node[square](meaning_representations)[right of=parsing, text width=3cm]{\small\uppercase{Meaning Representations}};
    \node[round](enrichment)[text width=2cm, right of=meaning_representations]{Enrichment and Transformation};
    \node[square](logical_form)[text width=1.5cm, right of=enrichment]{\small\uppercase{Logical Forms}};
    \node[round](reasoning)[right of=logical_form]{Automated\\Reasoning};
    
    % Arrows
    \draw[->] (cs_knowledge.east) -- (parsing.west);
    \draw[->] (parsing.east) -- (meaning_representations.west);
    \draw[->] (meaning_representations.east) -- (enrichment.west);
    \draw[->] (enrichment.east) -- (logical_form.west);
    \draw[->] (logical_form.east) -- (reasoning.west);

\end{tikzpicture}
}
\caption{A broad overview of constructing a knowledge-base in the context of automated reasoning.} \label{fig:M1}
\end{figure*}

The contribution of the paper is a review of the existing frameworks and a comparative study in the field of semantic parsing - being valuable for both the researcher and the practitioner who needs to start applying the parsers in his or her knowledge extraction and formalization tasks.


\section{Research Question}

The paper targets an accurate, efficient and extensible method for meaning extraction for automated graph-based commonsense knowledge base construction. For this, the following research questions were stated:

\begin{itemize}
    \item \textbf{RQ1:} What is the current state of the art in the field of semantic parsing?
    \item \textbf{RQ2:} What are the criteria for choosing a parser for semantic parsing task?
    \item \textbf{RQ2:} What is the optimal parser or set of parsers for knowledge-base construction for commonsense reasoner?
\end{itemize}

\section{Methodology}

% \hl{[TBC: and publications since 2019]}

During the preliminary phase, a review was conducted of existing semantic parsing frameworks to identify the key features and attributes for each framework. The following characteristics for each representation were identified: (a) \emph{goals}: primary features and driving motivation behind the framework; (b) \emph{research:} anchor and other notable publications. (c) \emph{theories:} linguistic and logical theories behind the framework; (d) \emph{data} underlying datasets, availability of annotated corpora and semantic representation; (e) \emph{tooling:} availability of parsing and visualization tools. 

%nTODO: How did I select the frameworks? Mingi tabel oleks abiks

After selecting the frameworks for further analysis, the parsing tools were reviewed and chosen for each notation based on the following attributes: (a) publicly available source code to re-create the results. (b) availability of journal articles or conference papers regarding said tool and (c) available corpora and models to re-create experiments described in said articles.

For conducting the experiments, a representative sample of said tools was chosen: for frameworks having over two parsers, the following criteria was applied: \emph{development activity} - how active and up-to-date the development of said parser is; \emph{accuracy} - the parsing accuracy of said tool based on literature; and \emph{lightness} - given a choice between otherwise matching and equally performant parsers, the more lightweight one was chosen. In addition, a minimal corpus was constructed for capturing the essential linguistic features during the experiments.

For the evaluation of parse results, a scale was constructed to evaluate the performance of said parsers. Due to different notations and aspects captured, two distinct scales were defined: qualitative hand-evaluation for \emph{correctness}: how accurately does the parser capture the meaning and quantitative evaluation \emph{expressiveness}: how much information does it capture.  The frameworks were assessed on said scales. 

After evaluating the performance, a qualitative analysis was conducted, taking into account the features of the framework given for the suitability of using it in a preliminary step for constructing a commonsense knowledge base. 

\section{Semantic Representation Frameworks}

The following frameworks were chosen for further analysis during preliminary phase as described in previous section.

\subsection{Abstract Meaning Representations}

Abstract Meaning Representation (AMR) is a semantic formalism based on propositional logic and the neo-Davidsonian 
event representations where each representation is a single-rooted, directed graph. AMR is strongly biased towards English though it does support multilingual meanings. Its concepts are either English verbs, PropBank framesets, or specific keywords. AMR also supports NER, question detection, within-sentence co-reference, modality and question identification. Limitations of AMR are lack of universal quantifier and missing inflections for tense and number. AMR 3.0 has two corpora publicly available with licensing terms not specified, with additional corpora available for LDC members.  \emph{ The Little Prince Corpus} consists of 1562 and \emph{Bio AMR Corpus} of 6952 sentences.

AMR parsers have numerous implementations - on Github alone, there are 45 projects tagged as so. \textbf{JAMR} \footnote{\url{https://github.com/jflanigan/jamr}} parser was initially constructed for Semeval-2014, and the most recent commit to the repository was in March 2019. The repository has 825 commits in total. JAMR is built on Scala 2.0 and is supported by 200 hand-aligned sentences of the AMR corpus. \textbf{Transition AMR Parser} \footnote{\url{https://github.com/IBM/transition-amr-parser}} is a transition-based parser for AMR built on top of Pytorch. It consists of a State machine and oracle transforming the sequence-to-graph task into a sequence-to-sequence problem and a sequence to sequence model that encodes the stack and buffer state of the parser into its attention heads. The repository has 1128 commits, the last being made in March 2022. \textbf{amrlib} \footnote{\url{https://github.com/bjascob/amrlib}} is a Python3 library built on Pytorch for AMR parsing, generation, and visualizations that can also be used as a Spacy library. The repository has 156 commits, the last of them made in March 2022. 


\subsection{Universal Conceptual Cognitive Annotation}

Universal Conceptual Cognitive Annotation (UCCA) is a language-agnostic annotation scheme based on Basic Linguistic Theory. Natural language utterances are converted to a graph containing purely semantic categories and structure, whereas syntactic categories and structure are discarded. The meaning representations are not for any specific domain or language - but provide a coarse-grained interpretation that allows for open-ended and partially automated extension using cognitively motivated categories. The foundational layer can be extended by adding an extra domain or language-specific layers. The focus of UCCA has been been the ease of annotation. Base element of the foundational layer is a \emph{scene} - describing movement, action or event \cite{Abend2013}. UCCA has annotated corpora in English, French, and German available under the Creative Commons 3.0 license. 

The following parsers exist for UCCA at the time of the writing of paper: \textbf{UCCA Parser} \footnote{\url{https://github.com/SUDA-LA/ucca-parser}} was constructed for 2019 SemEval Task 1: 
SemEval 2019 Task 1: Cross-lingual Semantic Parsing with UCCA \href{https://competitions.codalab.org/competitions/19160} and runs on Python3 and Pytorch. The project has 6 commits, the last made in June 2019. \textbf{TUPA} is a transition-based UCCA parser \footnote{\url{https://github.com/danielhers/tupa}} based on bidirectional LSTM. The project has 2135 commits, and the last commit was made in June 2020. 


\subsection{Universal Dependencies}

Universal Dependencies \footnote{\url{https://universaldependencies.org/}} (UD) is a project that combines Stanford Dependencies, Google universal part-of-speech tags, and the Interset interlingua for morphosyntactic tagsets for encoding additional morphological information to the syntax. \cite{Nivre2020} UD provides universal annotation scheme and a set of categories for multilingual corpora consisting of over 200 treebanks in over 100 languages. \cite{Haverinen2014}



\textbf{UDepLambda} \footnote{\url{https://github.com/sivareddyg/UDepLambda}} \cite{Reddy2017} is a parser that performs semantic parsing on UD corpus and transforms the text into lambda calculus. The parser is implemented in Java 8 with 225 commits, with the latest commit done in July 2018. \textbf{uuparser} \footnote{\url{https://github.com/UppsalaNLP/uuparser}} \cite{Kiperwasser2016} The parser is based on cython 3.7+ and is notable for ability to parse the input texts on multi-treebank models. The repository has 125 commits, the most recent of which was in October 2020. 


\subsection{Elementary Dependency Structures}

Elementary Dependency Structures (EDS) \footnote{\url{http://moin.delph-in.net/wiki/EdsTop}}
present an approach to Minimal Recursion Semantics (MRS) banking. 
MRS is an approach where each input item in a corpus is paired with elementary predicates - meaning single relation with its associated arguments - followed by manual disambiguation of quantifiers.  \cite{Copestake2005} The semantic form is based on the notion of semantic discriminants - local dependencies extracted from full-fledged semantic representation. \cite{Oepen2006}



\textbf{PyDelphin} \footnote{\url{https://github.com/delph-in/pydelphin}} is a toolkit that supports EDS, MRS and DMRS formalisms. The project is written in Python with 1023 commits, the latest being made in October 2021. \textbf{HRG Parser} \footnote{\url{https://github.com/draplater/hrg-parser}} is a string-to-graph parser for EDS graphs. The parsing is done in two steps - syntactic parsing using SHRG grammars and semantic interpretation.  The project is written in Python with 4 commits, the last being made in May 2018.


\subsection{Prague Tectogrammatical Graphs}

Prague Tectogrammatical Graphs \cite{hajic-etal-2012-announcing} (PTG) provides annotations in
English and Czech languages. The English sentences are from a complete English Web Text Treebank \footnote{\url{https://catalog.ldc.upenn.edu/LDC2015T13}} and a parallel Czech corpus morphologically annotated and parsed into surface-syntax
dependency trees in the Prague Dependency Treebank (PDT) 2.0 annotation style based on the same sentences. Noteworthy is the annotations having multiple layers - analytical (surface-syntax) layer consisting of dependency structures, semantic labels, argument structure, and ellipsis resolution; and a manually constructed deep-syntax tectogrammatical layer on top of that. \cite{Hajic2012} 

 

\textbf{PERIN} \footnote{\url{https://github.com/ufal/perin}} is an universal cross-framework semantic parser for five frameworks for CONLL 2020 shared task \emph{Cross-Framework Meaning Representation Parsing (MRP2020)} \footnote{\url{http://mrp.nlpl.eu/2020/}} that supports AMR, DRG, EDS, PTG and UCCA formalisms. \cite{Samuel2020}  The repository has 36 commits, the most recent of which was in October 2021. 


\subsection{Discourse Representation Structures}

Discourse Representation Structures (DRS) is a semantic formalism based on Discourse Representation Theory. In contrast to ordinary treebanks, the units of annotation in corpus are texts rather than isolated sentences. \cite{Basile2012}. Basic DRSs consist of discourse referents ($x$) representing entities and discourse conditions ($man(x)$) representing information about discourse referents. \cite{Liu2018} The corpus is based Groningen Meaning Bank that annotates English texts with formal meaning representations rooted in Combinatory Categorial Grammar\cite{Bos13}. 

\textbf{TreeDRSparsing} \footnote{\url{https://github.com/LeonCrashCode/TreeDRSparsing/tree/bs_sattn_drssup}} is an English to DRTS labelled tree parser using multi-head attention model that also includes pre-trained embeddings. The parser is built on Python2, and the repository has 59 commits in total in \verb!bs_sattn_drssup! branch, with the latest being made in March 2020. \textbf{EncDecDRSparsing}\footnote{\url{https://github.com/EdinburghNLP/EncDecDRSparsing}} is an open-domain neural semantic parser performing prediction in three stages: structure prediction, predicate and relation prediction, and variable prediction. \cite{Liu2018a} The parser is built on Python 2.7 and Pytorch. The data and pre-trained word embeddings are linked within the repository. The repository has 15 commits, the most recent of being made in August 2019.


\subsection{Universal Decompositional Semantics}

Universal Decompositional Semantics \footnote{\url{http://decomp.io/}} (UDS) framework is different from other formalisms because it decodes the meaning in a feature-based scheme — using continuous scales rather than categorical labels. The meaning is captured as
a node- and edge-level attribute in a single semantic graph having 
the structure deterministically extracted from Universal Dependencies.
UDS treats parsing as a sequence-to-graph problem - the
graph nodes created are based on input sequence, and edges are
dynamically added during generation. \cite{White2016} \textbf{PredPatt} \footnote{\url{https://github.com/hltcoe/PredPatt}} is a seq2seq parser for UDS written in Python3 and using either Stanford or Berkley dependencies. Predpatt can be used for layering semantic annotations atop UDS treebanks or considered a component for universal information extraction. It is a part of Decomp Toolkit - a toolkit for working with the UDS dataset - the dataset having 70 657 annotated nodes in total\cite{White2019}. The project has 59 commits, with the most recent being made in February 2021. \textbf{MISO} \footnote{\url{https://github.com/esteng/miso_uds}} is a transformer-based, multi-formalism deep learning network that transforms the utterance into a UDS graph amongst others, built heavily on top of AllenNLP. The project has 1019 commits, with the most recent done in September 2021. 


\subsection{Hobbsian Logical Form}

In addition to semantic parsing frameworks, \emph{Hobbsian Logical Form} \footnote{\url{https://isi.edu/~hobbs/csk.html}}  (HLF) was added to the experiment tooling for parsing the results directly to logical form for evaluation whether it is viable to perform translation to logical clauses and proof-graphs without intermediate semantic representations. \textbf{Interpret} \footnote{\url{https://github.com/jgordon/interpret}} is a parser to transform natural language utterances into HLF. It is written in Python3, the project having 77 commits, with the most recent done in July 2018. The work was supported by DARPA "CWIC: Communicating Intelligently with Computers" \footnote{\url{https://www.darpa.mil/news-events/2015-02-20}} project.



\section{Results and Evaluation}

%iffalse
The input and output data for experiments can be found at [anon].
%fi

\subsection{Test Corpus}

Usually the generated representations are compared to gold-standard annotations to evaluate the quality of parse results. Due to a variety of frameworks with different representation schemes, we do not have such annotations.

Thus  a test corpus was constructed consisting of 351 sentences (3858 tokens) from initial experiments conducted for evaluating the robustness of parsers. The sources for sentences were: CommonsenseQA\footnote{\url{https://huggingface.co/datasets/commonsense_qa}} (312 sentences), Geoquery Data \footnote{\url{https://www.cs.utexas.edu/users/ml/nldata/geoquery.html}} (5 sentences) and synthetic examples capturing the essential linguistic features for translating the text to logical form (32 sentences). These features are: handling simple facts; extraction of predicates from traditional set theory; extraction of universal and existential quantifiers; handling of negation; handling logical connectives: conjunction, disjunction, and implication; handling of equality; handling of multiple variables and identification and extraction of questions. The corpus was constructed of 312 sentences from CommonsenseQA, 5 sentences from Geoquery data and 32 synthetic sentences to cover all the mentioned linguistic features. After initial experiments, the baseline test corpus was pruned, and as a result, minimal corpus - consisting of 58 sentences (594 tokens) remained.

\subsection{Frameworks, Tools, Models}

The frameworks were summarized based on the unit of information and parse depth to conduct the further experiments.

\begin{table}[ht]
    \centering
    \caption{Framework, unit of information and parse depth for identified frameworks }
    \begin{tabular}{l@{\hskip 1cm}l@{\hskip 1cm}r@{\hskip 4pt}}
        \toprule
        Framework & Unit & Depth \\ 
        \midrule
        AMR & sentence &   deep-semantic	\\
        UCCA & sentence & deep-semantic	\\
        UD & sentence & morphosyntactic	\\
        EDS & sentence & logical \\
        PTG & sentence & morphosyntactic \\
        DRS & passage & logical \\
        UDS & sentence & shallow-semantic \\
        HLF & sentence & logical \\
        \bottomrule
    \end{tabular}
\end{table}

AMR and UCCA were chosen for deep-semantic parsing. UDS was added to the test set for comparative shallow-semantic results. DRS was rejected due to being the only framework supporting passage due to having passage instead of a sentence as a unit of annotation. UD and PTG were rejected due to not supporting the semantic depth. HLF logical form was added to the test battery to evaluate the viability of direct translation of sentences to logical form and interpretability of the representations thus generated. The parsers and models used are summarized in the table below:

\begin{table}[ht]
    \centering
    \caption{Tooling for parsing minimal corpus}
    \begin{tabular}{lll}
        \toprule
        Framework & Parsers & Model \\
        \midrule
        AMR & amrlib & Parse T5 v0.1.0% \tablefootnote{\url{https://github.com/bjascob/amrlib-models}} \\
        \\
        UCCA &  TUPA  & ucca-bilstm-1.3.10% \tablefootnote{\url{https://github.com/huji-nlp/tupa/releases/download/v1.3.10/ucca-bilstm-1.3.10.tar.gz}} \\
        \\
        UDS & PredPatt & UDS 1.0 % \tablefootnote{\url{http://decomp.io/data/}} \\
        \\
        HLF & Interpret & \emph{built-in} \\
        \bottomrule
    \end{tabular}
\end{table}

% \subsection{Parse Output}

Meaning representations vary greatly depending on the framework used. Here we explore the parse graphs for a  sentence  \emph{“Glass does not conduct electricity”}. 

% \subsubsection{Abstract Meaning Representations}

\textbf{AMR} parse graph is intuitive to interpret and does not need post-processing for evaluation. The graph is represented in Penman notation, being straightforward to process further if required. The negative polarity is explicitly denoted by \verb!polarity! attribute and in the case of question detection it is represented by \verb!amr-unknown! keyword.

\begin{figure}[ht]
\centering
\begin{BVerbatim}[fontsize=\small]
(c / conduct-01
    :polarity -
    :ARG0 (g / glass)
    :ARG1 (e / electricity))
\end{BVerbatim}
    \caption{Example AMR parse result}
\end{figure}

% \subsection{Universal Conceptual Cognitive Annotation}

\textbf{UDS} parse results are intuitive to read. Due to the UD parsing mechanism - annotations are added as labels and not as an acrylic graph - the parser performs extremely well on complex sentences. During the initial experiments, no breakage was encountered. Verbose UDS parse added also dependency relations\footnote{\url{https://universaldependencies.org/en/dep/}} to the parse graph, while simplified parse graphs omitted such features.

\begin{figure}[ht]
\centering
\begin{BVerbatim}[fontsize=\small]
Glass does not conduct electricity.
    ?a does not conduct ?b[ conduct-root,
    add_root(conduct/3)_for_dobj_from_(electricity/4),
    add_root(conduct/3)_for_nsubj_from_(Glass/0),n1,n1,n1,n2,n2,u]
		?a: Glass	[Glass-nsubj,g1(nsubj)]
		?b: electricity	[electricity-dobj,g1(dobj)]
\end{BVerbatim}
\caption{Example of verbose UDS parse result}
\end{figure}


\textbf{UCCA} parse graph is generated via intermediate step. The output for the parser was in XML format - one item for each sentence. The intermediate XML results were additionally processed using \emph{ucca-tool}\footnote{\url{https://github.com/sriram-c/ucca-tool}} to visualize the constructions. In addition to textual representation, graph representations were created for each result using the said tool.

\begin{figure}[!h]
\centering
\begin{BVerbatim}
    corpus-min_0007:
      Light verbs: 1.1->1.2 [F does]
      Participant:
        1.1->1.3 [A [E not] [E conduct] [C electricity] ]
        1.1->1.27 [A Glass]
      ...
      Center:
        1.3->1.8 [C electricity]
\end{BVerbatim}
\caption{A fragment of UCCA parse result}
\end{figure}

The parse result is a combination of UCCA foundation-layer categories: e.g., \emph{glass} as a primary participant in said sentence denoted by category \emph{A}.


% \subsubsection{Universal Decompositional Semantics}


\textbf{HLF} output resulted in the highest expressiveness. Parse graph is easy to post-process due to Lisp-like syntax, but also difficult to interpret. 

\begin{figure}[ht]
\centering
\begin{BVerbatim}[fontsize=\small]
(O (name 1)
(^ (glass-nn e6 x1)
  (nam e7 x1)
  (not e3 e1)
  (electricity-nn e5 x2)
  (conduct-vb e1 x1 x2 u4) (!= e6 e7)))
\end{BVerbatim}
\caption{Example HLF parse result}
\end{figure}

Due to variations in formalisms, the following scales were constructed: \emph{expressiveness} - the granularity of linguistic features captured, and \emph{correctness} - whether the representation generated matches expected form.

$Expressiveness$ was calculated as the ratio of tokens in input sentence \emph{vs} number of semantic attributes captured, averaged over the whole corpus. To evaluate $correctness$ human evaluation was conducted by the author. In addition to textual representations, graphical representations were generated for UCCA and HLF to aid in evaluation. 
Each result was manually graded on a scale of 0..1. If the information captured was deemed complete and accurate, it was graded 1. If a portion of information was missing, it was graded 0.5. If arbitrary or non-relevant information was added - as it is hard to detect such errors in the knowledge base, the score was lowered by 0.3 points. If essential information was not present or the parse failed, the grade was 0. For each framework, the grades were averaged over the whole corpus.

% TODO: For the sentence '' the parse ... . 

\begin{table}[ht]
    \centering
    \caption{Comparative summary of correctness and expressiveness values for semantic parsing frameworks}
    \begin{tabular}{lrrr}
        \toprule
        Framework & Parser & Correctness & Expressiveness \\
        \midrule
        AMR & AMRLib & 0.94 & 0.14 \\
        UCCA & TUPA & 0.96 & 0.19 \\
        HLF & Interpret & 0.91 & 0.20 \\
        UD & PredPatt & 0.92 & 0.08 \\
        \bottomrule
    \end{tabular}
\end{table}



\iffalse
In addition to performance, each framework was evaluated on the following attributes: research, data, parsers, and understanding. Each attribute was graded on a scale of 0 to 1. For performance, the result evaluation was used. 
\fi

% TODO: Iga valiku tegemisel 1x seda uuesti viidata
% TODO: Tabel kus asjad feilisid


\section{Conclusions}

Due to ambiguous nature of natural language, no parser alone is ideally suitable for the task. On the other hand, all the parsers chosen performed well in different aspects of capturing the meaning. The robustness of UDS is suitable for pre-processing the input - simplifying the structure of the sentence and splitting it into key components. At the same time the splitting boundary for some input sentences seemed arbitrary. On the other hand, AMR is suitable for explicit negation extraction and question detection. Also, the Penman output format is suitable for further post-processing due to its rigid yet flexible structure. On the other hand - adding additional hand annotations is not a viable option, and for the current task, we must rely on publicly available annotations. UCCA performed the best on the correctness scale but did not explicitly state negation and entity recognition. At the same time, due to annotation tooling, it is possible to implement the required layers if deemed necessary. Interpret resulted in the highest expressiveness, but also it was the only parser that crashed on one sentence in a corpus: \emph{What states border states that border states that border states that border Texas.}.

Author recommends using the tools in ensemble while constructing the knowledge extraction pipeline - considering the strengths and limitations or each individual framework: UDS to simplify the sentence structure, AMR for deep semantic parsing and UD for syntactic annotations when necessary. 