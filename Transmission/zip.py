'''
This file is meant to test zipping a file full of PNG images
Successes: creating PNG (1024x1024), zip PNG, zip file of PNG's
Look into: Compressing file of PNG's
'''
import zipfile
from zipfile import ZIP_DEFLATED
from PIL import Image
import pathlib

# Create path to directory
directory = pathlib.Path('pngFiles/')

# Try catch for invalid zip files being compressed
try:
    # Open ZipFile object, choose compression type and level
    with zipfile.ZipFile("comp_test.zip", "w", ZIP_DEFLATED, compresslevel=8) as archive:
        # for each file in directory recursively yield all files(rglob)
        for filePath in directory.rglob("*"):
            # Write file into one archive file with name arcname
            archive.write(filePath, arcname=filePath.relative_to(directory))
except zipfile.BadZipFile as error:
    print(error)
    
# Print details of the directory
with zipfile.ZipFile("comp_test.zip", "r") as archive:
    archive.printdir()
    



