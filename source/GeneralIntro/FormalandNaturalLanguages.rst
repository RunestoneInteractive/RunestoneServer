..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Formal and Natural Languages
----------------------------

**Natural languages** are the languages that people speak, such as English,
Spanish, and French. They were not designed by people (although people try to
impose some order on them); they evolved naturally.

**Formal languages** are languages that are designed by people for specific
applications. For example, the notation that mathematicians use is a formal
language that is particularly good at denoting relationships among numbers and
symbols. Chemists use a formal language to represent the chemical structure of
molecules. And most importantly:

    *Programming languages are formal languages that have been designed to
    express computations.*

Formal languages tend to have strict rules about syntax. For example, ``3+3=6``
is a syntactically correct mathematical statement, but ``3=+6$`` is not.
H\ :sub:`2`\ O is a syntactically correct chemical name, but :sub:`2`\ Zz is
not.

Syntax rules come in two flavors, pertaining to **tokens** and structure.
Tokens are the basic elements of the language, such as words, numbers, and
chemical elements. One of the problems with ``3=+6$`` is that ``$`` is not a
legal token in mathematics (at least as far as we know). Similarly,
:sub:`2`\ Zz is not legal because there is no element with the abbreviation
``Zz``.

The second type of syntax rule pertains to the **structure** of a statement---
that is, the way the tokens are arranged. The statement ``3=+6$`` is
structurally illegal because you can't place a plus sign immediately after an
equal sign.  Similarly, molecular formulas have to have subscripts after the
element name, not before.

When you read a sentence in English or a statement in a formal language, you
have to figure out what the structure of the sentence is (although in a natural
language you do this subconsciously). This process is called **parsing**.

For example, when you hear the sentence, "The other shoe fell", you understand
that the other shoe is the subject and fell is the verb.  Once you have parsed
a sentence, you can figure out what it means, or the **semantics** of the sentence.
Assuming that you know what a shoe is and what it means to fall, you will
understand the general implication of this sentence.

Although formal and natural languages have many features in common --- tokens,
structure, syntax, and semantics --- there are many differences:

.. glossary::

    ambiguity
        Natural languages are full of ambiguity, which people deal with by
        using contextual clues and other information. Formal languages are
        designed to be nearly or completely unambiguous, which means that any
        statement has exactly one meaning, regardless of context.

    redundancy
        In order to make up for ambiguity and reduce misunderstandings, natural
        languages employ lots of redundancy. As a result, they are often
        verbose.  Formal languages are less redundant and more concise.

    literalness
        Formal languages mean exactly what they say.  On the other hand,
        natural languages are full of idiom and metaphor. If someone says, "The
        other shoe fell", there is probably no shoe and nothing falling.

        .. tip::

            You'll need to find the original joke to understand the idiomatic
            meaning of the other shoe falling.  *Yahoo! Answers* thinks it
            knows!

People who grow up speaking a natural language---everyone---often have a hard
time adjusting to formal languages. In some ways, the difference between formal
and natural language is like the difference between poetry and prose, but more
so:

.. glossary::

    poetry
        Words are used for their sounds as well as for their meaning, and the
        whole poem together creates an effect or emotional response. Ambiguity
        is not only common but often deliberate.

    prose
        The literal meaning of words is more important, and the structure
        contributes more meaning. Prose is more amenable to analysis than
        poetry but still often ambiguous.

    program
        The meaning of a computer program is unambiguous and literal, and can
        be understood entirely by analysis of the tokens and structure.

Here are some suggestions for reading programs (and other formal languages).
First, remember that formal languages are much more dense than natural
languages, so it takes longer to read them. Also, the structure is very
important, so it is usually not a good idea to read from top to bottom, left to
right. Instead, learn to parse the program in your head, identifying the tokens
and interpreting the structure.  Finally, the details matter. Little things
like spelling errors and bad punctuation, which you can get away with in
natural languages, can make a big difference in a formal language.

**Check your understanding**

.. mchoicemf:: question1_10_1
   :answer_a: natural languages can be parsed while formal languages cannot.
   :answer_b: ambiguity, redundancy, and literalness.
   :answer_c: there are no differences between natural and formal languages.
   :answer_d: tokens, structure, syntax, and semantics.
   :correct: b
   :feedback_a: Actually both languages can be parsed (determining the structure of the sentence), but formal languages can be parsed more easily in software.
   :feedback_b: All of these can be present in natural languages, but cannot exist in formal languages.
   :feedback_c: There are several differences between the two but they are also similar.
   :feedback_d: These are the similarities between the two.

   The differences between natural and formal languages include:

.. mchoicemf:: question1_10_2
   :answer_a: True
   :answer_b: False
   :correct: b
   :feedback_a: It usually takes longer to read a program because the structure is as important as the content and must be interpreted in smaller pieces for understanding.
   :feedback_b: It usually takes longer to read a program because the structure is as important as the content and must be interpreted in smaller pieces for understanding.

   True or False:  Reading a program is like reading other kinds of text.


