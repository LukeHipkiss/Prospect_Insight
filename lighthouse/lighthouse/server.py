from flask import Flask
from flask_executor import Executor
from flask_shell2http import Shell2HTTP

# Flask application instance
app = Flask(__name__)

# application factory
executor = Executor(app)
shell2http = Shell2HTTP(app, executor)

shell2http.register_command(endpoint="lighthouse", command_name="runner")

# Application Runner
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
