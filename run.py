# run.py
from app import app
from layout import get_layout
import callbacks  # registra los callbacks

app.layout = get_layout()

if __name__ == '__main__':
    app.run(port=8052)

