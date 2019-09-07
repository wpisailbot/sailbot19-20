Installation
--------------------------------------------------------------------------------

To install this library, just place this entire folder as a subfolder in your
Arduino/lib/targets/libraries folder.

When installed, this library should look like:

Arduino/lib/targets/libraries/Comm_encoder              (this library's folder)
Arduino/lib/targets/libraries/Comm_encoder/Comm_encoder.cpp     (the library implementation file)
Arduino/lib/targets/libraries/Comm_encoder/Comm_encoder.h       (the library description file)
Arduino/lib/targets/libraries/Comm_encoder/keywords.txt (the syntax coloring file)
Arduino/lib/targets/libraries/Comm_encoder/examples     (the examples in the "open" menu)
Arduino/lib/targets/libraries/Comm_encoder/readme.txt   (this file)

Building
--------------------------------------------------------------------------------

After this library is installed, you just have to start the Arduino application.
You may see a few warning messages as it's built.

To use this library in a sketch, go to the Sketch | Import Library menu and
select Comm_encoder.  This will add a corresponding line to the top of your sketch:
#include <Comm_encoder.h>

To stop using this library, delete that line from your sketch.

Geeky information:
After a successful build of this library, a new file named "Comm_encoder.o" will appear
in "Arduino/lib/targets/libraries/Comm_encoder". This file is the built/compiled library
code.

If you choose to modify the code for this library (i.e. "Comm_encoder.cpp" or "Comm_encoder.h"),
then you must first 'unbuild' this library by deleting the "Comm_encoder.o" file. The
new "Comm_encoder.o" with your code will appear after the next press of "verify"

