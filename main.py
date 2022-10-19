import codecs
import storage as stg
import query as qry
import create_pdf as pdf


so_info_oid = "1.3.6.1.2.1.1.1.0"
device_name_oid = "1.3.6.1.2.1.1.5.0"
contact_oid = "1.3.6.1.2.1.1.4.0"
location_oid = "1.3.6.1.2.1.1.6.0"
total_interfaces_oid = "1.3.6.1.2.1.2.1.0"
interfaces_desc_oid = "1.3.6.1.2.1.2.2.1.2."
interfaces_status_oid = "1.3.6.1.2.1.2.2.1.7."
linux_logo_path = "C:\\Users\\tala_\\PycharmProjects\\oid_queries\\img\\linux.png"
windows_logo_path = "C:\\Users\\tala_\\PycharmProjects\\oid_queries\\img\\windows.png"
html_path = "C:\\Users\\tala_\\PycharmProjects\\oid_queries\\PDFTemplate.html"


def add_com():
    name = input("Ingrese el nombre de la comunidad:")
    version = int(input("Ingrese la version:"))
    port = int(input("Ingrese el puerto:"))
    ip_add = input("Ingrese la direccion ip:")
    stg.add_community(name, version, port, ip_add)
    print("Comunidad creada con exito.")


def del_com():
    name = input("Ingrese el nombre de la comunidad:")
    stg.delete_community(name)
    print("Comunidad borrada con exito.")


def com_report(name):
    com_rep = {}
    com = stg.get_community(name)
    com_rep["so"] = get_qry_res(name, com, so_info_oid)
    com_rep["dev-name"] = get_qry_res(name, com, device_name_oid)
    com_rep["con"] = get_qry_res(name, com, contact_oid)
    com_rep["loc"] = get_qry_res(name, com, location_oid)
    com_rep["no-int"] = get_qry_res(name, com, total_interfaces_oid)
    length = int(com_rep["no-int"]) + 1
    com_rep["desc"] = [get_qry_res(name, com, interfaces_desc_oid + str(i)) for i in range(1, length)]
    com_rep["stat"] = [get_qry_res(name, com, interfaces_status_oid + str(i)) for i in range(1, length)]
    return com_rep;


def html_vars(name):
    temp_com = com_report(name)
    hvars={}
    windows = False

    hvars["so_info"] = temp_com["so"]
    if hvars["so_info"].find("Windows") != -1:
        windows = True

    hvars["dev_name"] = temp_com["dev-name"]
    hvars["con_info"] = temp_com["con"]
    hvars["loc"] = temp_com["loc"]
    hvars["interfaces"] = temp_com["no-int"]

    table = f'<table style="border-collapse: collapse; width: 100%; height: 72px;" border="1"><thead><tr><th>Interfaz ' \
            f'</th><th>Estado</th></tr></thead><tbody>'

    for i in range(int(hvars["interfaces"])):
        desc = temp_com["desc"][i]
        if windows:
            deco = codecs.decode(desc[3:], "hex")
            desc = str(deco, 'utf-8')
        state = temp_com["stat"][i]
        row = f'<tr><td>{desc} </td><td>{state}</td></tr>'
        table += row

    img = "windows.png" if windows else "linux.png"
    table += f'</tbody></table>'
    #<p style="text-align: center;"><img src="./img/{img}" alt="" width="300" height="300" /></p>
    hvars["table"] = table

    return hvars


def get_qry_res(name, com, oid):
    raw_res = qry.oid_query(name, com[0], com[1], com[2], oid)
    index = str(raw_res).find('=')
    return str(raw_res)[index + 1:]


def print_report(name):
    com_rep = com_report(name)
    windows = False

    print("Sistema operativo: " + com_rep["so"])
    if com_rep["so"].find("Windows") != -1:
        windows = True

    print("Nombre del dispositivo: " + com_rep["dev-name"])
    print("Contacto: " + com_rep["con"])
    print("Ubicacion: " + com_rep["loc"])
    print("Numero de interfaces: " + com_rep["no-int"])
    print("Descripcion\tEstado")
    [print(com_rep["desc"][i] + "\t" + com_rep["stat"][i]) for i in range(int(com_rep["no-int"]))]


def main():
    flag = True
    while flag:
        op = int(input("Sistema de Administracion de Red\nPractica 1 - Adquisicion de Informacion\nLopez Lopez Oscar "
                       "Manuel 4CM13 2020630199\n1.Agregar Comunidad\n2.Eliminar Comunidad\n3.Listar "
                       "Comunidad\n4.Mostrar reporte en pantalla\n5.Crear PDF\nOtro: Salir\n"))
        if op == 1:
            add_com()
        elif op == 2:
            del_com()
        elif op == 3:
            print(stg.communities.items())
        elif op == 4:
            name = input("Ingrese el nombre de la comunidad: ")
            print_report(name)
        elif op == 5:
            name = input("Ingrese el nombre de la comunidad: ")
            variables = html_vars(name)
            pdf_name = name + ".pdf"
            pdf.create(html_path, variables, pdf_name)
        else:
            flag = False

    windows_com = "talaWindowsCom"
    ubuntu_com = "talaUbuntuCom"
    windows_ip = "localhost"
    ubuntu_ip = "192.168.56.101"
    #
    #192.168.21.95


if __name__ == '__main__':
    main()

