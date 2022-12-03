## Online Machine Learning model

# Data streams
River is a library to build online machine learning models. Such models operate on data streams. But a data stream is a bit of a vague concept.

In general, a data stream is a sequence of individual elements. In the case of machine learning, each element is a bunch of features. 
e call these samples, or observations. Each sample might follow a fixed structure and always contain the same features. 
But features can also appear and disappear over time. That depends on the use case.

# Reactive and proactive data streams¶
The origin of a data stream can vary, and usually it doesn't matter. You should be able to use River regardless of where your data comes from.
It is however important to keep in mind the difference between reactive and proactive data streams.

Reactive data streams are ones where the data comes to you. For instance, when a user visits your website, that's out of your control. You have no
influence on the event. It just happens and you have to react to it.

Proactive data streams are ones where you have control on the data stream. For example, you might be reading the data from a file. You decide at which
speed you want to read the data, in what order, etc.

If you consider data analysis as a whole, you're realize that the general approach is to turn reactive streams into proactive datasets.
Events are usually logged into a database and are processed offline. Be it for building KPIs or training models.

The challenge for machine learning is to ensure models you train offline on proactive datasets will perform correctly in production on reactive data streams.

# Online processing¶
Online processing is the act of processing a data stream one element at a time. In the case of machine learning, that means training a model by teaching
it one sample at a time. This is completely opposite to the traditional way of doing machine learning, which is to train a model on a whole batch data at a time.

An online model is therefore a stateful, dynamic object. It keeps learning and doesn't have to revisit past data. It's a different way of doing things,
and therefore has its own set of pros and cons.
