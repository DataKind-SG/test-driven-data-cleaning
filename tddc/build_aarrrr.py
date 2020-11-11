from string import Template

d = { 'input_filename':"in.R", 'output_filename':"out.R" }
f = open( 'r/main.R' )
s = Template( f.read() )
print(s.substitute(d))
