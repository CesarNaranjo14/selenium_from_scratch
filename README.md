# luo_crawlers
Crawlers para la minería de datos de bienes raíces.

## Pasos a ejecutar antes de correr el proyecto.

1) Ejecutar dentro del repositorio para instalar dependencias y ambiente virtual
```
pipenv shell
pipenv install --dev
```
2) Descargar [ChromeDriver](https://chromedriver.chromium.org/downloads) y descomprime el archivo. El driver debe de estar dentro de la ruta src/crawlers/driver/. La ruta puede ser modificada en el archivo config.json.

3) Configurar el archivo .env.sample y pasarlo a .env. El archivo .env.sample ya viene con la configuracion de selenium, se omitió el archivo config.json

4) Correr el comando para crear los pickles con las colonias/municipios:
```
flask create_pickles start
```

# Correr crawlers
```
flask crawlers start crawler_name
```
Páginas:
* inmuebles24
* icasas
* vivanuncios
* propiedades
* lamudi

### Notas
1.- Si se quiere ver el GUI (Interfaz gráfica) pasar el parametro headless: false en el archivo config.json.
