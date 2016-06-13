import re

s = '0 (RMB)'
pattern = re.compile('^(\d+\.\d+|\d+)\s*\(([a-zA-Z]+)\)$')
#pattern = re.compile('^(\d+\.\d+)$')
match = pattern.match(s)
print match
print match.group(1)
print match.start()
print match.end()
print match.span()