#!/usr/bin/env python3

# The proper logic converter parts of nlpsolver, used by nlptologic
#
# Licence:
#  MIT licence https://opensource.org/licenses/MIT
#
# Authors and copyright:
#  tanel.tammet@gmail.com

# ==== standard libraries ====

from re import S
import sys
import math

from numpy import number

# ==== import other source files ====

# configuration and other globals are in nlpglobals.py
from nlpglobals import *

# small utilities are in nlputils.py
from nlputils import *

from nlpsolver import server_parse

# ======= globals used and changed during work ===

constant_nr = 0  # new constants created add a numeric suffic, incremented
definition_nr = 0  # new definitions created add a numeric suffic, incremented

# ===== tips for development =====

"""
Cats and dogs are animals.

  and [[and cat dog] be animal]

  cat(X) => animal(X)
  dog(X) => animal(X)

Cats and dogs are animals and pets.

  and [[and cat dog] be [and animal pet]

  cat(X) => animal(X)
  dog(X) => animal(X) 
  cat(X) => pet(X)
  dog(X) => pet(X) 

Cats and dogs are wild or domestic.

  and [[and cat dog] be [or wild domestic]

  cat(X) => (wild(X) v domestic(X))
  dog(X) => (wild(X) v domestic(X))  

Cats or dogs are nice

  and [[or cat dog] be nice]

  (cat(X) => nice(X)) v (dog(X) => nice(X))

Cats or (dogs and rabbits) are nice

  and [[or cat [and dog rabbit]] be nice]

  (cat(X) => nice(X)) v 
     ( (dog(X) => nice(X)) and (rabbit(X) => nice(X)) )

  a v (b & c) = (a v b) & (a v c)

  (cat(X) => nice(X)) v (dog(X) => nice(X))  
  &
  (cat(X) => nice(X)) v (rabbit(X) => nice(X)) 

  cat(X) & dog(Y)  => nice(X) | nice(Y)
  ...

Big yellow cats are strong.

  [[props [and big yellow] cat] be strong]

  big(X) & yellow(X) & cat(X) => strong(X)

Some big yellow cats are strong.

  [quant [some] [[props [and big yellow] cat] be strong]]

   big(c) & yellow(c) & cat(c) & strong(c)

Big or yellow cats are strong.

  [[props [or big yellow] cat] be strong]

  (big(X) & cat(X) => strong(X)) v (yellow(X) & cat(X) => strong(X))


Big yellow cats are not strong.

  [[props [and big yellow] cat] -be strong]  

   big(X) & yellow(X) & cat(X) => -strong(X)

Not true that (all) big yellow cats are strong:

  not (forall (X) (big(X) & yellow(X) & cat(X) => strong(X)))

  big(c) & yellow(c) & cat(c) & -strong(c)

Not true that (some) big yellow cats are strong:

  not (exists (X) (big(X) & yellow(X) & cat(X) & strong(X)))

  -big(X) v -yellow(X) v -cat(X) v -strong(X)
  equivalently 
  big(X) & yellow(X) & cat(X) => -strong
  
"""


# =============== proper logic building ================================


def build_proper_logic(ctxt, sentence, tree):
    # debug_print("tree",tree)
    if not tree: return tree
    if type(tree) == str: return tree
    if type(tree) == dict: return tree
    if type(tree[0]) == dict: return tree
    if tree[0] in ["logic"]:
        return tree[2]
    elif tree[0] in ["ref"]:
        ref = tree[1][1:]
        # debug_print("ref",ref)
        sys.exit(0)
    elif tree[0] in ["and", "or", "unless", "nor", "xor"]:
        res = [tree[0]]
        for el in tree[1:]:
            tmp = build_proper_logic(ctxt, sentence, el)
            res.append(tmp)
        return res
    elif tree[0] == "if":
        tmp1 = build_proper_logic(ctxt, sentence, tree[1])
        tmp2 = build_proper_logic(ctxt, sentence, tree[2])
        res = [tmp1, "=>", tmp2]
        return res
    elif tree[0] == "unless":
        tmp1 = build_proper_logic(ctxt, sentence, tree[1])
        tmp2 = build_proper_logic(ctxt, sentence, tree[2])
        res = [["not", tmp1], "=>", tmp2]
        return res
    else:
        return tree


def build_subsentence_proper_logic(ctxt, sentence, tree, iscondition=False):
    # debug_print("build_subsentence_proper_logic tree",tree)

    if not tree: return tree
    if type(tree) == str: return tree
    if type(tree) == dict: return tree
    if type(tree[0]) == dict: return tree
    if tree[0] in ["svo", "sv"]:

        sentlogic = build_single_subsentence_proper_logic(ctxt, sentence, tree, iscondition)
        return sentlogic

    elif tree[0] in ["ref"]:
        ref = tree[1][1:]
        # debug_print("ref",ref)
        sys.exit(0)
    elif tree[0] in ["if"]:
        res = [tree[0]]
        tmp1 = build_subsentence_proper_logic(ctxt, sentence, tree[1], True)
        tmp2 = build_subsentence_proper_logic(ctxt, sentence, tree[2], False)
        # debug_print("tmp1",tmp1)
        # debug_print("tmp2",tmp2)

        tmp1 = remove_logic_annotations(tmp1)
        tmp1 = flatten_and_or_logic_term(tmp1)
        tmp2 = remove_logic_annotations(tmp2)
        tmp2 = flatten_and_or_logic_term(tmp2)

        tmp1vars = collect_free_vars(tmp1)
        tmp2vars = collect_free_vars(tmp2)
        if tmp2vars and not tmp1vars and tmp1 and tmp1[0] in ["exists", "forall"]:
            # "if some red elephant is big, it is nice"
            # not tmp1vars in order to not fire for "if person has a nice car, he is happy"
            tmp1 = tmp1[2]
        elif not (tmp2vars) and tmp1vars:
            # "if rabbits are big, elephants are strong"
            # "if person has a nice car, he is happy"
            tmp1 = ["forall", tmp1vars, tmp1]

        # debug_print("tmp1 +",tmp1)
        # debug_print("tmp2 +",tmp2)

        # sys.exit(0)

        res = [tmp1, "=>", tmp2]
        # debug_print("res",res)
        vars = collect_free_vars(res)
        # debug_print("vars",vars)
        if vars:
            res = ["forall", vars, res]
        res = ["logic", tree, res]
        return res
    elif tree[0] in ["and", "or", "if", "unless", "nor", "xor"]:
        res = [tree[0]]
        for el in tree[1:]:
            tmp = build_subsentence_proper_logic(ctxt, sentence, el, iscondition)
            res.append(tmp)
        res = flatten_and_or_logic_term(res)
        return res
    else:
        # res=flatten_and_or_logic_term(res)
        return tree


"""
Elephants with a long tail have a trunk

all x exists y   (Elephant x & (exists tail y & long y & have x y)) => have x z
"""

"""
"if an animal has a trunk, it is a nice animal."

 all x [  (animal(x) & has(trunk,x)) => nice(x) ]

         all x [animal(x) => has(trunk,x)]

         exists x [animal(x) & -has(trunk,x)]

logic:
  [['forall', ['?:X'], [['isa', 'animal', '?:X'], '=>', ['rel2', 'have', '?:X', ['of', 'trunk', '?:X']]]], '=>', ['and', ['prop', 'nice', '?:X'], ['isa', 'animal', '?:X']]]

"""


