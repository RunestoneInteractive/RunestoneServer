..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Exercises
---------



#. 


    .. tabbed:: q1

        .. tab:: Question

            The following sample file called ``studentdata.txt`` contains one line for each student in an imaginary class.  The 
            student's name is the first thing on each line, followed by some exam scores.  
            The number of scores might be different for each student.

            .. raw:: html

                <pre id="studentdata.txt">
                joe 10 15 20 30 40
                bill 23 16 19 22
                sue 8 22 17 14 32 17 24 21 2 9 11 17
                grace 12 28 21 45 26 10
                john 14 32 25 16 89
                </pre>

            Using the text file ``studentdata.txt`` write a program that prints out the names of
            students that have more than six quiz scores.



            .. actex:: ex_6_1


        .. tab:: Answer

            .. activecode:: ch_files_q1answer

                f = open("studentdata.txt","r")

                for aline in f:
                    items = aline.split()
                    if len(items[1:]) > 6:
                        print(items[0])

                f.close()

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_eb4a097382404ffe81300aac5744e3fe



#. Using the text file ``studentdata.txt`` (shown in exercise 1) write a program that calculates the average grade
   for each student, and print out the student's name along with their average grade.

   .. actex:: ex_10_2



#.

    .. tabbed:: q3

        .. tab:: Question


            Using the text file ``studentdata.txt`` (shown in exercise 1) write a program that calculates the minimum and
            maximum score for each student.  Print out their name as well.



            .. actex:: ex_6_3


        .. tab:: Answer

            .. activecode:: ch_files_q3answer

                f = open("studentdata.txt","r")

                for aline in f:
                   items = aline.split()
                   print(items[0],"max is", max(items[1:]), "min is", min(items[1:]))

                f.close()

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_eb4a097382404ffe81300aac5744e3fe_q3











#.  Here is a file called ``labdata.txt`` that contains some sample data from a lab experiment.


    .. raw:: html

        <pre id='labdata.txt'>
        44 71
        79 37
        78 24
        41 76
        19 12
        19 32
        28 36
        22 58
        89 92
        91 6
        53 7
        27 80
        14 34
        8 81
        80 19
        46 72
        83 96
        88 18
        96 48
        77 67
        </pre>

    Interpret the data file ``labdata.txt`` such that each line contains a an x,y coordinate pair.
    Write a function called ``plotRegression`` that reads the data from this file
    and uses a turtle to plot those points and a best fit line according to the following
    formulas:

    :math:`y = \bar{y} + m(x - \bar{x})`

    :math:`m = \frac{\sum{x_iy_i - n\bar{x}\bar{y}}}{\sum{x_i^2}-n\bar{x}^2}`

    where :math:`\bar{x}` is the mean of the x-values, :math:`\bar{y}` is the mean of the y-
    values and :math:`n` is the number of points.  If you are not familiar with the
    mathematical :math:`\sum` it is the sum operation.  For example :math:`\sum{x_i}`
    means to add up all the x values.

    Your program should analyze the points and correctly scale the window using
    ``setworldcoordinates`` so that that each point can be plotted.  Then you should
    draw the best fit line, in a different color, through the points.


    .. actex:: ex_10_4


#.  


    .. tabbed:: q5

        .. tab:: Question

            At the end of this chapter is a very long file called ``mystery.txt`` The lines of this
            file contain either the word UP or DOWN or a pair of numbers.  UP and DOWN are instructions
            for a turtle to lift up or put down its tail.  The pairs of numbers are some x,y coordinates.
            Write a program that reads the file ``mystery.txt`` and uses the turtle to draw the picture
            described by the commands and the set of points.

            .. actex:: ex_10_5



        .. tab:: Answer

            .. activecode:: ch_files_q5answer

                import turtle

                t = turtle.Turtle()
                wn = turtle.Screen()
                wn.setworldcoordinates(-300,-300,300,300)

                f = open("mystery.txt","r")

                for aline in f:
                    items = aline.split()
                    if items[0] == "UP":
                        t.up()
                    else:
                        if items[0] == "DOWN":
                            t.down()
                        else:
                            #must be coords
                            t.goto(int(items[0]),int(items[1]))

                f.close()
                wn.exitonclick()



        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_eb4a097382404ffe81300aac5744e3fe_q5







Here is the ``mystery.txt`` file:


