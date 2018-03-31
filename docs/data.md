### Links
[home](../README.md) &#8226; [intro](introduction.md) &#8226; [env](environment.md) &#8226;
[data](data.md)

### Data

Before we can decide what to do, we need to get some understanding of what we have at our
disposal.  One of the core elements is data.  As I stated earlier, the core of data comes from the
GTSDB. This [link](http://benchmark.ini.rub.de/Dataset_GTSDB/FullIJCNN2013.zip) downloads the
associated zip file and on the surface, it's a meaty 1.6GB.  Unfortunately, the files are in the
rather inefficient Portable Pixmap format (a 24-bit-color image where each pixel is encoded as
uncompressed text). On closer inspection, there are only 900 images spread across 42 classes. Here
is their distribution:

