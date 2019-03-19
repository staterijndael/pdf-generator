from bottle import run, route, request, response, template, Bottle,error
import json
from fpdf import FPDF
from PIL import Image
import os.path
import requests
import json

r = Bottle()

def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)


def convert_to_pdf(name):
    pdf = FPDF()

    if(os.path.exists("images\\" + name)):

        resize_image(input_image_path='images\\' + name,
                 output_image_path='images\\' + name,
                 size=(620, 850))

        image = "images\\" + name

        pdf.add_page()
        pdf.image(image, 0, 0, 0, 0)
        pdf.output("pdfs\\" + name + ".pdf", "F")

        return True
    else: return False



@r.error(404)
def error404(error):
    return 'Ня, извините, страница не найдена!'


@r.get('/x')
@r.post('/x')
def main_loop():
    episodes = ""
    item = False
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
        if item == "id":
            r = requests.get("https://api.anibe.ru/posts/" + request.GET.get(item))
            j = r.json()
        elif item == "episode":
            episodes = j["episodes"][request.GET.get(item)]
            answer = ""
            for v in episodes:
                cuted_link = v.replace(":", "")
                cuted_link = cuted_link.replace("/", "")
                if (convert_to_pdf(cuted_link)):
                    answer += "images\\" + v + ", "
            if answer:
                return json.dumps(PythonDict, indent=3) + "\n\n" + answer + "    had converted to PDF"
            else:
                return json.dumps(PythonDict, indent=3) + "\n"

    PythonDict['POST'] = {}
    for item in request.POST:
        PythonDict['POST'][item] = request.POST.get(item)

    PythonDict['params'] = {}
    for item in request.params:
        PythonDict['params'][item] = request.params.get(item)

    # todo: Get the name of manga by ID ( request.GET.get(item) - ID of manga )




r.run(host='localhost', port=8080, reloader=True)
