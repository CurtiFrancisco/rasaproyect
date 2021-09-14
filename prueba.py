import requests
url = 'https://api-dolar-argentina.herokuapp.com/api/dolaroficial'
r = requests.get(url)
datos = r.json()
p_d_compra = datos['compra']
p_d_venta = datos['venta']

print(p_d_compra)