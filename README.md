# svg2js
Convert ReMarkable 2 SVG to a JavaScript/HTML combination

So far, the format apparently only requires move and bezier; so a simple quick pathing is performed.

Embedded paths (e.g. cut-outs) are not accounted for.
The PNG color is inverted, will need to come up with a solution for this as well.

The goal of this is to actually create a tool to import and export into OneNote.