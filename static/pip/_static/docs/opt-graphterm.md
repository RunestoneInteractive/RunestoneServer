R. Saravanan from Texas A&M has integrated Online
Python Tutor with his [GraphTerm](http://code.mindmeldr.com/graphterm/)
project!

Here is a brief message from him on how to set it up:

------

I teach python to undergrads and my students have enjoyed using
PythonTutor to trace programs. I have modified PythonTutor slightly to
work within GraphTerm, which is a graphical terminal for unix computers
(written in python, of course!). So if you use the command line, you can
now trace your programs visually within the terminal.

To install it and run it, use the following three commands on a Mac or Linux system:

    sudo easy_install graphterm
    sudo gterm_setup              # To setup the toolchain
    gtermserver --terminal

This will run the GraphTerm server and open up a browser terminal
window. In that window, you can `cd` to the directory containing the
program you want to trace (say `example.py`), and then type:

    gtutor example.py | gframe -f

The first command outputs the HTML created by PythonTutor and the second
command renders it within the terminal (in an iframe). Click on the X on
the top right to end tracing. You can find more information in the
[GraphTerm project
page](http://code.mindmeldr.com/graphterm/start.html#code-tracing-using-python-tutor)

You can see a live demo of Inline PythonTutor in this [older YouTube
video](http://youtu.be/jmrmjC1VYsc) (about 1:20 after the start)

