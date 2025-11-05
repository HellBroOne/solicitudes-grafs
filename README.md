# Iniciar el Proyecto

Sigue estos pasos para levantar y ejecutar el proyecto:

1. **Levanta los contenedores en segundo plano:**
    ```bash
    docker compose up -d
    ```

2. **Verifica que los servicios estén corriendo:**
    ```bash
    docker compose ps
    ```

3. **Accede al contenedor de la aplicación:**
    ```bash
    docker compose exec app bash
    ```

4. **Navega al directorio del proyecto:**
    ```bash
    cd solicitudes
    ```

5. **Inicia el servidor de desarrollo de Django:**
    ```bash
    python manage.py runserver 0:8000
    ```

6. **Para detener y eliminar los contenedores:**
    ```bash
    docker compose down
    ```
