
.. _csv_chap:

.CSV Output
===========

CSV stands for Comma Separated Values. If you print out tabular data in CSV format, it can be easily imported into other programs like Excel, Google spreadsheets, or a statistics package (R, stata, SPSS, etc.).

For example, we will make a file with the following contents. If you save it as a file name grades.csv, then you could it import it into one of those programs. The first line gives the column names and the later lines each give the data for one row.

.. sourcecode:: python

   Name, score, grade
   Jamal, 98, A+
   Eloise, 87, B+
   Madeline, 99, A+
   
As long as none of your data contains commas, you can do this by hand using output formatting. You previously learned about :ref:`writing output to a text file <write_text_file_chap>`.

The typical pattern for writing data to a CSV file will be to write a header row, and loop through the items in a list (or dictionary), outputting one row for each. For example, you could try this in a native python interpreter (in the browser, you can't write files.) After you run it, take a look at the contents of the newly created file, grades.csv, and try importing it into Excel or a Google spreadsheet.

.. sourcecode:: python

   students = [("Jamal", 98, "A+"),
               ("Eloise", 87, "B+"),
               ("Madeline", 99, "A+")]

   outfile = open("grades.csv","w")
   # output the header row
   outfile.write("Name, score, grade\n")
   # output each of the rows:
   for student in students:
       outfile.write("%s, %d, %s\n" % student)
   outfile.close()
   
There are a couple of things worth noting in the code above. First, unlike the print statement, the .write() method on a file object does not automatically insert a newline. Instead, we had to explicitly add the character ``\n`` at the end of each line.

Second, we used string interpolation on the second to last line. That makes it  clear that we're taking the contents of the tuple student and putting the component values into the three spots in the string. We could have written that line with a bunch of strings and variables combined with + signs, but that code would be much harder for humans to read and understand.

If one or more columns contain text, and that text could contain commas, we need to do something to distinguish a comma in the text from a comma that is separating different values (cells in the table). There are a few options for doing that in CSV format, but the most common one is to enclose each of the values in double quotes. This starts to get a little tricky, because we will need to have the double quote character inside the string output. But it is doable. Indeed, one reason python allows strings to be delimited with either single quotes or double quotes is so that one can be used to delimit the string and the other can be a character in the string.

.. sourcecode:: python

   students = [("Jones, Jamal J", 98, "A+"),
               ("Ensted, Eloise E", 87, "B+"),
               ("Morton, Madeline", 99, "A+")]
   
   outfile = open("grades.csv","w")
   # output the header row
   outfile.write('"Name", "score", "grade"\n')
   # output each of the rows:
   for student in students:
       outfile.write('"%s", "%d", "%s"\n' % student)
   outfile.close()

Python also includes a .csv module, which provides a cleaner, more abstract way to handle writing .csv files. It can generate slightly different CSV formats, and handles a few other aspects of more complicated outputs in a nice way. You are welcome to explore the `documentation for the csv module <https://docs.python.org/2/library/csv.html>`_ if you'd like to learn how to use it.