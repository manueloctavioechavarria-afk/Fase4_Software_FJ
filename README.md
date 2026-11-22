# Software FJ – Sistema de Gestión de Clientes, Servicios y Reservas

**Universidad Nacional Abierta y a Distancia (UNAD)**  
**Curso:** Programación (213023) – Fase 4: Prácticas simuladas  
**Estudiante:** Manuel Octavio Echavarria Granados  
**Grupo:** 213023_228

## Descripción del proyecto

Este programa simula la administración de clientes, servicios y reservas de una empresa denominada **Software FJ**. Fue desarrollado en Python para practicar la programación orientada a objetos y el manejo de excepciones. No utiliza bases de datos: los clientes, los servicios y las reservas se almacenan temporalmente en listas.

El sistema permite registrar clientes y trabajar con tres tipos de servicios: **reserva de salas**, **alquiler de equipos** y **asesorías especializadas**. También permite confirmar o cancelar reservas y calcular costos con descuentos e impuestos opcionales.

## Archivos del repositorio

| Archivo | Función |
| --- | --- |
| `Sistema_Software_FJ_Fase4.py` | Contiene las clases del sistema y ejecuta las 18 operaciones de prueba. |
| `registro_software_fj.txt` | Conserva un ejemplo de los mensajes de éxito, eventos y errores generados al ejecutar el programa. |
| `README.md` | Explica el objetivo del proyecto, sus funciones y cómo ejecutarlo. |

## Cómo ejecutar el programa

1. Tener Python instalado en el computador.
2. Descargar el archivo `Sistema_Software_FJ_Fase4.py` y abrirlo con Visual Studio Code.
3. Seleccionar **Run Python File** o ejecutar en la terminal:

```bash
python Sistema_Software_FJ_Fase4.py
```

4. Revisar en la terminal el resultado de las **18 operaciones**.
5. Abrir `registro_software_fj.txt` en la carpeta desde la que se ejecutó el programa para consultar los registros.

No necesita instalar bibliotecas externas. Cada ejecución puede agregar nuevas líneas al archivo de registros.

## Organización del código

| Clase o función | Función principal |
| --- | --- |
| `Entidad` | Clase abstracta que define el método `descripcion()`. |
| `Cliente` | Almacena y valida nombre, identificación y correo electrónico. |
| `Servicio` | Clase abstracta de la que heredan los tres servicios. |
| `ServicioSala` | Valida la capacidad y calcula el costo de una sala. |
| `ServicioEquipo` | Valida la cantidad y calcula el alquiler de equipos. |
| `ServicioAsesoria` | Valida la especialidad y calcula el costo de una asesoría. |
| `Reserva` | Permite confirmar, procesar y cancelar una reserva. |
| `SistemaSoftwareFJ` | Administra listas de clientes, servicios y reservas. |
| `guardar_registro()` | Escribe eventos y errores en un archivo de texto. |

## Requisitos aplicados en la Fase 4

| Concepto | Aplicación en este proyecto |
| --- | --- |
| Abstracción | Clases abstractas `Entidad` y `Servicio`. |
| Herencia | Los tres tipos de servicios heredan de `Servicio`. |
| Polimorfismo | Cada servicio sobrescribe `descripcion()`, `validar_parametros()` y `calcular_costo()`. |
| Encapsulación | Los datos se almacenan en atributos con guion bajo y se consultan mediante métodos. |
| Sobrecarga simulada | Los métodos de cálculo utilizan parámetros opcionales para descuentos e impuestos. |
| Excepciones personalizadas | `ErrorSistema`, `DatoInvalidoError`, `ServicioNoDisponibleError` y `OperacionNoPermitidaError`. |
| Control de errores | Uso de `try`, `except`, `else` y `finally`. |
| Encadenamiento de excepciones | Uso de `raise ... from error` al convertir datos inválidos. |
| Registro de eventos | Archivo `registro_software_fj.txt`. |
| Simulación | 18 operaciones válidas e inválidas, por encima del mínimo solicitado de 10. |

## Resultados de las pruebas

La simulación registra **2 clientes válidos**, crea **3 servicios válidos** y genera **5 reservas**: 3 quedan confirmadas, 1 cancelada y 1 fallida. También prueba nombres vacíos, correos incorrectos, identificaciones duplicadas, tarifas y capacidades inválidas, una duración escrita con letras, un servicio no disponible y una cancelación repetida.

La última operación confirma una nueva reserva después de que ocurrieron errores controlados. Esto permite comprobar que el programa continúa ejecutándose.

## Observación académica

Este repositorio corresponde a un aporte desarrollado individualmente en el marco de una actividad planteada como colaborativa.
