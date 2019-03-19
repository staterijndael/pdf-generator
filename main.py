from bottle import run, route, request, response, template, Bottle,error
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
    '''Checking to file existence'''
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
    """Error if page is not found"""
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
            '''Getting the json from the api service by ID of manga'''
            r = requests.get("https://api.anibe.ru/posts/" + request.GET.get(item))
            j = r.json()
        elif item == "episode":
            '''Getting the link on screenshots of the episode of the manga same name of file on the server'''
            episodes = j["episodes"][request.GET.get(item)]
            answer = ""
            for v in episodes:
                '''Cut the symbols, which not perceive into the name of file'''
                cuted_link = v.replace(":", "")
                cuted_link = cuted_link.replace("/", "")
                if (convert_to_pdf(cuted_link)):
                    '''If file already exists, then just add the path to result'''
                    answer += "images\\" + v + ", "
                else:
                    '''If file not exists, then download it from the origin'''
                    r = requests.get(v)

                    with open('images\\' + cuted_link, 'wb') as f:
                        f.write(r.content)
                    convert_to_pdf(cuted_link)
                    answer += "images\\" + v + ", "
            if answer:
                '''Just print files,which had corverted to PDF'''
                return json.dumps(PythonDict, indent=3) + "\n\n" + answer + "    had converted to PDF"
            else:
                return json.dumps(PythonDict, indent=3) + "\n"

    PythonDict['POST'] = {}
    for item in request.POST:
        PythonDict['POST'][item] = request.POST.get(item)

    PythonDict['params'] = {}
    for item in request.params:
        PythonDict['params'][item] = request.params.get(item)


r.run(host='localhost', port=8080, reloader=True)
