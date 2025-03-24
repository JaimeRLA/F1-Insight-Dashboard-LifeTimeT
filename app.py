from dash import Dash, html, dcc
from layout import get_layout

app = Dash(__name__)
app.title = "F1 Full Dashboard"
app.layout = get_layout()

if __name__ == '__main__':
    app.run(debug=True)
