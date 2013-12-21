# Execution Trace Format

This document describes the execution trace format that serves as the
interface between the frontend and backend of Online Python Tutor
(thereafter abbreviated as OPT).

It is a starting point for anyone who wants to create a different
backend (e.g., for another programming language) or a different frontend
(e.g., for visually-impaired students). View it online at:

https://github.com/pgbovine/OnlinePythonTutor/blob/master/v3/docs/opt-trace-format.md

Look at the Git history to see when this document was last updated; the
more time elapsed since that date, the more likely things are
out-of-date.

I'm assuming that you're competent in Python, JSON, command-line-fu, and
Google-fu. Feel free to email philip@pgbovine.net if you have questions.

And please excuse the sloppy writing; I'm not trying to win any style awards here :)


## Trace Overview

Before you continue reading, I suggest for you to first skim the Overview for Developers doc:
https://github.com/pgbovine/OnlinePythonTutor/blob/master/v3/docs/developer-overview.md

Pay particular attention to what `generate_json_trace.py` is and how to run it:
https://github.com/pgbovine/OnlinePythonTutor/blob/master/v3/docs/developer-overview.md#two-quick-tips-for-starters

Let's start with a simple example. Create an `example.py` file with the following contents:
```python
x = 5
y = 10
z = x + y
```

Now run:
```
python generate_json_trace.py example.py
```

and you should see the following output:
```javascript
{
  "code": "x = 5\ny = 10\nz = x + y\n\n", 
  "trace": [
    {
      "ordered_globals": [], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {}, 
      "heap": {}, 
      "line": 1, 
      "event": "step_line"
    }, 
    {
      "ordered_globals": [
        "x"
      ], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {
        "x": 5
      }, 
      "heap": {}, 
      "line": 2, 
      "event": "step_line"
    }, 
    {
      "ordered_globals": [
        "x", 
        "y"
      ], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {
        "y": 10, 
        "x": 5
      }, 
      "heap": {}, 
      "line": 3, 
      "event": "step_line"
    }, 
    {
      "ordered_globals": [
        "x", 
        "y", 
        "z"
      ], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {
        "y": 10, 
        "x": 5, 
        "z": 15
      }, 
      "heap": {}, 
      "line": 3, 
      "event": "return"
    }
  ]
}
```

Recall that when OPT is deployed on a webserver, the backend generates this trace and sends it to the frontend,
where it will be turned into a visualization.

