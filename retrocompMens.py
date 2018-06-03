from bs4 import BeautifulSoup
import requests, argparse, csv

parser = argparse.ArgumentParser(description='Trae mensajes del foro Retrocomputación.')
parser.add_argument('mensajes', help = 'Cantidad de mensajes a traer (default:20)', type = int, nargs = '?', default = '20')
parser.add_argument('csv', help = 'Cantidad de mensajes a traer (default:20)', type = int, nargs = '?', default = '20')
argumentos = parser.parse_args()

URL = 'http://www.retrocomputacion.com/e107_plugins/forum/forum_latest.php?' + str(argumentos.mensajes)
pagina = requests.get(URL)

sopa = BeautifulSoup(pagina.text,'html.parser')

mensajes = sopa.find_all('td', attrs={'class': 'forumheader3', 'style': 'width:60%'})
autores = sopa.find_all('td', attrs={'class': 'forumheader3', 'style': 'width:27%; text-align:center'})

salida = []

for mensaje, autor in zip(mensajes, autores):
    titulo = mensaje.contents[0].string
    cuerpo = mensaje.text.replace(titulo,'')
    user = autor.contents[0].string
    linea = {'titulo': titulo, 'user': user, 'cuerpo': cuerpo}
    salida.append(linea)
    print("\nTITULO: " + titulo)
    print("USUARIO: " + user)
    print("CUERPO: " + cuerpo)

with open('mensajes.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['titulo', 'user', 'cuerpo']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerows(salida)