def build_single_subsentence_proper_logic(ctxt, sentence, tree, iscondition=False):
    root = tree[1][0]
    svo = tree[1][1:]
    # debug_print("svo",svo)
    subjpart = svo[0]
    verbpart = svo[1]
    objpart = svo[2]

    """
  verb=subjpart[1]
  if type(subjpart)==dict:
    subj=subjpart
  else:
    subj=subjpart[-1]  
  if type(subjpart)==dict:
    subj=subjpart
  else:
    subj=subjpart[-1]  
  """

    # debug_print("verbpart",verbpart)
    verb = verbpart

    # debug_print("build_single_subsentence_proper_logic objpart",objpart)

    object_data = make_object_data(ctxt, sentence, objpart)
    # debug_print("object_data",object_data)

    object = get_thing(objpart)
    objspecialvar = None
    objconst = None
    objispronoun = False
    if pronoun(ctxt, object):
        tmp = resolve_pronoun(ctxt, object, tree)
        object = tmp[1]
        objrepr = tmp[0]
        objispronoun = True
    elif object and type(object) == dict and variable_shaped_lemma(object["lemma"]):
        svar = "?:" + object["lemma"]
        objspecialvar = svar
        objrepr = objspecialvar
    elif object and type(object) == dict and object["upos"] in ["PROPN"]:
        objconst = find_make_constant(ctxt, sentence, object)
        objrepr = objconst
    else:
        ovar = "?:X" + str(ctxt["varnum"])
        ctxt["varnum"] += 1
        objrepr = ovar
    object_quant = get_word_quant(ctxt, sentence, object)
    object_det = get_word_det(ctxt, sentence, object)
    # debug_print("object_quant",object_quant)
    # debug_print("object_det",object_det)

    # debug_print("build_single_subsentence_proper_logic subjpart",subjpart)

    subject = get_thing(subjpart)
    subjspecialvar = None
    subjconst = None
    subjispronoun = False
    if pronoun(ctxt, subject):
        tmp = resolve_pronoun(ctxt, subject, tree)
        subject = tmp[1]
        subjrepr = tmp[0]
        subjispronoun = True
    elif subject and variable_shaped_lemma(subject["lemma"]):
        svar = "?:" + subject["lemma"]
        subjspecialvar = svar
        subjrepr = subjspecialvar
    elif subject and subject["upos"] in ["PROPN"]:
        subjconst = find_make_constant(ctxt, sentence, subject)
        subjrepr = subjconst
    else:
        # svar="?:X"
        svar = "?:X" + str(ctxt["varnum"])
        ctxt["varnum"] += 1
        subjrepr = svar
    subject_quant = get_word_quant(ctxt, sentence, subject)
    subject_det = get_word_det(ctxt, sentence, subject)
    # debug_print("subject_quant",subject_quant)
    # debug_print("subject_det",subject_det)

    # - - - - - be - - - - - -

    if verb["lemma"] in ["be"]:
        var = subjrepr  # "?:X"
        objrepr = subjrepr
        if subjspecialvar: var = subjspecialvar
        subj_logic = make_subj_logic(ctxt, sentence, var, subjpart, verbpart, objpart)
        if (subject_quant and subject_quant["lemma"] in ["no"] and
                (not (object_quant) or not (object_quant["lemma"] in ["no"]))):
            reversepolarity = True
        else:
            reversepolarity = False
        # reversepolarity=False
        # debug_print("reversepolarity",reversepolarity)
        obj_logic = make_obj_data_logic(ctxt, sentence, var, subjpart, verbpart, objpart, object_data, False, False,
                                        reversepolarity)
        if not (subjispronoun) and subject_quant and subject_quant["lemma"] in ["some", "exist"]:
            quantifier = "exists"
            logic = ["logic", tree, [quantifier, [var], ["and", subj_logic, obj_logic]]]
        elif not (subjispronoun) and subject_quant and subject_quant["lemma"] in ["all", "every"]:
            quantifier = "forall"
            logic = ["logic", tree, [quantifier, [var], ["and", subj_logic, obj_logic]]]
        elif iscondition and is_var(subjrepr):
            logic = ["logic", tree, ["and", subj_logic, obj_logic]]
        elif subjispronoun:
            logic = ["logic", tree, obj_logic]
        elif subjspecialvar:
            logic = ["logic", tree, [subj_logic, "=>", obj_logic]]
        elif not (subjispronoun) and subject_quant and subject_quant["lemma"] in ["some", "exist"]:
            quantifier = "exists"
            logic = ["logic", tree, [quantifier, [var], ["and", subj_logic, obj_logic]]]
        elif subjconst:
            obj_logic = make_obj_logic(ctxt, sentence, subjconst, subjpart, verbpart, objpart, False, False,
                                       reversepolarity)
            logic = ["logic", tree, obj_logic]
        else:
            quantifier = "forall"
            logic = ["logic", tree, [quantifier, [var], [subj_logic, "=>", obj_logic]]]

    # - - - - - have - - - - -

    elif ((verb["lemma"] in ["have"]) and
          object and
          not (object["upos"] in ["PROPN"])):
        # debug_print("has case")
        svar = subjrepr
        subj_logic = make_subj_logic(ctxt, sentence, svar, subjpart, verbpart, objpart)
        positive1 = get_word_polarity(ctxt, sentence, verb)
        # debug_print("object_data1",object_data)
        if not (type(object_data) == list and object_data[0] in ["and", "or", "nor", "xor"]):
            object_data = ["single", object_data]
        # debug_print("object_data2",object_data)
        # debug_print("subject_quant",subject_quant)
        if subject_quant and subject_quant["lemma"] in ["some", "exists"]:
            subject_quantifier = "exists"
        else:
            subject_quantifier = "forall"
        object_quantifier = "forall"
        ovar = svar
        if type(object_data) == list and object_data[0] in ["single", "and", "or", "nor", "xor"]:
            mainop = object_data[0]
            res = [mainop]
            for thisobject in object_data[1:]:
                objpart = thisobject["objpart"]
                # debug_print("objpart",objpart)
                thing = get_thing(objpart)
                # debug_print("thing",thing)
                ovar = "?:O"
                obj_logic = make_obj_logic(ctxt, sentence, ovar, subjpart, verbpart, objpart, False, False, False,
                                           False)
                # debug_print("obj_logic",obj_logic)
                positive = positive1
                if mainop in ["nor"]:
                    positive = not positive
                if type(obj_logic) == list:
                    if obj_logic[0] == "not":
                        positive = False
                        obj_logic = obj_logic[1]
                    elif obj_logic[0] == "-isa":
                        positive = False
                        obj_logic = ["isa"] + obj_logic[1:]
                    elif type(obj_logic[-1]) == list and obj_logic[-1][0] == "-isa":
                        positive = False
                        obj_logic = obj_logic[:-1] + [["isa"] + obj_logic[-1][1:]]
                if type(obj_logic) == list and obj_logic[0] == "and":
                    if len(obj_logic) == 3:
                        pure_obj_logic = obj_logic[1]
                    else:
                        pure_obj_logic = obj_logic[:-1]
                elif type(obj_logic) == list:
                    pure_obj_logic = []
                # debug_print("pure_obj_logic",pure_obj_logic)
                # debug_print("positive1",positive)
                if positive:
                    thisvar = make_have_term(ctxt, thing, svar)
                    obj_logic = logic_replace_el(obj_logic, ovar, thisvar)
                    pure_obj_logic = logic_replace_el(pure_obj_logic, ovar, thisvar)
                else:
                    thisvar = ovar
                relation = make_atom_2(verb, positive, svar, thisvar)
                # debug_print("relation",relation)
                op = "=>"
                if positive:
                    if pure_obj_logic:
                        conjecture = ["and", pure_obj_logic, relation]
                    else:
                        conjecture = relation
                    thislogic = [subj_logic, op, conjecture]
                    thislogic = [subject_quantifier, [svar], thislogic]
                else:
                    if obj_logic:
                        precondition = ["and", subj_logic, obj_logic]
                    else:
                        precondition = subj_logic
                    conjecture = relation
                    thislogic = [precondition, op, conjecture]
                    thislogic = [subject_quantifier, [svar], [object_quantifier, [thisvar], thislogic]]
                if mainop in ["nor"]:
                    thislogic = ["not", thislogic]
                res.append(thislogic)

        if res and res[0] == "single":
            res = res[1]
            # debug_print("res1",res)
        res = flatten_and_or_logic_term(res)
        # debug_print("res2",res)
        logic = simplify_quantors(res)
        return logic

        # sys.exit(0)

        # obj_logic=make_obj_logic(ctxt,sentence,ovar,subjpart,verbpart,objpart)
        object_props = get_props_list(objpart)
        obj_props_logic = make_property_logic(ctxt, ovar, object_props)

        conjecture = make_atom_2(verb, positive, svar, ovar)
        obj_logic = obj_props_logic
        full_obj_logic = make_obj_logic(ctxt, sentence, ovar, subjpart, verbpart, objpart, False, False, False)
        #
        # if obj_props_logic:
        #  premiss=["and",subj_logic,obj_logic]
        # else:
        #  premiss=subj_logic
        debug_print("iscondition", iscondition)
        debug_print("subjispronoun", subjispronoun)
        debug_print("subjrepr", subjrepr)
        debug_print("subject", subject)
        debug_print("full_obj_logic", full_obj_logic)
        sys.exit(0)

        # if iscondition and is_var(subjrepr):
        #  # "if a person has a car, he is happy"
        #  debug_print("cp")
        #  logic=["logic",tree,["and",subj_logic,full_obj_logic]]
        #  debug_print("logic",logic)
        logicbuilt = False
        if (subject and subjspecialvar):
            op = "=>"
            log1 = [subj_logic, op, conjecture]



        elif (subject and (not subjspecialvar) and
              not iscondition and
              ((subject["upos"] in ["PROPN"]) or
               (subject_det and subject_det["lemma"] in ["some"]))):
            # "John has a car"
            debug_print("checkpoint1")
            quantifier = "exists"
            op = "&"
            if not positive:
                # log1=[quantifier,[svar,ovar],[["and",subj_logic,full_obj_logic],"=>",conjecture]]
                # log1=["not",[quantifier,[svar],[subj_logic,op,conjecture]]]
                full_obj_logic = make_obj_logic(ctxt, sentence, ovar, subjpart, verbpart, objpart, False, True, False)
                log1 = ["forall", [svar, ovar], [["and", subj_logic, full_obj_logic], "=>", conjecture]]
                # debug_print("log1",log1)
            else:
                log1 = [quantifier, [svar], ["and", subj_logic, conjecture]]
            debug_print("checkpoint2 log1", log1)
        elif (subject and (not subjspecialvar) and
              not iscondition and subjispronoun):
            # "..., it has a bike"
            debug_print("checkpoint1e")
            # sys.exit(0)
            quantifier = "exists"
            op = "&"
            if not positive:
                # log1=[quantifier,[svar,ovar],[["and",subj_logic,full_obj_logic],"=>",conjecture]]
                # log1=["not",[quantifier,[svar],[subj_logic,op,conjecture]]]
                full_obj_logic = make_obj_logic(ctxt, sentence, ovar, subjpart, verbpart, objpart, False, True, False)
                log1 = ["forall", [ovar], [full_obj_logic, "=>", conjecture]]
                # logic=log1
                logic = ["logic", tree, log1]
                # debug_print("log1",log1)
            else:
                # log1=conjecture
                logic = ["logic", tree, full_obj_logic]
            # debug_print("checkpoint2e log1",log1)

            debug_print("checkpoint2e logic", logic)
            logicbuilt = True
        elif (subject and (not subjspecialvar) and
              iscondition and
              (not (subject["upos"] in ["PROPN"]) or
               (subject_quant and subject_quant["lemma"] in ["some", "exists"]))):
            #   "if a person has a nice car, he is happy"
            debug_print("checkpoint1a")
            quantifier = "exists"
            op = "&"
            if not positive:
                # log1=[quantifier,[svar,ovar],[["and",subj_logic,full_obj_logic],"=>",conjecture]]
                # log1=["not",[quantifier,[svar],[subj_logic,op,conjecture]]]
                full_obj_logic = make_obj_logic(ctxt, sentence, ovar, subjpart, verbpart, objpart, False, True, False)
                log1 = ["forall", [svar, ovar], [["and", subj_logic, full_obj_logic], "=>", conjecture]]
                # debug_print("log1",log1)
            else:
                log1 = [quantifier, [ovar], ["and", subj_logic, conjecture, full_obj_logic]]
            debug_print("checkpoint2a log1", log1)
            debug_print("checkpoint2a full_obj_logic", full_obj_logic)
            # combinedlog=
            logic = ["logic", tree, log1]
            debug_print("checkpoint2a logic", logic)
            logicbuilt = True
        elif subjconst:
            debug_print("checkpoint subjconst")
            op = "=>"
            log1 = [subj_logic, op, conjecture]
        else:
            # "Elephants have a trunk
            # "Elephants do not have a trunk "
            debug_print("checkpoint1b positive", positive)
            debug_print("checkpoint1b full_obj_logic", full_obj_logic)
            debug_print("checkpoint1b obj_logic", obj_logic)
            debug_print("checkpoint1b conjecture", conjecture)
            quantifier = "forall"
            op = "=>"
            if not positive:
                # "Elephants do not have a trunk "
                log1 = [quantifier, [svar, ovar], [["and", subj_logic, full_obj_logic], "=>", conjecture]]
                # debug_print("log1",log1)
            else:
                # "Elephants have a trunk
                log1 = [quantifier, [svar], [subj_logic, "=>", conjecture]]

                # log1=[quantifier,[svar],[subj_logic,op,conjecture]]
        # if iscondition and is_var(subjrepr):
        #  None #logic=["logic",tree,logic]
        if not logicbuilt:
            debug_print("obj_props_logic", obj_props_logic)
            if obj_props_logic and positive != False:
                if op == "=>":
                    log2 = [quantifier, [svar], [subj_logic, "=>", obj_logic]]
                else:
                    log2 = [quantifier, [svar], ["and", subj_logic, obj_logic]]
                logic = ["logic", tree, ["and", log1, log2]]
            else:
                logic = ["logic", tree, log1]

    # - - - - not be or have  - - - - -

    else:
        # svar="?:X"
        if subjspecialvar:
            svar = subjspecialvar
        elif subjconst:
            svar = subjconst
        subj_logic = make_subj_logic(ctxt, sentence, svar, subjpart, verbpart, objpart, subjspecialvar)
        # ovar="?:Y"
        if objspecialvar:
            ovar = objspecialvar
        elif objconst:
            ovar = objconst

        obj_logic = make_obj_logic(ctxt, sentence, ovar, subjpart, verbpart, objpart, objspecialvar, False, False,
                                   False)
        verb = verbpart
        positive1 = get_word_polarity(ctxt, sentence, verb)
        conjecture = make_atom_2(verb, positive1, svar, ovar)
        if (subject and subjspecialvar):
            squantifier = "forall"
            oquantifier = "forall"
            op = "=>"
            logic = ["logic", tree,
                     [["and", subj_logic, obj_logic], op, conjecture]]
        elif (subject and
              ((subject["upos"] in ["PROPN"]) or
               (subject_det and subject_det["lemma"] in ["some"]))):
            squantifier = "exists"
            oquantifier = "forall"
            # op="&"
            logic = ["logic", tree,
                     [squantifier, [svar],
                      [oquantifier, [ovar], ["and", subj_logic, obj_logic, conjecture]]]]
        else:
            squantifier = "forall"
            oquantifier = "forall"
            op = "=>"
            logic = ["logic", tree,
                     [squantifier, [svar],
                      [oquantifier, [ovar], [["and", subj_logic, obj_logic], op, conjecture]]]]

    ctxt["passed_words"].append([subjrepr, subject, "subject"])
    ctxt["passed_words"].append([objrepr, object, "object"])

    # debug_print("pre-flatten logic",logic)
    logic = flatten_and_or_logic_term(logic)
    logic = simplify_quantors(logic)
    return logic


