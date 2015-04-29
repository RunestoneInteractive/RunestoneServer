..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Sorting
-------

Sorting is the process of placing elements from a collection in some
kind of order. For example, a list of words could be sorted
alphabetically or by length. A list of cities could be sorted by
population, by area, or by zip code. We have already seen a number of
algorithms that were able to benefit from having a sorted list (recall
the final anagram example and the binary search).

There are many, many sorting algorithms that have been developed and
analyzed. This suggests that sorting is an important area of study in
computer science. Sorting a large number of items can take a substantial
amount of computing resources. Like searching, the efficiency of a
sorting algorithm is related to the number of items being processed. For
small collections, a complex sorting method may be more trouble than it
is worth. The overhead may be too high. On the other hand, for larger
collections, we want to take advantage of as many improvements as
possible. In this section we will discuss several sorting techniques and
compare them with respect to their running time.

Before getting into specific algorithms, we should think about the
operations that can be used to analyze a sorting process. First, it will
be necessary to compare two values to see which is smaller (or larger).
In order to sort a collection, it will be necessary to have some
systematic way to compare values to see if they are out of order. The
total number of comparisons will be the most common way to measure a
sort procedure. Second, when values are not in the correct position with
respect to one another, it may be necessary to exchange them. This
exchange is a costly operation and the total number of exchanges will
also be important for evaluating the overall efficiency of the
algorithm.

