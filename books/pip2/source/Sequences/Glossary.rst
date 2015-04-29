Summary
=======

This chapter introduced a lot of new ideas.  The following summary 
may prove helpful in remembering what you learned.

.. glossary::

    indexing (``[]``)
        Access a single character in a string using its position (starting from
        0), or a single item from a list.  Example: ``'This'[2]`` evaluates to ``'i'``.
        Example: ``[10, 20, 'hello'][1]`` evaluates to ``20``

    length function (``len``)
        Returns the number of characters in a string or a list.  Example:
        ``len('happy')`` evaluates to ``5``.
        Example: ``len([10, 20 'hello'])`` evaluates to 3

    slicing (``[:]``)
        A *slice* is a substring of a string or a list. Example: ``'bananas and
        cream'[3:6]`` evaluates to ``ana`` (so does ``'bananas and
        cream'[1:4]``).
        Example: ``[10, 20, 'hello', 'goodbye'][1:3]`` evaluates to ``[20, 'hello']``

    string comparison (``>, <, >=, <=, ==, !=``)
        The six common comparision operators work with strings, evaluating according to
        `lexigraphical order
        <http://en.wikipedia.org/wiki/Lexicographic_order>`__.  Examples:
        ``'apple' < 'banana'`` evaluates to ``True``.  ``'Zeta' < 'Appricot'``
        evaluates to ``False``.  ``'Zebra' <= 'aardvark'`` evaluates to
        ``True`` because all upper case letters precede lower case letters.

    in and not in operator (``in``, ``not in``)
        The ``in`` operator tests whether one string is contained
        inside another string.  Examples: ``'heck' in "I'll be checking for
        you."`` evaluates to ``True``.  ``'cheese' in "I'll be checking for
        you."`` evaluates to ``False``.

    collection data type
        A data type in which the values are made up of components, or elements,
        that are themselves values.

    dot notation
        Use of the **dot operator**, ``.``, to access methods and attributes of an object.

    immutable
        A compound data type whose elements can not be assigned new values.

    index
        A variable or value used to select a member of an ordered collection, such as
        a character from a string, or an element from a list.

    whitespace
        Any of the characters that move the cursor without printing visible
        characters. The constant ``string.whitespace`` contains all the
        white-space characters.
        
    aliases
        Multiple variables that contain references to the same object.

    clone
        To create a new object that has the same value as an existing object.
        Copying a reference to an object creates an alias but doesn't clone the
        object.

    delimiter
        A character or string used to indicate where a string should be split.

    element
        One of the values in a list (or other sequence). The bracket operator
        selects elements of a list.

    mutable data type
        A data type in which the elements can be modified. All mutable types
        are compound types. Lists are mutable data types; strings are not.

    object
        A thing to which a variable can refer.
