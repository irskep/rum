RUM User Manual
v0.1

RUM (bRainfUck iMproved) is a Brainfuck interpreter with Extra Features! It supports 0, -1, and 'ignore' EOF types, as well as an arbitrarily bounded (or unbounded) tape length. It also supports strings, numbered repetitions, and comments.

The following program converts the string "hello world" to uppercase:
"helloworld",[--------------------------------.,]

You can repeat a command n times by preceding that command with a number. Using this feature, we can significantly shorten the 'helloworld' program:
"helloworld",[32-.,]

Procedures are defined by parentheses, pbrain-style. For example, +([-]) puts a procedure that resets the current cell to zero in slot 1. Use : to call the procedure denoted by the value of the current cell.

For example, to print out HELLOWORLD twice:
+(,[32-.,])"helloworld":+:
In this example, we store the function "helloworld",[32-.,] in slot 1 and call it immediately. Since strings are null-terminated, we need to increment the cell once more to call the procedure again.

Since the uppercase function will not work on punctuation, we can use procedures to uppercase individual words:
+(,[.,])+(,[32-.,])"hello":[-]+", ":[-]++"world":
In this example, procedure 1 is essentially a print function, and procedure 2 is the uppercase function from earlier. With comments:
+(,[.,]) 		#procedure 1 is print
+(,[32-.,]) 	#procedure 2 is print-uppercase
"hello": 		#print 'HELLO'
", "[-]+:		#print ', '
"world"[-]++: 	#print 'WORLD'

Comment out lines until the next LF with #. Please use discretion when putting punctuation in comments, as I have not tested it at all.

RUM is in the public domain.