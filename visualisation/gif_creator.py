import re
import imageio
from os import walk

f = []
for (dirpath, dirnames, filenames) in walk('C:/Users/samue/OneDrive - Vlaamse overheid - Office 365/Github_large_files/multi/'):
    f.extend(filenames)
    break


def sorted_nicely(l):
    """ Sort the given iterable in the way that humans expect."""
    def convert(text): return int(text) if text.isdigit() else text

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


test = []
for x in sorted_nicely(f):
    test.append(x)

images = []
for filename in test:
    images.append(imageio.imread('C:/Users/samue/OneDrive - Vlaamse overheid - Office 365/Github_large_files/multi/' + filename))
imageio.mimsave('../output_ml/movie_iow_multiple.gif', images)