.. raw:: html

   <pre id="mystery.txt">
   UP
   -218 185
   DOWN
   -240 189
   -246 188
   -248 183
   -246 178
   -244 175
   -240 170
   -235 166
   -229 163
   -220 158
   -208 156
   -203 153
   -194 148
   -187 141
   -179 133
   -171 119
   -166 106
   -163 87
   -161 66
   -162 52
   -164 44
   -167 28
   -171 6
   -172 -15
   -171 -30
   -165 -46
   -156 -60
   -152 -67
   -152 -68
   UP
   -134 -61
   DOWN
   -145 -66
   -152 -78
   -152 -94
   -157 -109
   -157 -118
   -151 -128
   -146 -135
   -146 -136
   UP
   -97 -134
   DOWN
   -98 -138
   -97 -143
   -96 -157
   -96 -169
   -98 -183
   -104 -194
   -110 -203
   -114 -211
   -117 -220
   -120 -233
   -122 -243
   -123 -247
   -157 -248
   -157 -240
   -154 -234
   -154 -230
   -153 -229
   -149 -226
   -146 -223
   -145 -219
   -143 -214
   -142 -210
   -141 -203
   -139 -199
   -136 -192
   -132 -184
   -130 -179
   -132 -171
   -133 -162
   -134 -153
   -138 -145
   -143 -137
   -143 -132
   -142 -124
   -138 -112
   -134 -104
   -132 -102
   UP
   -97 -155
   DOWN
   -92 -151
   -91 -147
   -89 -142
   -89 -135
   -90 -129
   -90 -128
   UP
   -94 -170
   DOWN
   -83 -171
   -68 -174
   -47 -177
   -30 -172
   -15 -171
   -11 -170
   UP
   12 -96
   DOWN
   9 -109
   9 -127
   7 -140
   5 -157
   9 -164
   22 -176
   37 -204
   40 -209
   49 -220
   55 -229
   57 -235
   57 -238
   50 -239
   49 -241
   51 -248
   53 -249
   63 -245
   70 -243
   57 -249
   62 -250
   71 -250
   75 -250
   81 -250
   86 -248
   86 -242
   84 -232
   85 -226
   81 -221
   77 -211
   73 -205
   67 -196
   62 -187
   58 -180
   51 -171
   47 -164
   46 -153
   50 -141
   53 -130
   54 -124
   57 -112
   56 -102
   55 -98
   UP
   48 -164
   DOWN
   54 -158
   60 -146
   64 -136
   64 -131
   UP
   5 -152
   DOWN
   1 -150
   -4 -145
   -8 -138
   -14 -128
   -19 -119
   -17 -124
   UP
   21 -177
   DOWN
   14 -176
   7 -174
   -6 -174
   -14 -170
   -19 -166
   -20 -164
   UP
   -8 -173
   DOWN
   -8 -180
   -5 -189
   -4 -201
   -2 -211
   -1 -220
   -2 -231
   -5 -238
   -8 -241
   -9 -244
   -7 -249
   6 -247
   9 -248
   16 -247
   21 -246
   24 -241
   27 -234
   27 -226
   27 -219
   27 -209
   27 -202
   28 -193
   28 -188
   28 -184
   UP
   -60 -177
   DOWN
   -59 -186
   -57 -199
   -56 -211
   -59 -225
   -61 -233
   -65 -243
   -66 -245
   -73 -246
   -81 -246
   -84 -246
   -91 -245
   -91 -244
   -88 -231
   -87 -225
   -85 -218
   -85 -211
   -85 -203
   -85 -193
   -88 -185
   -89 -180
   -91 -175
   -92 -172
   -93 -170
   UP
   -154 -93
   DOWN
   -157 -87
   -162 -74
   -168 -66
   -172 -57
   -175 -49
   -178 -38
   -178 -26
   -178 -12
   -177 4
   -175 17
   -172 27
   -168 36
   -161 48
   -161 50
   UP
   -217 178
   DOWN
   -217 178
   -217 177
   -215 176
   -214 175
   -220 177
   -223 178
   -223 178
   -222 178
   UP
   -248 185
   DOWN
   -245 184
   -240 182
   -237 181
   -234 179
   -231 177
   -229 176
   -228 175
   -226 174
   -224 173
   -223 173
   -220 172
   -217 172
   -216 171
   -214 170
   -214 169
   UP
   -218 186
   DOWN
   -195 173
   -183 165
   -175 159
   -164 151
   -158 145
   -152 139
   -145 128
   -143 122
   -139 112
   -138 105
   -134 95
   -131 88
   -129 78
   -126 67
   -125 62
   -125 54
   -124 44
   -125 38
   -126 30
   -125 27
   -125 8
   -126 5
   -125 -9
   -122 -15
   -115 -25
   -109 -32
   -103 -39
   -95 -42
   -84 -45
   -72 -47
   -56 -48
   -41 -47
   -31 -46
   -18 -45
   -1 -44
   9 -43
   34 -45
   50 -52
   67 -61
   83 -68
   95 -80
   112 -97
   142 -115
   180 -132
   200 -146
   227 -159
   259 -175
   289 -185
   317 -189
   349 -190
   375 -191
   385 -192
   382 -196
   366 -199
   352 -204
   343 -204
   330 -205
   315 -209
   296 -212
   276 -214
   252 -208
   237 -202
   218 -197
   202 -193
   184 -187
   164 -179
   147 -173
   128 -168
   116 -164
   102 -160
   88 -158
   78 -159
   69 -162
   57 -164
   56 -165
   51 -165
   UP
   68 -144
   DOWN
   83 -143
   96 -141
   109 -139
   119 -146
   141 -150
   161 -155
   181 -163
   195 -169
   208 -179
   223 -187
   241 -191
   247 -193
   249 -194
   UP
   -6 -141
   DOWN
   -15 -146
   -29 -150
   -42 -154
   -51 -153
   -60 -152
   -60 -152
   UP
   -90 -134
   DOWN
   -85 -131
   -79 -128
   -78 -123
   -80 -115
   -82 -106
   -80 -101
   -76 -101
   UP
   -81 -132
   DOWN
   -76 -130
   -71 -126
   -72 -124
   UP
   43 -118
   DOWN
   44 -125
   47 -135
   41 -156
   37 -160
   40 -166
   47 -171
   47 -171
   UP
   -106 -153
   DOWN
   -107 -167
   -106 -178
   -109 -192
   -114 -198
   -116 -201
   </pre>
