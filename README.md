🕵️ Generador de Google Dorks Avanzado

Herramienta de Recopilación de Datos Pasiva
Este proyecto proporciona una interfaz gráfica intuitiva para construir consultas especializadas utilizando Google Dorks. Estas búsquedas aprovechan operadores avanzados de Google para encontrar información pública pero potencialmente sensible, como archivos expuestos, paneles de administración o datos personales indexados.

🛠️ Requisitos
Instala las dependencias necesarias con pip:
pip install requests beautifulsoup4

🎯 Funcionalidades Principales
Interfaz gráfica basada en Tkinter.
Selección de operadores Google Dork con descripciones.
Generación automática de dorks personalizados.
Copia al portapapeles, guardado en archivo y apertura directa en Google.
Extracción de resultados desde Google (títulos solamente).
Módulo de ayuda con ejemplos útiles.

🔍 Recopilación de Datos Pasiva
Esta herramienta realiza búsquedas en Google y analiza resultados públicos indexados:
No interactúa con los servidores objetivo.
No ejecuta escaneos ni pruebas de penetración.
Sí es útil para OSINT y reconocimiento previo.

🧩 Operadores Compatibles
Operador  Descripción
site:     Buscar en un dominio específico
inurl:    Palabra clave en la URL
intitle:  Palabra clave en el título
intext:   Palabra clave en el contenido del texto
filetype: Buscar tipos de archivo (xls, doc, pdf...)
ext:      Extensión de archivo
cache:    Ver versión en caché de una página
link:     Páginas que enlazan a otra
related:  Páginas similares
"..."     Coincidencia exacta
OR        Búsqueda con operador lógico OR
-         Excluir palabra
*         Comodín

🧪 Ejemplo de Uso
Marca site: e ingresa gov.
Marca filetype: e ingresa xls.
Marca inurl: e ingresa contact.
Generará el siguiente dork:
site:gov filetype:xls inurl:contact
Ideal para encontrar hojas de cálculo públicas con datos de contacto.

💾 Guardado y Portabilidad
Guarda dorks en archivos .txt.
Copia al portapapeles.
Ejecuta búsquedas directamente en Google desde la aplicación.

🛡️ Aviso de Uso Ético
Esta herramienta está diseñada para fines educativos y de auditoría autorizada. El uso indebido puede violar leyes locales o políticas de privacidad. Únicamente debe usarse en contextos legales y con consentimiento.

📎 Licencia
  Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

📌 Créditos
Desarrollado en Python 3 usando bibliotecas estándares como tkinter, requests, y beautifulsoup4.
