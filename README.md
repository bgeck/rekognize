# rekognize
Interactive art experiment that examines social issues around AI and machine learning.

#requirements
This project is designed for Python 2.7 or before. 
You will need the following installed:

## General dependencies
```OpenCV```

For me on Mac OSX, that means simply
```brew install opencv```

## Python Speicifc - installable using pip.
```pip install scipy numpy Pillow pygame requests SimpleCV svgwrite```


## Note
Sometimes SimpleCV has an issue where it is missing it's logo file. This is the fix for that:
```mkdir /usr/local/lib/python2.7/site-packages/SimpleCV/sampleimages/ && cp simplecv.png /usr/local/lib/python2.7/site-packages/SimpleCV/sampleimages/```