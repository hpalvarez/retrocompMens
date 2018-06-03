from bs4 import BeautifulSoup
import requests

pagina = requests.get('http://www.retrocomputacion.com/e107_plugins/forum/forum_latest.php?150')

sopa = BeautifulSoup(pagina.text,'html.parser')

mensajes = sopa.find_all('td', attrs={'class': 'forumheader3', 'style': 'width:60%'})
autores = sopa.find_all('td', attrs={'class': 'forumheader3', 'style': 'width:27%; text-align:center'})

for mensaje, autor in zip(mensajes, autores):
    titulo = mensaje.contents[0].string
    cuerpo = mensaje.text.replace(titulo,'')
    user = autor.contents[0].string
    print("\nTITULO: " + titulo)
    print("USUARIO: " + user)
    print("CUERPO: " + cuerpo)