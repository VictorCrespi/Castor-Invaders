import os
import sys

# Añadir el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.main import main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error al iniciar el juego: {e}")
        input("Presiona Enter para salir...") 