def get_deco_obj_data_logic_thing(logic):
    if not logic: return logic
    if type(logic) == dict: return logic
    if logic[0] == "logic": return logic[1]
    lastel = logic[-1]
    res = get_deco_obj_data_logic_thing(lastel)
    return res


def make_object_data(ctxt, sentence, objpart):
    if not objpart: return objpart
    if type(objpart) == dict:
        data = make_object_data_single(ctxt, sentence, objpart)
        return data
    elif objpart[0] in ["or", "nor", "xor", "and"]:
        op = objpart[0]
        res = [op]
        for el in objpart[1:]:
            data = make_object_data_single(ctxt, sentence, el)
            res.append(data)
        return res
    else:
        data = make_object_data_single(ctxt, sentence, objpart)
        return data


def make_object_data_single(ctxt, sentence, objpart):
    object = get_thing(objpart)
    objspecialvar = None
    objconst = None
    objispronoun = False
    if pronoun(ctxt, object):
        tmp = resolve_pronoun(ctxt, object, tree)
        object = tmp[1]
        objrepr = tmp[0]
        objispronoun = True
    elif object and type(object) == dict and variable_shaped_lemma(object["lemma"]):
        svar = "?:" + object["lemma"]
        objspecialvar = svar
        objrepr = objspecialvar
    elif object and type(object) == dict and object["upos"] in ["PROPN"]:
        objconst = find_make_constant(ctxt, sentence, object)
        objrepr = objconst
    else:
        ovar = "?:X" + str(ctxt["varnum"])
        ctxt["varnum"] += 1
        objrepr = ovar
    object_quant = get_word_quant(ctxt, sentence, object)
    object_det = get_word_det(ctxt, sentence, object)
    # debug_print("object_quant",object_quant)
    # debug_print("object_det",object_det)
    res = {"object": object, "objrepr": objrepr, "objspecialvar": objspecialvar,
           "quant": object_quant, "det": object_det,
           "objpart": objpart}
    return res


