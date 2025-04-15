import webbrowser
import os

def open_app():
    file_path = os.path.abspath('example.html')
    webbrowser.open('file://' + file_path)

if __name__ == '__main__':
    open_app()