from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Redirect Links</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                color: #333;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                height: 100vh; /* Full height of the viewport */
                text-align: center;
                padding-top: 100px; /* Adjust this value to move the content lower or higher */
            }
            h1 {
                margin-bottom: 30px;
            }
            ul {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            li {
                margin: 30px 0; /* Adds vertical space between the links */
            }
            a {
                text-decoration: none;
                color: white;
                background-color: #007bff; /* Blue background color */
                padding: 10px 20px;
                border-radius: 5px;
                transition: background-color 0.3s;
            }
            a:hover {
                background-color: #0056b3; /* Darker blue on hover */
            }
        </style>
    </head>
    <body>
        <div>
            <h1>Redirect to Different Apps</h1>
            <ul>
                <li><a href="http://127.0.0.1:5000">Water Level Module</a></li>
                <li><a href="http://127.0.0.1:8000">ECS Module</a></li>
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(port=8080)
