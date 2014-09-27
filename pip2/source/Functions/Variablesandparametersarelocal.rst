..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Variables and parameters are local
----------------------------------

An assignment statement in a function creates a **local variable** for the
variable on the left hand side of the assignment operator. It is called local because this variable only
exists inside the function and you cannot use it outside. For example,
consider again the ``square`` function:

.. codelens:: bad_local

    def square(x):
        y = x * x
        return y

    z = square(10)
    print y


If you press the 'last >>' button you will see an error message.
When we try to use ``y`` on line 6 (outside the function) Python looks for a global
variable named ``y`` but does not find one.  This results in the
error: ``Name Error: 'y' is not defined.``

The variable ``y`` only exists while the function is being executed ---
we call this its **lifetime**.
When the execution of the function terminates (returns),
the local variables  are destroyed.  Codelens helps you  visualize this
because the local variables disappear after the function returns.  Go back and step thru the
statements paying particular attention to the variables that are created when the function is called.
Note when they are subsequently destroyed as the function returns.

Formal parameters are also local and act like local variables.
For example, the lifetime of ``x`` begins when ``square`` is
called,
and its lifetime ends when the function completes its execution.

So it is not possible for a function to set some local variable to a
value, complete its execution, and then when it is called again next
time, recover the local variable.  Each call of the function creates
new local variables, and their lifetimes expire when the function returns
to the caller.

