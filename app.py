from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("q", "").lower()

    results = []

    if "admin" in query or "internal" in query or "document" in query:
        results.append({
            "title": "Internal Documentation",
            "description": "Internal documentation for authorized personnel.",
            "url": "/internal-docs/7f3a92?file=",
            "type": "internal"
        })

    if "user" in query:
        results.append({
            "title": "User Profile",
            "description": "View and edit your user profile.",
            "url": "/documents/user",
            "type": "page"
        })

    if "settings" in query:
        results.append({
            "title": "Settings",
            "description": "Configure your application settings.",
            "url": "/documents/settings",
            "type": "page"
        })

    return {
        "query": query,
        "results": results
    }

@app.route("/documents/user")
def user():
    return render_template(
        "documents.html",
        title="User Documents",
        files=[
            "photo1.jpg"
        ]
    )
@app.route("/documents/settings")
def settings():
    return render_template(
        "settings.html",
        title="Application Settings",
        settings=[
            {
                "name": "Theme",
                "value": "Light"
            },
            {
                "name": "Language",
                "value": "English"
            },
            {
                "name": "Notifications",
                "value": "Enabled"
            },
            {
                "name": "Session Timeout",
                "value": "30 minutes"
            }
        ],
        system_info={
            "Application": "Internal Document Portal",
            "Environment": "Production",
            "Configuration": "Managed by administrator"
        }
    )

@app.route("/documents/admin")
def admin():
    return render_template(
        "documents.html",
        title="Administration Documents",
        files=[
            "secret_file.txt",
            "flag.txt"
        ]
    )

@app.route("/documents/<directory>/<filename>")
def document_file(directory, filename):
    return send_from_directory(
        f"/app/documents/{directory}",
        filename
    )

@app.route("/internal-docs/7f3a92")
def internal_document():
    file_path = request.args.get("file")

    if not file_path:
        return {
            "title": "Internal Documentation",
            "content": "No document specified."
        }

    try:
        base_path = "/app/documents"
        full_path = os.path.join(base_path, file_path)

        if os.path.isabs(file_path):
            return {"error": "Invalid file path"}, 400

        with open(full_path, "r") as file:
            content = file.read()

        return {
            "title": "Internal Documentation",
            "content": content
        }

    except Exception as error:
        return {
            "error": str(error)
        }, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)