[Click here](http://pythontutor.com/visualize.html#code=x+%3D+5%0Ay+%3D+10%0Az+%3D+x+%2B+y&mode=display&cumulative=false&py=2&curInstr=0)
to see the visualization of this trace (open it in a new window if possible).
Note that the trace object contains *all* of the information required to create this visualization.

The trace is a JSON object with two fields: `code` is the string contents of the code
to be visualized, and `trace` is the actual execution trace, which consists of a list of execution points.

In the above example, `trace` is a list of four elements since there are four execution points.
If you step through the visualization, you'll notice that there are exactly four steps, one for each
element of the `trace` list.
(Sometimes the frontend will filter out some redundant entries in `trace`, but a simplifying assumption
is that `trace.length` is the number of execution steps that the frontend renders.)

Ok, still with me? Let's now dig into what an individual element in `trace` looks like.


## Execution Point Objects

The central type of object in a trace is an "execution point", which represents the state of the computer's (abstract)
memory at a certain point in execution. Recall that a trace is an ordered list of execution points.

The key concept to understand is that the frontend renders an execution point by simply looking at
the contents of the corresponding execution point object, **without consulting any of its neighbors**.

Ok, let's now look at the **four** execution points in our above example in order. The first point
is what the frontend visualizes when it says "Step 1 of 3":

```javascript
    {
      "ordered_globals": [], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {}, 
      "heap": {}, 
      "line": 1, 
      "event": "step_line"
    }
```

This is pretty much what an "empty" execution point object looks like. `line` shows the line number of the
line that is *about to execute*, which is line 1 in this case. And `event` is `step_line`, which indicates
that an ordinary single-line step event is about to occur. `func_name` is the function that's currently
executing: In this case, `<module>` is the faux name for top-level code that's not in any function.
All of the other fields are empty, and if you look at the visualization, nothing is rendered in the "Frames"
or "Objects" panes.

Ok now let's look at the second point, which corresponds to the frontend visualization when it says
"Step 2 of 3":

```javascript
    {
      "ordered_globals": [
        "x"
      ], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {
        "x": 5
      }, 
      "heap": {}, 
      "line": 2, 
      "event": "step_line"
    }
```

Ok note that `line` is now 2, which means that line 2 is *about* to execute (yes, this convention is a bit confusing,
but it's what the bdb debugger gives us). `globals` is now populated with one key-value pair: the global variable
`x` has a value of `5`. That makes sense since we just executed line 1 (from the previous execution point),
which was the code `x = 5`. If you look at the
[visualization at this step](http://pythontutor.com/visualize.html#code=x+%3D+5%0Ay+%3D+10%0Az+%3D+x+%2B+y&mode=display&cumulative=false&py=2&curInstr=1),
you'll see that `x` has been assigned to `5`.

Ok let's keep marching to the next execution point, which is the one that corresponds to "Step 3 of 3"
in the frontend:

```javascript
    {
      "ordered_globals": [
        "x", 
        "y"
      ], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {
        "y": 10, 
        "x": 5
      }, 
      "heap": {}, 
      "line": 3, 
      "event": "step_line"
    }
```

Now `line` is 3, because we're about to execute line 3 (we just executed lines 1 and 2). Notice that there is a
new key-value pair in`globals` showing that `y` has been assigned to `10`. No surprises here, since we just
executed the line `y = 10`.

Ok now this is where I want to talk about `ordered_globals`, which is a list of global variables (i.e.,
keys in `globals`) in the order that the frontend should visualize them. The backend appends variable
names in their order of appearance throughout execution. Why is this list necessary? Because `globals`
is an object whose keys are unsorted, so if you don't also keep an `ordered_globals` sorted list,
then the visualization might end up being jarring. For instance, at one execution point, it might
render `x` and then `y`, and at the next execution point, it might render `y` and then `x`, thereby
causing the visualization to "jitter" unnecessarily. And I've found that it looks aesthetically pleasing
when variables are sorted in their order of appearance as you step forwards through execution.

Still with me? Ok, let's get to the final execution point, which corresponds to the frontend displaying
"Program terminated" ([click here](http://pythontutor.com/visualize.html#code=x+%3D+5%0Ay+%3D+10%0Az+%3D+x+%2B+y&mode=display&cumulative=false&py=2&curInstr=3)
to jump directly there).

```javascript
    {
      "ordered_globals": [
        "x", 
        "y", 
        "z"
      ], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {
        "y": 10, 
        "x": 5, 
        "z": 15
      }, 
      "heap": {}, 
      "line": 3, 
      "event": "return"
    }
```

This time, the event is a `return`, which signifies "returning" from the top-level module code (meaning the program
has terminated). Note that now there is another new variable `z`, which is bound to `15` since `z = x + y` just executed.
Note that, again, `ordered_globals` shows all three variables in their order of appearance.

Ok, that's it for the basic tour. Next let's talk about what happens when the `heap` field isn't empty.


## Heap Objects

The previous example contained only primitive values that JSON could encode directly within the `globals` object.
JSON natively supports numbers, strings, and boolean values (which map well to Python's "primitive" data types).
But what happens when the user's program contains compound
Python data types such as lists, tuples, dicts, sets, etc.?

Create an `example.py` file with the following contents:
```python
x = [1, 2, 3]
y = ('Alice', 'Bob', 'Cindy')
z = {'carrot': 'vegetable', 'mouse': 'animal', 'rock': 'mineral'}
```

You should know how to generate a trace by now. The trace again contains **four** elements since there are
four execution steps (one for the very beginning of execution plus three executed lines).

"Step 1 of 3" is boring since nothing is displayed. Let's jump to "Step 2 of 3"
(<a href="http://pythontutor.com/visualize.html#code=x+%3D+%5B1,+2,+3%5D%0Ay+%3D+('Alice',+'Bob',+'Cindy')%0Az+%3D+%7B'carrot'%3A+'vegetable',+'mouse'%3A+'animal',+'rock'%3A+'mineral'%7D%0A&mode=display&cumulative=false&py=2&curInstr=1">click here</a>)

The visualization now shows `x` pointing to a list containing `[1, 2, 3]`. This is the corresponding execution
point object:

```javascript
    {
      "ordered_globals": [
        "x"
      ], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {
        "x": [
          "REF", 
          1
        ]
      }, 
      "heap": {
        "1": [
          "LIST", 
          1, 
          2, 
          3
        ]
      }, 
      "line": 2, 
      "event": "step_line"
    }
```

Note that in `globals`, `x` now refers to a `["REF", 1]` object, which means a *reference* (pointer) to a heap
object with an ID of 1.

Let's now look at `heap`, which is a mapping of heap object IDs to their contents. The current heap has one
object with an ID of 1. That object is a list of [1, 2, 3], which is encoded in JSON as:

```javascript
["LIST", 1, 2, 3]
```

Let's skip forward to the end of execution ("Program terminated"):
<a href="http://pythontutor.com/visualize.html#code=x+%3D+%5B1,+2,+3%5D%0Ay+%3D+('Alice',+'Bob',+'Cindy')%0Az+%3D+%7B'carrot'%3A+'vegetable',+'mouse'%3A+'animal',+'rock'%3A+'mineral'%7D%0A&mode=display&cumulative=false&py=2&curInstr=3">click here</a>

Now there are three variables -- `x` points to a list, `y` points to a tuple, and `z` points to a dict.
This execution point object is getting kinda big:

```javascript
    {
      "ordered_globals": [
        "x", 
        "y", 
        "z"
      ], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {
        "y": [
          "REF", 
          2
        ], 
        "x": [
          "REF", 
          1
        ], 
        "z": [
          "REF", 
          3
        ]
      }, 
      "heap": {
        "1": [
          "LIST", 
          1, 
          2, 
          3
        ], 
        "2": [
          "TUPLE", 
          "Alice", 
          "Bob", 
          "Cindy"
        ], 
        "3": [
          "DICT", 
          [
            "carrot", 
            "vegetable"
          ], 
          [
            "mouse", 
            "animal"
          ], 
          [
            "rock", 
            "mineral"
          ]
        ]
      }, 
      "line": 3, 
      "event": "return"
    }
```

Note that in `globals`, `x` refers to heap object 1, `y` to heap object 2, and `z` to 3. If you then look at `heap`,
you'll see that objects 1, 2, and 3 map to the corresponding list, tuple, and dict, respectively.

Look at the comments at the top of `pg_encoder.py` to learn the JSON encoding formats for various Python data types:

https://github.com/pgbovine/OnlinePythonTutor/blob/master/v3/pg_encoder.py

The basic idea behind the encoding format is that each compound object is encoded as a JSON list
where the first element is a string "tag" identifying its type (e.g., "LIST", "TUPLE", "DICT").

## Heap-to-Heap References

In the above example, the heap objects contained only primitives (numbers and strings), which can be directly
encoded within those objects' representations in `heap`.

But heap objects can themselves point to other heap objects. Let's look at the following example:

```python
c = (1, (2, None))
d = (1, c)
```

<a href="http://pythontutor.com/visualize.html#code=c+%3D+(1,+(2,+None))%0Ad+%3D+(1,+c)&mode=display&cumulative=false&py=2&curInstr=2">Jump to the end</a> of execution and notice that:

- `c` points to a tuple
- the second element of that tuple points to another tuple
- `d` points to a tuple whose second element points to what `c` points to

Let's look at the execution point object that corresponds to this visualization:

```javascript
    {
      "ordered_globals": [
        "c", 
        "d"
      ], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {
        "c": [
          "REF", 
          1
        ], 
        "d": [
          "REF", 
          3
        ]
      }, 
      "heap": {
        "1": [
          "TUPLE", 
          1, 
          [
            "REF", 
            2
          ]
        ], 
        "2": [
          "TUPLE", 
          2, 
          null
        ], 
        "3": [
          "TUPLE", 
          1, 
          [
            "REF", 
            1
          ]
        ]
      }, 
      "line": 2, 
      "event": "return"
    }
```

What's going on here? Let's start with `globals` again. `c` points to heap object 1 (`["REF", 1]`), and `d` points
to heap object 3 (`["REF", 3]`).

Let's now look at `heap`. Heap object 1 is:

```javascript
["TUPLE", 1, ["REF", 2]]
```

What does this mean? It means that it represents a tuple whose first element is the number `1` and whose
second element is a reference (pointer) to heap object 2.

Ok let's look at heap object 2:

```javascript
["TUPLE", 2, null]
```

which corresponds to the Python tuple object `(2, None)`.

Finally, heap object 3 (which `d` points to) is:

```javascript
["TUPLE", 1, ["REF", 1]]
```

which corresponds to the Python object `(1, c)`.

The ability to put "REF" objects inside of heap objects enables an arbitrary object graph to be
represented in the execution trace.


## Capturing `stdout` Output

The `stdout` field in an execution point object represents the sum total of all output sent to stdout
so far during execution. For example, given this program:

```python
print 1
print "two"
print (3, 4, 5)
```

The complete trace object is:

```javascript
{
  "code": "print 1\nprint \"two\"\nprint (3, 4, 5)\n\n", 
  "trace": [
    {
      "ordered_globals": [], 
      "stdout": "", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {}, 
      "heap": {}, 
      "line": 1, 
      "event": "step_line"
    }, 
    {
      "ordered_globals": [], 
      "stdout": "1\n", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {}, 
      "heap": {}, 
      "line": 2, 
      "event": "step_line"
    }, 
    {
      "ordered_globals": [], 
      "stdout": "1\ntwo\n", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {}, 
      "heap": {}, 
      "line": 3, 
      "event": "step_line"
    }, 
    {
      "ordered_globals": [], 
      "stdout": "1\ntwo\n(3, 4, 5)\n", 
      "func_name": "<module>", 
      "stack_to_render": [], 
      "globals": {}, 
      "heap": {}, 
      "line": 3, 
      "event": "return"
    }
  ]
}
```

By now you should be getting pretty good at reading these objects :)

Let's just focus on the `stdout` field at each execution point. Note that its contents start as an empty string
at the beginning of execution and then grow incrementally as more stuff is printed to stdout at each
subsequent execution point. If we grep for `stdout` in the trace, we see the following progression:

```javascript
      "stdout": "", 
      "stdout": "1\n", 
      "stdout": "1\ntwo\n", 
      "stdout": "1\ntwo\n(3, 4, 5)\n", 
```

This isn't rocket science; but just be aware that `stdout` contains the cumulative contents of the stdout
buffer up to that execution point, not only what's been printed by the most recently executed line.


## Function Stack Frames

So far our example programs contained no function calls. Let's now kick it up a notch and see an example
with function calls:

```python
def foo(x, y, z):
  return bar(x, y)
  
def bar(a, b):
  return baz(a)
  
def baz(c):
  return c
  
result = foo(1, 2, 3)
```

Let's jump straight to <a href="http://pythontutor.com/visualize.html#code=def+foo(x,+y,+z)%3A%0A++return+bar(x,+y)%0A++%0Adef+bar(a,+b)%3A%0A++return+baz(a)%0A++%0Adef+baz(c)%3A%0A++return+c%0A++%0Aresult+%3D+foo(1,+2,+3)%0A&mode=display&cumulative=false&py=2&curInstr=7">Step 8 of 10</a>,
when the program is about to return from the call to `baz`.

Study the visualization for a bit. Note that there are four frames currently on the stack: globals, `foo`, `bar`, and `baz`.
Each frame consists of a name and a mapping between constituent variable names and values. There is a special
variable called `Return value` (stored in the trace as `__return__`),
which represents the value that `baz` is about to return to its caller.

Let's now look at the execution point object corresponding to this visualization:

```javascript
    {
      "ordered_globals": [
        "foo", 
        "bar", 
        "baz"
      ], 
      "stdout": "", 
      "func_name": "baz", 
      "stack_to_render": [
        {
          "frame_id": 1, 
          "encoded_locals": {
            "y": 2, 
            "x": 1, 
            "z": 3
          }, 
          "is_highlighted": false, 
          "is_parent": false, 
          "func_name": "foo", 
          "is_zombie": false, 
          "parent_frame_id_list": [], 
          "unique_hash": "foo_f1", 
          "ordered_varnames": [
            "x", 
            "y", 
            "z"
          ]
        }, 
        {
          "frame_id": 2, 
          "encoded_locals": {
            "a": 1, 
            "b": 2
          }, 
          "is_highlighted": false, 
          "is_parent": false, 
          "func_name": "bar", 
          "is_zombie": false, 
          "parent_frame_id_list": [], 
          "unique_hash": "bar_f2", 
          "ordered_varnames": [
            "a", 
            "b"
          ]
        }, 
        {
          "frame_id": 3, 
          "encoded_locals": {
            "__return__": 1, 
            "c": 1
          }, 
          "is_highlighted": true, 
          "is_parent": false, 
          "func_name": "baz", 
          "is_zombie": false, 
          "parent_frame_id_list": [], 
          "unique_hash": "baz_f3", 
          "ordered_varnames": [
            "c", 
            "__return__"
          ]
        }
      ], 
      "globals": {
        "bar": [
          "REF", 
          2
        ], 
        "foo": [
          "REF", 
          1
        ], 
        "baz": [
          "REF", 
          3
        ]
      }, 
      "heap": {
        "1": [
          "FUNCTION", 
          "foo(x, y, z)", 
          null
        ], 
        "2": [
          "FUNCTION", 
          "bar(a, b)", 
          null
        ], 
        "3": [
          "FUNCTION", 
          "baz(c)", 
          null
        ]
      }, 
      "line": 8, 
      "event": "return"
    }, 
```

First things first: This is a `return` event occurring on line 8 (the `return c` line in `baz`). The currently-active
function is `baz`. There are three global variables: `foo`, `bar`, and `baz`, which all point to function objects
on the heap.

The only new kind of field is `stack_to_render`, which is (unsurprisingly) a list of stack frames to render.
In this case, `stack_to_render` contains three elements -- the frames for `foo`, `bar`, and `baz`, in that exact order.
The frontend simply walks down `stack_to_render` and renders each frame in a similar way that it renders global variables.

Let's now zoom in on one particular frame in `stack_to_render`. Here is the frame for `bar`:

```javascript
        {
          "frame_id": 2, 
          "encoded_locals": {
            "a": 1, 
            "b": 2
          }, 
          "is_highlighted": false, 
          "is_parent": false, 
          "func_name": "bar", 
          "is_zombie": false, 
          "parent_frame_id_list": [], 
          "unique_hash": "bar_f2", 
          "ordered_varnames": [
            "a", 
            "b"
          ]
        }, 
```

For starters, `func_name` is the name of the function, and `is_highlighted` is true only if the current
frame is the "top-most" one (telling the frontend to highlight it in a brighter color).

`encoded_locals` is a mapping from local variable names to their values, similar to how `globals`
provides a mapping from global variable names to their values.

`ordered_varnames` is an ordered list of keys from `encoded_locals`, usually sorted by order of appearance
during execution. The global analogue for this field is `ordered_globals`. (I suppose this field should be named
`ordered_locals`, but I haven't gotten around to renaming yet.)

`frame_id` is an integer that *uniquely* identifies this frame; the first function call (of *any* function) gets
a frame ID of 1, and then subsequent calls get successively increasing frame IDs.

`unique_hash` is a unique string that identifies this frame. For now, a simple way
to construct `unique_hash` is by concatenating the frame's function name with `frame_id`.
Note that `unique_hash` seems redundant with `frame_id`, since the latter is already unique.
However, you'll see in the "Closures and Zombie Frames" section why `unique_hash` is required.

Finally, ignore `is_parent`, `is_zombie`, and `parent_frame_id_list` for now. We'll cover those in the more advanced
"Closures and Zombie Frames" section below.


## Closures and Zombie Frames (advanced)

(TODO: WRITE ME!)

(TODO: talk about needing to append `_p` and `_z` onto `unique_hash` when a frame becomes a parent or zombie,
respectively, since the frontend needs to know when to refresh the display.)
