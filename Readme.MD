La manera automática de iniciar el proyecto:

chmod +x setup_hooks.py
./setup_hooks.py


La manera manual:

1.	Crear un Directorio de Hooks Global:
Crea un directorio en tu sistema donde almacenarás los hooks globales. Por ejemplo:

```
mkdir -p ~/.git-templates/hooks
```

2.	Configurar Git para Usar la Plantilla de Hooks Global:
Configura Git para que utilice este directorio como plantilla para hooks:

```
git config --global init.templateDir '~/.git-templates'
```

3.  Crear el Hook commit-msg en el Directorio Global de Hooks:
Crea un archivo commit-msg en el directorio ~/.git-templates/hooks/:
```
nano ~/.git-templates/hooks/commit-msg
```

4. Añadir el Contenido del Hook:
Copia el siguiente script en el archivo commit-msg para que invoque tu script Python:

´´´
#!/bin/bash
# Archivo de hook commit-msg

# La ruta a tu script Python
SCRIPT_PATH="/ruta/al/Main.py"

# Obtener el archivo temporal que contiene el mensaje del commit
COMMIT_MSG_FILE="$1"

# Leer el mensaje del archivo temporal
COMMIT_MSG=$(<"$COMMIT_MSG_FILE")

# Ejecutar el script Python con el mensaje del commit
MODIFIED_MSG=$(python3 "$SCRIPT_PATH" --message "$COMMIT_MSG" --test)

# Reemplazar el mensaje en el archivo temporal si el script Python devolvió un mensaje modificado
if [ "$COMMIT_MSG" != "$MODIFIED_MSG" ]; then
    echo "$MODIFIED_MSG" > "$COMMIT_MSG_FILE"
fi
```

5. Hacer el Hook Ejecutable:
Asegúrate de que el archivo commit-msg sea ejecutable:

´´´
chmod +x ~/.git-templates/hooks/commit-msg
```

Aplicar el Hook a Repositorios Existentes
´´´
cp ~/.git-templates/hooks/commit-msg /ruta/a/tu/repositorio/.git/hooks/
```