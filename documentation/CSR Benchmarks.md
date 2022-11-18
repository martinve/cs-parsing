# CSR Benchmarks

Exploring and Analyzing Machine Commonsense Benchmarks. H. Santos, M. Gordon et al. 2012 https://arxiv.org/abs/2012.11634

COM2SENSE: A Commonsense Reasoning Benchmark with Complementary Sentences. S. Singh, N. Wen et al. 2021. https://arxiv.org/abs/2106.00969



## AMR Specific

SEMBLEU: A Robust Metric for AMR Parsing Evaluation. https://medium.com/analytics-vidhya/understanding-the-sembleu-and-bleu-metric-2e8a01cedcb3

SMATCH Score





## Other

Evaluating Semantic Parsing against a Simple Web-based Question Answering Model. A. Talmor, M. Geva, J. Berant 2017. https://arxiv.org/pdf/1707.04412.pdf

A Statistical Semantic Parser that Integrates Syntax and Semantics. R Ge, R. Mooney 2005 https://www.cs.utexas.edu/~ml/papers/parsing-conll-05.pdf

CoNLL Shared Task on Cross-Framework Meaning Representation Parsing. https://www.aclweb.org/portal/content/conll-shared-task-cross-framework-meaning-representation-parsing





Building a Semantic Parser Overnight. https://nlp.stanford.edu/pubs/wang-berant-liang-acl2015.pdf



# 





# Choosing a benchmark

Smatch score (https://amr.isi.edu/smatch-13.pdf) is an evaluation metric for comparing two whole-sentence AMR graphs.  An AMR graph can be viewed as conjunction of logical triples. Smatch score computes the maximum match number of triples among all possible variable mappings and gets the F-score, precision, and recall.

General Language Understanding Evaluation (GLUE) (https://arxiv.org/abs/1804.07461) and SuperGLUE (https://arxiv.org/pdf/1905.00537.pdf) are an model-agnostic benchmarks for natural language understanding. not tailored to specific domain or dataset. The datasets contain both word knowledge and common sense and logical entailments: (https://super.gluebenchmark.com/diagnostics/) 

Bilingual Evaluation Understudy (BLEU) is a metric for evaluating machine translated text from one natural language to another. SEMBLEU (https://arxiv.org/1905.10726) is an extension of BLEU metric

Complementary Commonsense (COM2SENSE() (https://arxiv.org/abs/2106.00969) is a commonsense reasoning benchmark of 4000 natural language sentence pairs that can be either true or false. The dataset is constructed across both knowledge domains (physical, social, temporal) and resasoning scenarios (causal, comparative)

CommonsenseQA (https://arxiv.org/abs/1811.00937) is a multiple choice multiple-choice question answering dataset that requires commonsense knowledge based on ConceptNet relations

Also: COPA, SWAG, Winograd.

Vt. gold standardid https://www.ruslang.ru/doc/kashkin/2014/06.pdf