def pronoun(ctxt, word):
    if not word: return False
    if type(word) != dict: return False
    if word["upos"] in ["PRON"]:
        debug_print("pronoun", word)
        return True
    return False


def resolve_pronoun(ctxt, word, tree):
    debug_print("resolve pronoun word", word)
    locals = ctxt["passed_words"]
    debug_print("resolve pronoun locals", locals)
    l = len(locals)
    i = 0
    while i < l:
        local = locals[i]
        localword = local[1]
        if localword["upos"] in ["NOUN", "PROPN"]:
            return local
        i += 1
    i = 0
    while i < l:
        local = locals[i]
        localword = local[1]
        # if localword["upos"] in ["NOUN","PROPN"]:
        return local
        i += 1
    return None


def make_subj_logic(ctxt, sentence, var, subjpart, verbpart, objpart, specialvar=False):
    andlist = []
    positive = True
    thing = get_thing(subjpart)
    propslist = make_props_list_of_thingpart(ctxt, subjpart)
    for prop in propslist:
        # debug_print("prop",prop)
        if complex_property(prop):
            proplogic = make_complex_property_atom(ctxt, sentence, var, prop, thing)
            if proplogic:
                andlist.append(proplogic)
            continue
        if variable_shaped_word(prop):
            continue
            # positive=True
        positive = get_word_polarity(ctxt, sentence, prop)
        proplogic = make_atom_1(prop, positive, var)
        if proplogic:
            andlist.append(proplogic)
    # debug_print("andlist",andlist)
    if not variable_shaped_word(thing):
        # positive=get_word_polarity(ctxt,sentence,thing)
        thingatom = make_atom_1(thing, True, var)
        if thingatom:
            andlist.append(thingatom)
    if not andlist:
        return True
    elif len(andlist) == 1:
        andlist = andlist[0]
    else:
        andlist = ["and"] + andlist
    # if positive==False:
    #  andlist=["not",andlist]
    return andlist


def make_obj_logic(ctxt, sentence, var, subjpart, verbpart, objpart, specialvar=False, forcepositive=False,
                   reversepolarity=False, deco=False):
    # debug_print("make_obj_logic objpart",objpart)
    # debug_print("make_obj_logic var",var)
    # debug_print("make_obj_logic reversepolarity",reversepolarity)
    andlist = []
    listop = "and"
    if objpart and type(objpart) == list and objpart[0] in ["and", "or", "nor", "xor"]:  # "or","nor","xor"]
        listop = objpart[0]
        andlist = [listop]
        for el in objpart[1:]:
            tmp = make_obj_logic(ctxt, sentence, var, subjpart, verbpart, el, specialvar, forcepositive,
                                 reversepolarity, deco)
            andlist.append(tmp)
        if reversepolarity:
            andlist = ["not", andlist]
        return andlist
    else:
        listop = "and"
    positive = True
    globalnegative = False
    thing = get_thing(objpart)
    # debug_print("make_obj_logic thing",thing)
    # debug_print("make_obj_logic objpart",objpart)
    propslist = make_obj_props_list_of_thingpart(ctxt, objpart)
    # debug_print("make_obj_logic propslist",propslist)
    propcount = 0
    if var and type(var) == list and var[0] == "make_have_term":
        thisvar = make_have_term(ctxt, thing, var[1])
    else:
        thisvar = var
    for prop in propslist:
        propcount += 1
        if complex_property(prop):
            proplogic = make_complex_property_atom(ctxt, sentence, thisvar, prop, thing)
            if proplogic:
                andlist.append(proplogic)
            continue
        if variable_shaped_word(prop):
            continue
        positive = get_word_polarity(ctxt, sentence, prop)
        # debug_print("prop",prop)
        # debug_print("positive",positive)
        if listop in ["and", "or", "nor", "xor"] and propcount == 1 and not positive:
            globalnegative = True
            positive = True
        if reversepolarity: positive = not positive
        # debug_print("prop1",prop)
        # debug_print("positive1",positive)

        # if type(prop)==list and prop[0] in ["and"]:
        #
        # else:

        proplogic = make_atom_1(prop, positive, thisvar)
        if proplogic:
            if deco:
                andlist.append(["logic", prop, proplogic])
            else:
                andlist.append(proplogic)
    # debug_print("make_obj_logic andlist1",andlist)
    if not variable_shaped_word(thing):
        if not forcepositive:
            positive = get_word_polarity(ctxt, sentence, thing)
            # debug_print("thing",thing)
            # debug_print("positive",positive)
            if reversepolarity: positive = not positive
            if not positive and thing["deprel"] != "conj":
                globalnegative = True
                positive = True
            # debug_print("thing2",thing)
            # debug_print("positive2",positive)
        # thingatom=make_atom_1(thing,positive,var)
        thingatom = make_atom_1(thing, positive, thisvar)
        if thingatom:
            if deco:
                andlist.append(["logic", thing, thingatom])
            else:
                andlist.append(thingatom)
                # debug_print("make_obj_logic andlist2",andlist)
    if not andlist:
        return True
    elif len(andlist) == 1:
        andlist = andlist[0]
    else:
        andlist = [listop] + andlist
    if globalnegative and not deco:
        # debug_print("globalnegative",globalnegative)
        andlist = ["not", andlist]
    return andlist


def make_obj_data_logic(ctxt, sentence, var, subjpart, verbpart, objpart, object_data, specialvar=False,
                        forcepositive=False, reversepolarity=False, deco=False):
    # deco=False
    # debug_print("make_obj_data_logic object_data",object_data)
    # debug_print("make_obj_data_logic subjpart",subjpart)
    # print(object_data)
    # debug_print("make_obj_data_logic reversepolarity",reversepolarity)
    if not object_data: return object_data
    if type(objpart) == dict and not ("objpart" in object_data):
        # debug_print("make_obj_data_logic cp1")
        res = make_obj_logic(ctxt, sentence, var, subjpart, verbpart, object_data, specialvar, forcepositive, False,
                             deco)
    elif type(object_data) == dict and "objpart" in object_data:
        # debug_print("make_obj_data_logic cp2")
        res = make_obj_logic(ctxt, sentence, var, subjpart, verbpart, object_data["objpart"], specialvar, forcepositive,
                             False, deco)
    # elif type(objpart)==list and not("objpart" in object_data):
    #  debug_print("make_obj_data_logic cp1")
    #  res=make_obj_logic(ctxt,sentence,var,subjpart,verbpart,object_data,specialvar,forcepositive,reversepolarity)
    elif type(object_data) == list:
        # debug_print("make_obj_data_logic cp3")
        op = object_data[0]
        res = [op]
        for el in object_data[1:]:
            tmp = make_obj_data_logic(ctxt, sentence, var, subjpart, verbpart, el["objpart"], el, specialvar,
                                      forcepositive, False, deco)
            res.append(tmp)
    # debug_print("make_obj_data_logic reversepolarity",reversepolarity)
    if reversepolarity:
        res = ["not", res]
        # debug_print("make_obj_data_logic res",res)
    return res


def complex_property(prop):
    # debug_print("complex_property prop",prop)
    if not prop: return False
    if type(prop) == list and prop[0] in ["svo", "sv", "ref"]:
        return True
    else:
        return False


def make_complex_property_atom(ctxt, sentence, var, prop, thing):
    # debug_print("make_complex_property_atom prop",prop)
    # debug_print("make_complex_property_atom thing",thing)
    # res=["$daa",1]
    var = {"lemma": "X10", "upos": "PROPN", "id": 1000, "head": 2000}
    replaced = replace_property_objects(ctxt, sentence, prop, thing, var)
    # debug_print("make_complex_property_atom replaced",replaced)
    prelogic = build_single_subsentence_proper_logic(ctxt, sentence, replaced, iscondition=False)
    # debug_print("make_complex_property_atom prelogic",prelogic)
    purelogic = prelogic[2]
    purevar = "?:X10"
    defn = make_definition(ctxt, purelogic, [purevar])
    # debug_print("make_complex_property_atom defn",defn)
    if type(defn) == list and defn[0] == "forall":
        defatom = defn[2][0]
    else:
        defatom = defn[0]
    # debug_print("make_complex_property_atom defatom",defatom)
    # debug_print("make_complex_property_atom ctxt1",ctxt)
    if "sentence_defs" in ctxt:
        ctxt["sentence_defs"].append(defn)
    else:
        ctxt["sentence_defs"] = [defn]
    # debug_print("make_complex_property_atom ctxt2", ctxt)
    # sys.exit(0)
    return defatom


