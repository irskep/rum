RUM User Manual
v0.1

RUM (bRainfUck iMproved) is a Brainfuck interpreter with Extra Features! It supports 0, -1, and 'ignore' EOF types, as well as an arbitrarily bounded (or unbounded) tape length. It also supports strings, numbered repetitions, and comments.

The following program converts the string "hello world" to uppercase:
"helloworld",[--------------------------------.,]

You can repeat a command n times by preceding that command with a number. Using this feature, we can significantly shorten the 'helloworld' program:
"helloworld",[32-.,]