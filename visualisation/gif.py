import imageio
images = []
for filename in file_names:
    images.append(imageio.imread(filename))
imageio.mimsave('./output_ml/movie_iow.gif', images)