def make_property_logic(ctxt, var, propslist):
    if not propslist: return []
    andlist = []
    for prop in propslist:
        if variable_shaped_lemma(prop["lemma"]):
            continue
        positive = True
        proplogic = make_atom_1(prop, positive, var)
        if proplogic:
            andlist.append(proplogic)
    if len(andlist) == 1:
        andlist = andlist[0]
    else:
        andlist = ["and"] + andlist
    return andlist


def get_thing(thingdata):
    if type(thingdata) == dict:
        return thingdata
    elif (type(thingdata) == list and type(thingdata[-1]) == list and
          thingdata[-1][0] in ["props"]):
        return thingdata[-1][-1]
    else:
        return thingdata[-1]


def get_props_list(thingdata):
    if type(thingdata) == dict:
        return []
    props = thingdata[1]
    if type(props) == list:
        return props[1:]
    else:
        return [props]


def make_props_list_of_thingpart(ctxt, subjpart):
    # debug_print("make_props_list_of_thingpart subjpart",subjpart)
    if type(subjpart) != list:
        return []
    if type(subjpart[1]) == dict:
        return [subjpart[1]]
    elif complex_property(subjpart[1]):
        return [subjpart[1]]
    else:
        return subjpart[1][1:]


def make_obj_props_list_of_thingpart(ctxt, objpart):
    # debug_print("make_obj_props_list_of_thingpart objpart",objpart)
    if type(objpart) != list:
        return []
    elif objpart[0] in ["and", "seq", "or", "nor", "xor"]:
        tmp = objpart[1:-1]
        if type(objpart[-1]) == list and objpart[-1][0] in ["props"]:
            tmp = tmp + objpart[-1][1:-1]
        # debug_print("tmp",tmp)
        return tmp
    elif type(objpart[1]) == dict:
        return [objpart[1]]
    elif complex_property(objpart[1]):
        return [objpart[1]]
    else:
        return objpart[1][1:]


def make_atom_1(thing, positive, var):
    # debug_print("make_atom_1 thing",thing)
    lemma = thing["lemma"]

    if thing["upos"] in ["PROPN"]:
        pred = "hasname"
        if dummyname_constant(None, var):
            return None
    elif thing["upos"] in ["NOUN"]:
        pred = "isa"
    else:
        pred = "prop"
    if not positive:
        pred = "-" + pred
    res = [pred, lemma, var]
    return res


def make_atom_2(thing, positive, var1, var2):
    lemma = thing["lemma"]
    if positive:
        pred = "rel2"
    else:
        pred = "-rel2"
    res = [pred, lemma, var1, var2]
    return res


def make_have_term(ctxt, object, var):
    lemma = object["lemma"]
    fun = "fun"
    res = ["of", lemma, var]
    return res


def get_word_quant(ctxt, sentence, word):
    if not word: return None
    if not (type(word) == dict): return None
    children = get_children(sentence, word)
    res1 = None
    if children:
        for child in children:
            if child["deprel"] == "det" and child["upos"] == "DET":
                if child["lemma"] in ["a", "an", "the"]:
                    return None
                else:
                    return child
        for child in children:
            if not (child["deprel"] in ["amod"]): continue
            # debug_print("child in get_word_quant",child)
            childchildren = get_children(sentence, child)
            for childchild in childchildren:
                # debug_print("childchild in get_word_quant",childchild)
                if childchild["deprel"] == "advmod" and childchild["upos"] == "ADV":
                    if childchild["lemma"] in ["some", "most", "few"]:
                        return childchild
    parent = get_parent(sentence, word)
    if parent:
        res2 = get_word_quant(ctxt, sentence, parent)
        if res2:
            return res2
    return None


def get_word_det(ctxt, sentence, word):
    if not word: return None
    if not (type(word) == dict): return None
    children = get_children(sentence, word)
    res1 = None
    if children:
        for child in children:
            if child["deprel"] == "det" and child["upos"] == "DET":
                if child["lemma"] in ["a", "an", "the"]:
                    return child
                else:
                    return None
                return child
    parent = get_parent(sentence, word)
    if parent:
        res2 = get_word_det(ctxt, sentence, parent)
        if res2:
            return res2
    return None


def get_word_polarity(ctxt, sentence, word):
    if not word: return True
    if not (type(word) == dict): return True
    children = get_children(sentence, word)
    res1 = None
    if children:
        for child in children:
            if child["deprel"] == "advmod" and child["upos"] in ["PART", "ADV"]:
                if child["lemma"] in ["not", "no", "never"]:
                    return False
            elif child["deprel"] == "det" and child["upos"] in ["DET"]:
                if child["lemma"] in ["not", "no", "never"]:
                    return False
                    # parent=get_parent(sentence,word)
    # if parent:
    #  res2=get_word_det(ctxt,sentence,parent)
    #  if res2:
    #    return res2
    return True


