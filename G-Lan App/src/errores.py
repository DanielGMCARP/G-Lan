class UsuarioNoEncontradoError(Exception):
    """Excepción personalizada para usuario no encontrado."""
    def __init__(self, mensaje="Usuario no encontrado. Por favor, regístrese."):
        super().__init__(mensaje)
        
class ContraseñaIncorrectaError(Exception):
    """Excepción personalizada para contraseña incorrecta."""
    def __init__(self, mensaje="Contraseña incorrecta. Por favor, inténtelo de nuevo."):
        super().__init__(mensaje)

class JuegoNoEncontradoError(Exception):
    """Excepción personalizada para juego no encontrado."""
    def __init__(self, mensaje="El juego no existe en el catálogo o no lo ha comprado."):
        super().__init__(mensaje)

class JuegoYaDescargadoError(Exception):
    """Excepción personalizada para juego ya descargado."""
    def __init__(self, mensaje="El juego ya ha sido descargado."):
        super().__init__(mensaje)

class IDInvalidoError(Exception):
    """Excepción personalizada para ID inválido."""
    def __init__(self, mensaje="ID inválido. Por favor, ingrese un número válido."):
        super().__init__(mensaje)

class JuegoYaCompradoError(Exception):
    """Excepción personalizada para juego ya comprado."""
    def __init__(self, mensaje="El juego ya ha sido comprado."):
        super().__init__(mensaje)
