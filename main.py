from bottle import run, route, request, response, template, Bottle
import json
from fpdf import FPDF
from PIL import Image

r = Bottle()

def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)


def convert_to_pdf(name):
    pdf = FPDF()

    resize_image(input_image_path='images\\' + name + '.png',
                 output_image_path='images\\' + name + '.png',
                 size=(620, 850))

    image = "images\\" + name + ".png"

    pdf.add_page()
    pdf.image(image, 0, 0, 0, 0)
    pdf.output("pdfs\\" + name + ".pdf", "F")

@r.get('/x')
@r.post('/x')
def main_loop():
    PythonDict = {}
    PythonDict['forms'] = {}
    for item in request.forms:
        PythonDict['forms'][item] = request.forms.get(item)

    PythonDict['query'] = {}
    for item in request.forms:
        PythonDict['query'][item] = request.query.get(item)

    PythonDict['GET'] = {}
    for item in request.GET:
        PythonDict['GET'][item] = request.GET.get(item)

    PythonDict['POST'] = {}
    for item in request.POST:
        PythonDict['POST'][item] = request.POST.get(item)

    PythonDict['params'] = {}
    for item in request.params:
        PythonDict['params'][item] = request.params.get(item)


    # todo: Get the name of manga by ID ( request.GET.get(item) - ID of manga )

    name = "3"   # name of got manga

    convert_to_pdf(request.GET.get(item)) # WARNING!!!! PARAMETER CHANGE TO NAME OF THE MANGA. IT IS ID OF THE MANGA NOW

    return json.dumps(PythonDict, indent=3) + "\n\n" + "images\\" + name + "    has converted to PDF"




r.run(host='localhost', port=8080, reloader=True)