def build_proper_logic(ctxt, sentence, tree):
    # debug_print("tree",tree)
    if not tree: return tree
    if type(tree) == str: return tree
    if type(tree) == dict: return tree
    if type(tree[0]) == dict: return tree
    if tree[0] in ["logic"]:
        return tree[2]
    elif tree[0] in ["ref"]:
        ref = tree[1][1:]
        # debug_print("ref",ref)
        sys.exit(0)
    elif tree[0] in ["and", "or", "unless", "nor", "xor"]:
        res = [tree[0]]
        for el in tree[1:]:
            tmp = build_proper_logic(ctxt, sentence, el)
            res.append(tmp)
        return res
    elif tree[0] == "if":
        tmp1 = build_proper_logic(ctxt, sentence, tree[1])
        tmp2 = build_proper_logic(ctxt, sentence, tree[2])
        res = [tmp1, "=>", tmp2]
        return res
    elif tree[0] == "unless":
        tmp1 = build_proper_logic(ctxt, sentence, tree[1])
        tmp2 = build_proper_logic(ctxt, sentence, tree[2])
        res = [["not", tmp1], "=>", tmp2]
        return res
    else:
        return tree

        # ======================== old part =========================

        # ===== parse specific parts of a sentence ======

        """
     general noun case:

    Elephants have a small tail. (unknown number of tails)
    [["isa","elephant","?:X"],"=>",["and",["rel2","have","?:X",["tail_n_of","?:N","?:X"]], ["property","small",["tail_n_of","?:N","?:X"]]]

    Elephants have one small tail. (single small tail_object)
    [["isa","elephant","?:X"],"=>",["and",["rel2","have","?:X",["tail_n_of",1,"?:X"]], ["property","small",["tail_n_of",1,"?:X"]]]
    
    [["isa","elephant","?:X"],"=>",["and",["tail_n_of","?:A","?:X"],"=",["tail_n_of","?:B","?:X"]]
    or also/better
    [["and",["isa","elephant","?:X"],["rel2","have","?:X",["tail_n_of","?:N","?:X"]]],"=>",["?:N",<,2]]

    generally

    [["?:X","!=","?:Y"],"=>",[["..._n_of","?:X","?:Z],"!=",["..._n_of","?:Y","?:Z]]

    Elephants have legs. 
    [["isa","elephant","?:X"],"=>",["rel2","have","?:X",["leg_n_of",1,"?:X"]]]
    [["isa","elephant","?:X"],"=>",["rel2","have","?:X",["leg_n_of",2,"?:X"]]]
    [["leg_n_of",1,"?:X"],"!=",["leg_n_of",2,"?:X"]]

    Elephants have a left eye and a right eye. 
    [["isa","elephant","?:X"],"=>",["and",["rel2","have","?:X",["eye_n_of",1,"?:X"]],["property","left",["eye_n_of",1,"?:X"]]]
    [["isa","elephant","?:X"],"=>",["and",["rel2","have","?:X",["eye_n_of",2,"?:X"]],["property","right",["eye_n_of",2,"?:X"]]]

    ["eye_n_of",1,

    [["isa","elephant","?:X"],"=>",["rel2","have","?:X",["eye_n_of",2,"?:X"]]]
    [["leg_1_of","?:X"],"!=",["leg_2_of","?:X"]]


    Elephants have strong legs. 
    [["isa","elephant","?:X"],"=>",["rel2","have","?:X",["leg_n_of",1,"?:X"]]]
    [["isa","elephant","?:X"],"=>",["rel2","have","?:X",["leg_n_of",2,"?:X"]]]

    [["and",["isa","elephant","?:X"],["isa","leg","?:Y"]],
      "=>",
      ["and",["rel2","have","?:X","?:Y"],,["property","strong","?:Y]]]

     number case:

     men have two hands
 
    [["isa","man","?:X"],"=>",["and",["rel2","have","?:X",["hand_1_of","?:X"]]
    [["isa","man","?:X"],"=>",["and",["rel2","have","?:X",["hand_2_of","?:X"]]
    [["hand_1_of","?:X"],"!=",["hand_2_of","?:X"]]

    [["isa","man","?:X"],"=>",["and",["rel2","have","?:X",["hand_n_of",1,"?:X"]]
    [["isa","man","?:X"],"=>",["and",["rel2","have","?:X",["hand_n_of",2,"?:X"]]
    
    [["and",["isa","man","?:Z"],["?:X","!=","?:Y"]],"=>",[["hand_n_of","?:X","?:Z"],"!=",["hand_n_of","?:Y","?:Z"]]

    [["and",["isa","man","?:X"],["hand_n_of",1,"?:X"]"=>",
    ["hand_n_of","?:X","?:Z"]

    
     negation case:

     John does not have a car.
     [["isa","car","?:X"],"=>",['-rel2', 'have', 'c0_John', '?:X']]
     John does not have a red car.
     [["and",["isa","car","?:X"],["property","red","?:X"]],"=>",['-rel2', 'have', 'c0_John', '?:X']]
     John does not have a car or a bike.
     [["or",["isa","car","?:X"],["isa","bike","?:X"]],"=>",['-rel2', 'have', 'c0_John', '?:X']]
     John and Mike do not have a car.
     [["isa","car","?:X"],"=>",['-rel2', 'have', 'c0_John', '?:X']]
     [["isa","car","?:X"],"=>",['-rel2', 'have', 'c1_Mike', '?:X']]
     John or Mike does not have a car.
     ["or"
       ["isa","car","?:X"],"=>",['-rel2', 'have', 'c0_John', '?:X']]
       ["isa","car","?:Y"],"=>",['-rel2', 'have', 'c1_Mike', '?:Y']]
      ] 
      or rather
      ["isa","car","?:X"],"=>",["or" ['-rel2', 'have', 'c0_John', '?:X'],['-rel2', 'have', 'c1_Mike', '?:Y']]


    Question ideas:

   

    What does John have?
    
    ["rel2", "have", "c0_John", "?:X"]

    Does John have a trunk? Which/What trunk John has?    
       
       John has trunk:
      
       ["rel2", "have", "c0_John", "?:X"] , "&", ["isa","trunk", "?:X"]

       Having a trunk:

       ["have_trunk","?:Y"], "<=", [["rel2", "have", "?:Y", "?:X"] , "&", ["isa","trunk", "?:X"]]

       John has a trunk?

       ["have_trunk","c0_John"],  

    
    ??? ["rel2", "have", "c0_John", ["nof_trunk","?:N","c0_John"]], "&", ["isa","trunk",["nof_trunk","?:N","c0_John"]]

    Who has a trunk?
    
    assume idef1(Y) <= ["rel2", "have", "?:Y", "?:X"], "&",  ["isa","trunk","?:X"]
    ask idef1(Y)

    ["have_trunk","?:Y"],  

    Some elephants have a trunk?

    assume idef(X) <= ['isa', 'elephant', '?:X'], "&", ['isa', 'trunk', '?:Y'], "&", ['rel2', 'have', '?:X', '?:Y']
    ask idef1(X)

    All elephants have a trunk?

    assume ['isa', 'trunk', ['nof_trunk', '?:N', '?:X']]
    assume ['isa', 'elephant', 'dummy1']
    ask ['rel2', 'have', 'dummy1', ['nof_trunk', '?:N', 'dummy1']]]

    ask idef1()

    Does elephant have a trunk?

    assume: ["isa","elephant","dummy1"]
    ask: ["have_trunk","dummy1"]  or
          ["rel2", "have", "dummy1", "?:X"], "&",  ["isa","trunk","?:X"]

      ["elephant_have_trunk","?:Y"], "<=>", [["isa","elephant","?:Y"], "=>", ["have_trunk","?:Y"]],  
    
     ["isa","elephant","?:Y"], "=>", ["and, ["rel2", "have", "?:Y", "?:X"], ["isa","trunk","?:X"]]

    """


def oldis_definition(clause):
    if not clause: return False
    if type(clause) != list: return False
    if type(clause[0]) != list: return False
    defsymb = clause[0][0]
    if not (defsymb.startswith(definition_prefix)): return False
    return True


# Add all additional adjectives and nouns to the main property:
# "Elephants are big and grey animals" : mainword is "big"

def filter_propertywords(ctxt, sentence, mainpropword):
    res = []
    # debug_print("filter_propertywords mainpropword",mainpropword)
    for word in get_children(sentence, mainpropword):
        # debug_print("word1",word)
        # big and (grey)
        if (word["deprel"] == "amod" or
                (word["deprel"] == "conj" and word["upos"] in ["NOUN", "PROPN", "ADJ", "PRON"])):
            # debug_print("word2",word)
            # if word["upos"] in ["PRON"]:
            #  word=find_pronoun_replacement(ctxt,sentence,word,objects)
            res.append(word)
            childwords = get_children(sentence, word)
            # debug_print("childwords2",childwords)
            for childword in childwords:
                if childword["deprel"] == "conj" and childword["upos"] in ["NOUN", "PROPN", "ADJ", "PRON"]:
                    # word has itself children conjuncted with and/or
                    subres = filter_propertywords(ctxt, sentence, childword)
                    # debug_print("word3",word)
                    # debug_print("subres",subres)
                    if subres:
                        res = res + subres
        elif word["deprel"] == "nummod":
            res.append(word)
    return res


# ====== question handling special components ==================


def is_question_sentence(sentence):
    # debug_print("is_question_sentence sentence",sentence)
    end_punct = sentence[-1]
    if (end_punct and end_punct["lemma"] == "?"):
        # debug_print("is_question_sentence result",True)
        return True
    else:
        return False

    root = get_root(sentence)
    # debug_print("root",root)

    subjword = get_word_by_keyval(get_children(sentence, root), "deprel", "nsubj")
    end_punct = sentence[-1]
    # debug_print("end_punct",end_punct)
    if (end_punct and end_punct["lemma"] == "?" and
            (root['upos'] == "PRON" and root['lemma'] in ["who", "what"])):
        return True
    if (end_punct and end_punct["lemma"] == "?" and
            (subjword and subjword['upos'] == "PRON" and subjword['lemma'] in ["who", "what"])):
        return True
    if (end_punct and end_punct["lemma"] == "?" and
            root['upos'] == "VERB"):
        return True
    return False


def prepare_question_sentence(sentence):
    root = get_root(sentence)
    subjword = get_word_by_keyval(get_children(sentence, root), "deprel", "nsubj")
    end_punct = sentence[-1]
    if (end_punct and end_punct["lemma"] == "?" and
            (root['upos'] == "PRON" and root['lemma'] in ["who", "what"])):
        debug_print("====== original question sentence ==========\n")
        debug_print_sentence_tree(sentence)
        text = make_text_from_doc(sentence)
        newtext = replace_text_word(text, root['text'], dummy_name)
        debug_print("replacement text for question:", newtext)
        data = server_parse(newtext)
        sentence = data["doc"][0]
        # debug_print("segetntence with a dummy name for question",sentence)
    elif (end_punct and end_punct["lemma"] == "?" and
          (subjword and subjword['upos'] == "PRON" and subjword['lemma'] in ["who", "what"])):
        debug_print("====== original question sentence ==========\n")
        debug_print_sentence_tree(sentence)
        text = make_text_from_doc(sentence)
        newtext = replace_text_word(text, subjword['text'], dummy_name)
        debug_print("replacement text for question:", newtext)
        data = server_parse(newtext)
        sentence = data["doc"][0]
    return sentence


