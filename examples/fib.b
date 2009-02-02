#Needs 4 cells
#4th cell is repetition count
#run RUM with -r for raw number output
#i.e. "python RUM.py examples/fib.b -r"

(>[<+>-])		#store shift-number-left procedure at 0
+>+> 			#initialize to 1|1|0
>10+ 			#give tenth fibonacci number
[
	3<			#go back to start
	[>+>+<<-]	#add first number to other 2, destructive
	2:			#shift numbers left
	>-			#decrement counter
]
3<.				#print output