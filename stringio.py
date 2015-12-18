import cStringIO

o = cStringIO.StringIO()
o.write('First line \n')
print >>o, 'Second line.'
c = o.getvalue()
print c
o.close()