def make_question_from_logic(ctxt, logic, isnegative, constant=False, keepvars=[]):
    # debug_print("make_question_from logic input clauses",logic)
    # debug_print("make_question_from logic constant",logic)
    clauseres = []
    questionres = []

    dummies = collect_dummy_constants(ctxt, logic, [])
    # debug_print("res",dummies)
    varmap = {}
    vars = []
    i = 1
    for dummy in dummies:
        var = "?:Q" + str(i)
        varmap[dummy] = var
        vars.append(var)
        i += 1
    # debug_print("varmap",varmap)
    replaced = logic_replace_el_map(logic, varmap)
    # debug_print("replaced",replaced)
    defn = make_definition(ctxt, replaced, vars)
    defn = simplify_quantors(defn)
    # debug_print("defn",defn)
    return defn


def replace_dummies_with_vars(ctxt, logic):
    dummies = collect_dummy_constants(ctxt, logic, [])
    # debug_print("res",dummies)
    varmap = {}
    vars = []
    i = 1
    for dummy in dummies:
        var = "?:Q" + str(i)
        varmap[dummy] = var
        vars.append(var)
        i += 1
    # debug_print("varmap",varmap)
    replaced = logic_replace_el_map(logic, varmap)
    # debug_print("replaced",replaced)
    return replaced


def suitable_question_logic(ctxt, logic):
    # debug_print("suitable_question_logic logic",logic)
    if not logic: return False
    if type(logic) != list: return False
    head = logic[0]
    if type(head) != list and not logic_connective(head):
        return True
    for el in logic:
        if not el: return False
        if logic_connective(el) and not el in ["and", "&"]:
            return False
        if type(el) == list and logic_connective(el[0]):
            return False
        if type(el) == list and len(el) > 2 and logic_connective(el[1]):
            return False
    return True


def logic_connective(x):
    if type(x) == str and (x in ["and", "or", "not", "&", "|", "<=", "=>", "<=>", "exists", "forall"]):
        return True
    else:
        return False


def old_make_question_from_logic(ctxt, clauses, isnegative, constant=False, keepvars=[]):
    debug_print("make_question_from logic input clauses", clauses)
    debug_print("make_question_from logic constant", constant)
    clauseres = []
    questionres = []

    if dummyname_constant(ctxt, constant):
        var = "?:Q"
        keepvars = logic_replace_el(keepvars, constant, var)
        debug_print("keepvars", keepvars)
        clauses = logic_replace_el(clauses, constant, var)
        constant = var
    for clause in clauses:
        if type(clause[0]) == list and definition_prefix in clause[0][0]:
            # debug_print("definition",clause)
            clauseres.append(clause)
        else:
            # make a one-sided definition
            newdef = make_one_sided_definition(ctxt, clause, keepvars)
            debug_print("newdef", newdef)
            clauseres.append(newdef)
            if newdef[0] == "forall":
                defbody = newdef[2]
            else:
                defbody = newdef
            tmpquestion = defbody[-1]
            question = [tmpquestion[0]]
            if not constant: constant = make_skolem_constant()
            question.append(constant)
            for el in tmpquestion[2:]:
                question.append(el)
            if isnegative:
                question = negate_literal(question)
            debug_print("question", question)
    return {"background": clauseres, "question": question}


def collect_dummy_constants(ctxt, term, found=[]):
    if not term: return []
    if type(term) != list: return []
    res = []
    for lel in term:
        if dummyname_constant(ctxt, lel):
            if not (lel in found):
                found.append(lel)
        else:
            res = collect_dummy_constants(ctxt, lel, found)
    return found


def dummyname_constant(ctxt, constant):
    if type(constant) == str and dummy_name in constant:
        if "_" in constant:
            return True
        else:
            return False
    else:
        return False


def make_definition(ctx, clause, keepvars):
    global definition_nr
    vars = keepvars  # collect_logic_list_vars(clause,[])
    pred = definition_prefix + str(definition_nr)
    definition_nr += 1
    # usevars=[]
    # for el in keepvars:
    conseq = [pred] + keepvars  # vars
    premiss = clause
    allvars = []
    for el in vars:
        if el in keepvars:
            allvars.append(el)
    existvars = []
    for el in vars:
        if not (el in allvars):
            existvars.append(el)
    if existvars:
        leftside = premiss  # ["exists",existvars,premiss]
    else:
        leftside = premiss
        # debug_print("leftside",leftside)
    leftside = logic_remove_quantors(leftside, keepvars, ["exists"])
    mainbody = [conseq, "<=>", leftside]
    if allvars:
        res = ["forall", allvars, mainbody]
    else:
        res = mainbody
    # ["forall", allvars, [["exists",existvars, premiss],"<=>",conseq]]
    res = simplify_quantors(res)
    return res


# ====== larger linguistic components =======


def old_find_pronoun_replacement(ctxt, sentence, word, wordconstants, objectid):
    debug_print("find_pronoun_replacement word", word)
    debug_print("wordconstants", wordconstants)
    debug_print("objectid", objectid)
    debug_print("ctxt", ctxt)
    if "objects" in ctxt and ctxt["objects"]:
        l = len(ctxt["objects"])
        i = l - 1
        while i >= 0:
            object = ctxt["objects"][i]
            if word["lemma"] in ["it", "he", "she", "this", "that"]:
                return object[1]
            i = i - 1
    elif "logic" in ctxt and ctxt["logic"] and word["lemma"] in ["they", "these", "it", "he", "she"]:
        loglist = ctxt["logic"]
        loglen = len(loglist)
        i = loglen - 1
        while i >= 0:
            clause = loglist[i]
            debug_print("clause", clause)
            candidate = find_pronoun_candidate_isa(ctxt, clause)
            if candidate:
                debug_print("candidate", candidate)
                return candidate
            i = i - 1
    # return word["lemma"]
    return objectid


def find_pronoun_candidate_isa(ctxt, clause):
    if not clause: return None
    if type(clause[0]) == list:
        for lit in clause:
            if lit and type(lit) == list and type(lit[0]) != list and lit[0] in ["isa", "-isa"]:
                return {"pred": "isa", "prop": lit[1]}
    return None


# ====== linguistic helpers ========

def get_root(sentence):
    return get_word_by_keyval(sentence, "deprel", "root")


def get_word_by_keyval(sentence, key, val):
    if not sentence: return None
    for word in sentence:
        if word[key] == val:
            return word
    return None


def get_children(sentence, parent):
    res = []
    if not parent: return []
    parent_id = parent['id']
    for word in sentence:
        if word['head'] == parent_id:
            if not end_punct_word(word):
                res.append(word)
    return res


def get_parent(sentence, child):
    res = None
    if not child: return None
    head_id = child["head"]
    if head_id == 0: return None
    for word in sentence:
        if word['id'] == head_id:
            if not end_punct_word(word):
                return word
    return None


def end_punct_word(word):
    lemma = word["lemma"]
    if lemma in end_punctuation_lemmas:
        return True
    else:
        return False


def word_has_feat(word, feat, val):
    if not word: return False
    if not ("feats" in word): return False
    tmp = word["feats"]
    if not tmp: return False
    tmplst = tmp.split("|")
    for el in tmplst:
        tmpel = el.split("=")
        if tmpel and tmpel[0] == feat and tmpel[1] == val:
            return True
    return False


def word_has_article(ctxt, sentence, word, deforindef):
    # debug_print("word_has_article word",word)
    if not word: return False
    children = get_children(sentence, word)
    if not children: return False
    for child in children:
        if (child["deprel"] == "det" and
                word_has_feat(child, "PronType", "Art")):  #
            if deforindef == "indefinite":
                if word_has_feat(child, "Definite", "Ind"):
                    return True
            elif deforindef == "definite":
                if word_has_feat(child, "Definite", "Def"):
                    return True
    return False


def word_has_quantor(ctxt, sentence, word, existorforall):
    debug_print("word_has_quantor word ", word)
    debug_print("word_has_quantor existorforall ", existorforall)
    if not word: return False
    children = get_children(sentence, word)
    if not children: return False
    for child in children:
        if (child["deprel"] == "det"):
            if existorforall == "exist":
                if child["lemma"] in ["some"]:
                    return True
            elif existorforall == "forall":
                if child["lemma"] in ["all"]:
                    return True
    return False


def adjective_lemma(s):
    return s.lower()


def passive_verb(ctxt, word):
    if not word: return False
    if word["lemma"] in ["have"]:
        return True
    return False


