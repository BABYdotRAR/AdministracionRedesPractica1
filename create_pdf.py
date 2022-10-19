import jinja2
import pdfkit


def create(html_path, vars_dic, pdf_name):
    file_name = html_path.split('\\')[-1]
    file_path = html_path.replace(file_name, '')

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(file_path))
    template = env.get_template(file_name)
    html = template.render(vars_dic)

    options = {
        'page-size': 'Letter',
        'margin-top': '0.1in',
        'margin-bottom': '0.1in',
        'margin-right': '0.1in',
        'margin-left': '0.1in',
        'encoding': 'UTF-8',
        'enable-local-file-access': ""
    }

    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    output_path = "C:\\Users\\tala_\\PycharmProjects\\oid_queries\\" + pdf_name

    pdfkit.from_string(html, output_path, options=options, configuration=config)
    print("Archivo pdf creado con exito");
