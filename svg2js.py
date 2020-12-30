import numpy as np
import re
import base64

def create_html(x,y,data):
    return np.array(["<!doctype html>\n",
        "<html lang=\"en\">\n",
        "<head>\n",
        "  <meta charset=\"utf-8\">\n",
        "\n",
        "  <title>The HTML5 Herald</title>\n",
        "  <meta name=\"description\" content=\"SVG Viewer\">\n",
        "  <meta name=\"author\" content=\"Darnell J. Otterson\">\n",
        "\n",
        "  <link rel=\"stylesheet\" href=\"css/styles.css?v=1.0\">\n",
        "\n",
        "</head>\n",
        "\n",
        "<body>\n",
        #"    <img id=\"brush\" src=\"data:image/png;base64, {}\" alt=\"Brush\" />\n".format(data),
        "    <img id=\"brush\" src=\"brush.png\" alt=\"Brush\" />\n",
        "    <canvas id=\"myCanvas\" width=\"{}\" height=\"{}\" ></canvas>\n".format(x,y),
        "    <script type=\"text/javascript\" src=\"svgWrite.js\"></script>\n",
        "</body>\n",
        "</html>\n"
    ])

def create_header():
    return np.array([
        "var ctx = document.getElementById('myCanvas').getContext('2d')\n",
        "var img = document.getElementById(\"brush\");\n",
        "var pat = ctx.createPattern(img, \"repeat\");\n",
        "ctx.beginPath();\n"
    ])

def move_to(x,y):
    return "ctx.moveTo({0},{1});\n".format(x,y)

def bezier_curve(x1,y1,x2,y2,x3,y3):
    return "ctx.bezierCurveTo({0},{1},{2},{3},{4},{5});\n".format(
        x1,y1,x2,y2,x3,y3
    )

# main
def main():
    jsFile = create_header()
    index = 2
    width = 0
    height = 0
    ignoreFirst=False

    with open('Quick sheets - page 2.svg', 'r') as fp:
        line = fp.readline()
        x = re.search("width=\"([\\d]+)\".height=\"([\\d]+)\"", line)
        # print("Width = {}, Height = {}".format(x.groups()[0],x.groups()[1]))
        width = x.groups()[0]
        height = x.groups()[1]
        # The third line contains the parts
        # We can get the width and height from the 
        line = fp.readline()
        x = re.search("xlink:href=\"data:image/png;base64,([\s\S]+)\"/>", line)
        data = x.groups()[0]

        # Trash line
        pattern = fp.readline()

    # With the pattern string

    # Split the string
    word_parts = pattern.strip().split(' ')
    # Fix-up the first move
    word_parts[2] = word_parts[2][3:]
    # print(word_parts[2])

    # Go through all the parts, 
    # if it starts with an M it is a move statement
    # if it is a c it is a Bezier curve
    # Move has itself and the next
    # The Bezier is itself and 5 more

    # This should trigger a fill on the objects, I am missing something
    jsFile = np.append(jsFile, "ctx.fillStyle = pat;\n");
    jsFile = np.append(jsFile, "ctx.fill();\n");

    # The first element is a move and does not need a stroke
    jsFile = np.append(jsFile,move_to(word_parts[index][1:], word_parts[index+1]))
    index+=2

    while(index < len(word_parts)):
        if('M' == word_parts[index][0]):
            # TODO: Need to add in logic to detect embedded paths
            # If there is an embedded path, it must not be filled
            # it is a cut-out
            jsFile = np.append(jsFile, "ctx.fillStyle = pat;\n");
            jsFile = np.append(jsFile, "ctx.fill();\n");
            jsFile = np.append(jsFile, "ctx.closePath();\n");
            jsFile = np.append(jsFile, "ctx.stroke();\n");
            jsFile = np.append(jsFile, "ctx.beginPath();\n");
            jsFile = np.append(jsFile,move_to(word_parts[index][1:], word_parts[index+1]))
            index+=2
        elif('C' == word_parts[index][0]):
            # Remember to shift the M out of the value
            jsFile = np.append(jsFile,bezier_curve(
                word_parts[index][1:], word_parts[index+1],
                word_parts[index+2], word_parts[index+3],
                word_parts[index+4], word_parts[index+5]
            ))
            index+=6
        else:
            index = len(word_parts)+1 # cheap we are done
    # close the path
    jsFile = np.append(jsFile, "ctx.closePath();\n");
    jsFile = np.append(jsFile, "ctx.stroke();\n")
    # Now write it out to a file and see what we get

#    with open('brush.png', 'wb') as fp:
#        fp.write(base64.b64decode(data))
    with open('svgWrite.js', 'w') as fp:
        fp.writelines(jsFile)
    with open('svgWrite.html', 'w') as fp:
        fp.writelines(create_html(width, height, data))

if __name__ == "__main__":
    main()