# === finding an existing object to match a word ===

# Given: Big Mick is a furry red cat. Small Mick is a mouse.
# Determine: It likes cheese / Mick likes cheese / Big Mick likes fish.

# ctxt is {"logic":..., "objects": ...} from previous sentences
# sentence is the ud of the current sentence
# noun is the ud representation of the investigated word in the current sentence
#
# return a constant if a good match is found, None otherwise


def find_make_constant(ctxt, sentence, word, strictness=False):
    # debug_print("find_make_constant ctxt ",ctxt)
    # debug_print("find_make_constant word ",ctxt)
    object = find_existing_object(ctxt, sentence, word)
    if object:
        return object[0]
    else:
        const = make_constant(word)
        if "objects" in ctxt:
            ctxt["objects"].append([const, word, None])
        else:
            ctxt["objects"] = [[const, word, None]]
    return const

    # debug_print("find_make_constants ctxt ",ctxt)
    # debug_print("find_make_constants strictness",strictness)
    res = []
    if not wordlist: return []
    for word in wordlist:
        # debug_print("find_make_constants word",word)
        if not word: continue
        const = find_existing_constant(ctxt, sentence, word)
        if const:
            res.append([word, const])
        elif word["upos"] == "PROPN":
            const = make_constant(word)
            res.append([word, const])
        elif (word["upos"] == "NOUN" and
              (not strictness) and
              word_has_feat(word, "Number", "Sing") and
              (word_has_article(ctxt, sentence, word, "indefinite") or
               word_has_article(ctxt, sentence, word, "definite") or
               word_has_quantor(ctxt, sentence, word, "exist"))):
            const = make_constant(word)
            res.append([word, const])
        elif (word["upos"] == "NOUN" and
              (not strictness) and
              word_has_feat(word, "Number", "Plur") and
              word_has_quantor(ctxt, sentence, word, "exist")):
            const = make_constant(word)
            res.append([word, const])
        elif (word["upos"] == "NOUN" and
              (not strictness) and
              # word_has_feat(word,"Number","Sing") and
              (not word_has_quantor(ctxt, sentence, word, "forall")) and
              word_has_count(ctxt, sentence, word)):
            const = make_constant(word)
            res.append([word, const])
            # debug_print("find_make_constants res",res)
    return res


def find_existing_object(ctxt, sentence, word):
    # debug_print("find_existing_object ctxt",ctxt)
    # debug_print("find_existing_object word",word)
    if not ("objects" in ctxt): return None
    ctxtobjects = ctxt["objects"]
    for object in ctxtobjects:
        if object[1]["lemma"] == word["lemma"]:
            return object
    return None


def word_has_count(ctxt, sentence, word):
    children = get_children(sentence, word)
    for child in children:
        if child["deprel"] == "nummod":
            return True
    return False


# first quick check whether noun could match an object

def old_suitable_word_candidate_object(ctxtlogic, word, object, word_propertylogic):
    # debug_print("!*!*!* suitable_word_candidate_object word",word)
    # debug_print("suitable_word_candidate_object object",object)
    objword = object[0]
    if len(object) > 2:
        object_propertylogic = object[2]
    else:
        object_propertylogic = []
    # debug_print("object_propertylogic",object_propertylogic)
    # debug_print("word_propertylogic",word_propertylogic)

    if not word: return False
    if word["lemma"] == objword["lemma"] and word["upos"] == objword["upos"]:
        for wordprop in word_propertylogic:
            for objectprop in object_propertylogic:
                if wordprop[0] == "count" and objectprop[0] == "count":
                    if type(wordprop[1]) == int and type(objectprop[1]) == int:
                        if wordprop[1] != objectprop[1]:
                            return False
        return True
    else:
        return False


# give a numeric goodness measure for the match
# return 0 if no match at all, return 1 if perfect

def match_word_candidate_object(word, object):
    return 1


# give a numeric goodness measure for the properties:
# return 0 if no match at all, return 1 if perfect
#
def match_word_candidate_object_props(ctxt, wordchildren, objprops):
    # debug_print("************ \nmatch_word_candidate_object wordchildren",wordchildren)
    # debug_print("match_word_candidate_object objprops",objprops)
    # debug_print("match_word_candidate_object ctxt",ctxt)
    return 1


# ====== small linguistic helpers ===============

def process_lemma(lemma):
    if type(lemma) != str:
        return lemma
    else:
        return lemma.lower()

    # ====== logic building and conversion helpers ========


def make_constant(word):
    global constant_nr
    res = constant_prefix + str(constant_nr) + "_" + word["lemma"]
    constant_nr += 1
    return res


def make_skolem_constant():
    global constant_nr
    res = skolem_constant_prefix + str(constant_nr)
    constant_nr += 1
    return res


def make_population_constant(ctxt, atoms):
    # global constant_nr
    res = ""
    l = len(atoms)
    i = 0
    for el in atoms:
        if el[0][0] == "-":
            res = res + "not_" + el[1]
        else:
            res = res + el[1]
        i += 1
        if i < l: res += "_"
    res = "some_" + res  # str(constant_nr)
    # constant_nr+=1
    return res


def make_var(nr):
    res = var_prefix + str(nr)
    return res


def is_negative_literal(lit):
    if type(lit) != list: return False
    if type(lit[0]) != str: return False
    s = lit[0]
    if s[0] == "-":
        return True
    else:
        return False


def negate_literal(lit):
    if type(lit) != list:
        show_error("literal " + str(lit) + " is not a list")
        sys.exit(0)
    if type(lit[0]) != str:
        show_error("predicate of a literal " + str(lit) + " is not a string")
        sys.exit(0)
    s = lit[0]
    if s[0] == "-":
        s = s[1:]
    else:
        s = "-" + s
    return [s] + lit[1:]


def make_term_from_preterm(sentence, preterm, replacements=None):
    if not preterm: return preterm
    if type(preterm) == list:
        res = []
        for el in preterm:
            res.append(make_term_from_preterm(sentence, el, replacements))
        return res
    elif type(preterm) == dict:
        return preterm["lemma"]
    elif type(preterm) == str and replacements:
        for key in replacements:
            if key in preterm:
                return replacements[key]
        return preterm
    else:
        return preterm


def make_question_from_prequestion(sentence, prequestion, question_dummy_name):
    # debug_print("prequestion",prequestion)
    if not prequestion: return prequestion
    replacements = {}
    atom = []
    if question_dummy_name:
        replacements["_" + question_dummy_name] = question_var
    for preterm in prequestion:
        if type(preterm) == dict:
            atom.append(preterm['lemma'])
        else:
            atom.append(make_term_from_preterm(sentence, preterm, replacements))
    question = {"@question": atom}
    return question


def skolemize_clause(clause):
    mapping = {}
    if not clause: return clause
    if not type(clause) == list: return clause
    if type(clause[0]) == str:
        return skolemize_term(clause[0], mapping)
    else:
        res = []
        for literal in clause:
            res.append(skolemize_term(literal, mapping))
        return res


def skolemize_term(term, mapping):
    if not term: return term
    if type(term) == list:
        res = []
        for el in term:
            res.append(skolemize_term(el, mapping))
        return res
    elif type(term) == dict:
        return term
    elif type(term) == str:
        if is_var(term):
            if term in mapping:
                return mapping[term]
            else:
                const = make_skolem_constant()
                mapping[term] = const
                return const
        else:
            return term
    else:
        return term


def make_logic_from_list(op, lst):
    if not lst:
        return False
    if type(lst[0]) != list:
        return lst
    if len(lst) == 1:
        return lst[0]
    return [op] + lst


# =========== the end ==========

"""
"if foxes are red then they are green." -debug

"If elephants are grey then they are big."
[['-isa', 'elephant', '?:X'], ['-property', 'grey', '?:X'], ['property', 'big', '?:X']]

"If John is grey then he is big."
[['-property', 'grey', 'c0_John'], ['property', 'big', 'c0_John']]



"If John is grey then elephants are big."

[['-property', 'grey', 'c0_John'], ['-isa', 'elephant', '?:X'], ['property', 'big', '?:X'], ['$block', ['$', 'elephant'], ['$not', ['property', 'big', '?:X']]]]

not:

[['-property', 'grey', 'c0_John'], [['-isa', 'elephant', 'c0_John'], ['property', 'big', 'c0_John'], ['$block', ['$', 'elephant'], ['$not', ['property', 'big', 'c0_John']]]]]

"""
