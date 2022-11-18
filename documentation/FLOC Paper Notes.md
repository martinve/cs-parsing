FLOC Paper Notes

### Paper: How much of UCCA can be predicted from AMR? https://arxiv.org/pdf/2207.12174.pdf

"While powerful in its ability to abstract away from a surface form, there are number of phenomena that AMR does not cover: tense, plurality, definitevess, scope"

**Bos 2020**: Extensions for dealing with scope AMR. "[Separating Argument Structure from Logical Structure in AMR](https://aclanthology.org/2020.dmr-1.2.pdf)"
**Donatelli 2018**: proposition to augment AMR with tense and aspect.

**Koller 2019:** Framework classification. https://aclanthology.org/P19-4002.pdf


Types of encodings:
- vector based semantic encodings: continous, sense and distributed.
- classical encodings: hierarchically structured and discrete.

Types of graphs
- Tree
- Non tree: properties are (reentrancies, multiple roots, and semantically vacuous surface tokens).


Definition of semantic parsing: **Kate and Wong 2010**

Reusable intermediate layer that is application and domain independent that captures in suitably abstract form relevant constraints that the linguistic signal imposes on interpretation (Koller)

**Kuhlmann 2016 ** Towards a Catalogue of Linguistic
Graph Banks. https://aclanthology.org/J16-4009.pdf provides an unified view of linguistic graph banks.

Traditionally trees> where every node is reachable from distinguished root node by exactly one directed path.

Extended versions:

* Sagae, Kenji and Junichi Tsujii. 2008. Shift-reduce dependency DAG parsing
* Das, Dipanjan, Nathan Schneider, Desai Chen, and Noah A. Smith. 2010. Probabilistic frame-semantic parsing. I
* Jones, Goldwater, and Johnson 2013
* Flanigan et al. 2014
* Martins and Almeida 2014;

CCD: Combinatory Categorical Grammar word-word dependencies. *bilexical*

SDP: Semantic Dependency Parsing targets from SemEval 2014 and 2015.  *bilexical*



**bilexical dependencies** where graph nodes correspond to surface lexical units

**semantic networks (conceptual graphs)** - nodes represent concepts and there needs not to be explicit mapping to surface linguistic forms.  



### Paper



###### Towards a Catalogue of Linguistic Graph Banks. Marco Kuhlmann and Stephan Oepen. 2016. https://aclanthology.org/J16-4009.pdf



###### A Tale of Three Parsers: Towards Diagnostic Evaluation for Meaning Representation Parsing. 2020. https://aclanthology.org/2020.lrec-1.234.pdf

When considering dimensions in which the accuracy of a
meaning representation graph may be analysed, the queries
can be separated into two broad categories: (1) structural
factors, stemming from formal graph theory—the aspects
of a tree or graph such as root node labels, and edge lengths;
and (2) linguistic factors—related to underlying characteristics of the input strings, such as part-of-speech tags, and
sentence length.

Attributes to consider are:
- sentence length
- dependency distance
- distance to root
- type of dependency relation
- parts of speech
- node related dimensions


*sentence meaning*

contrastive - The contrastive studies initiated by McDonald and Nivre
(2007) and McDonald and Nivre (2011) have been influential in comparing the performance of two core types of
approaches to syntactic dependency parsing, i.e. different
families of parsing approaches.

diagnostic

Sources:

* McDonald & Nivre. 2007. Characterizing the Errors of Data-Driven Dependency Parsing Models. https://aclanthology.org/D07-1013.pdf. Summary:  contrastive error analysis of graph-based vs. transitionbased syntactic dependency parsers. Though the best graph- and transition-based syntactic dependency parsers at the time achieved very similar accuracy on average, they had quite distinctive error profiles. ransition-based parsers were more accurate on short
dependencies thanks to a richer feature model, but degraded
more because of error propagation in greedy decoding.
Conversely, graph-based parsers showed a more graceful
degradation thanks to global optimization and exact decoding, but had a disadvantage for local structures because of
a more restricted feature model. More recently, Kulmizev
et al. (2019) replicated this analysis for neural graph-based
and transition-based parsers and showed that, although the
distinct error profiles are still discernible, the differences
are now much smaller and are further reduced by the use of
deep contextualized word embeddings (Peters et al., 2018;
Devlin et al., 2019).


* McDonald & Nivre. 2013. Analyzing and Integrating Dependency Parsers. https://aclanthology.org/J11-1007.pdf






###### MRP 2019: Cross-Framework Meaning Representation Parsing. 2019. Oepen et. al, https://aclanthology.org/K19-2001.pdf

Meaning Representation Parsing (MRP) across frameworks (Oepen et al., 2019). For the first time, this task combined formally and linguistically different approaches to meaning representation in graph form in a uniform
training and evaluation setup - to advance learning from complementary knowledge sources (e.g. via parameter sharing)

The training and evaluation data for the task comprised five distinct approaches which all encode core predicate–argument structure, among
other things—to the representation of sentence meaning in the form of directed graphs, packaged in a uniform abstract structure and serialization.


###### McDonald & Nivre

Defined querying dimensions

Parsing models
* **graph based** - model is parametrized over dependency subraphs and learns those parameters to globally score correct graphs above incorrect ones. Inference is also global, in that system attempts to find highest scoring graph among the set of all graphs. 
* **transition based** - model is parametrized over transitions from one state to antother in abstract state-machine. Parameters are learned using standadrd classification techniques that learn to predict one classification from a set of permissible transitions given a state history.  Inference is local,in that systems start in a fixed initial state and greedily construct the graph by taking the highest
scoring transitions at each state entered until a termination condition is met.

_Classifier stacking_ is the method by allowing the outputs of one model to define features for the other. 



#### Definitions and Explanations

Predicate-argument structure. https://www.departments.bucknell.edu/linguistics/lectures/10lect09.html, see also http://www.departments.bucknell.edu/linguistics/ln110.html#one

