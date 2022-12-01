from functools import lru_cache



@lru_cache(maxsize=2048)
class One(object):
     def __init__(self):
         self.a = None

     def set_a(self,val):
         self.a = val

     def get_a(self):
         return self.a

class new():
    def print_cache():
        print(One().get_a())

# Cache
second=One()
second.set_a(4)
new.print_cache()

