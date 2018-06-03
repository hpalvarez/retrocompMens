# Scraper de mensajes de Retrocomputación

# Importo BeautifulSoup 4 (requerido) y requests (trae la página), argparse (linea de comandos) y csv (para la salida)

from bs4 import BeautifulSoup
import requests, argparse, csv

# Leo de la línea de comandos cuantos mensajes quiero, por default traigo 20

parser = argparse.ArgumentParser(description='Trae mensajes del foro Retrocomputación.')
parser.add_argument('mensajes', help = 'Cantidad de mensajes a traer (default:20)', type = int, nargs = '?', default = '20')
argumentos = parser.parse_args()

# Armo la URL y la traigo

url = 'http://www.retrocomputacion.com/e107_plugins/forum/forum_latest.php?' + str(argumentos.mensajes)
pagina = requests.get(url)

# Preparo la sopa

sopa = BeautifulSoup(pagina.text,'html.parser')

# Extraigo los mensajes y los autores de la tabla, usando los atributos de nombre y estilo de cada celda

mensajes = sopa.find_all('td', attrs={'class': 'forumheader3', 'style': 'width:60%'})
autores = sopa.find_all('td', attrs={'class': 'forumheader3', 'style': 'width:27%; text-align:center'})

# Preparo la lista de salida

salida = []

# Extraigo los datos

for mensaje, autor in zip(mensajes, autores):
    titulo = mensaje.contents[0].string
    cuerpo = mensaje.text.replace(titulo,'')
    user = autor.contents[0].string
    linea = {'titulo': titulo, 'user': user, 'cuerpo': cuerpo}
    salida.append(linea)
    print("\nTITULO: " + titulo)
    print("USUARIO: " + user)
    print("CUERPO: " + cuerpo)

# Usando la lista "salida" genero el CSV

with open('mensajes.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['titulo', 'user', 'cuerpo']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerows(salida)