import facebook
import pdb

secret = '4df924206fdefc71bbf5e8fd90fed874'

access_token = 'CAACEdEose0cBAFDEXGZBC5gNS6P9ooF8ZAXatCX2Imp3pJ1vQMnhLRVZCOnUdY93qzCFNfKVAHdBSXtgvI4OHzVEyRHQQWI4vdqZCWKjH86qxnVCUtaZASFzNz9ujkZAZBCEkTZAxaEXPAt0FSI8Wu1bQGKEBH6TwZCGt2YiWoBHLJFGaLddjiJEOEQRziFFZAv8nfZAWmFylXA9REphkc2JZBZBAWAC9ULwMbXAZD'

graph = facebook.GraphAPI(access_token=access_token)
obj = graph.get_object(id='me')
pdb.set_trace()
#obj = graph.get_connections(id='me', connection_name='friends')
print(obj)
