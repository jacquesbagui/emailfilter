from flask import Flask, render_template, request, redirect, url_for, flash
import re
import os

app = Flask(__name__)

#route index
@app.route('/', methods = ['GET'])
def index():
    data = {
        "title": "Welcome Filter Import",
        "body": "Filter Import is a simple web application that allows you to import your filters"
    }
    return render_template('index.html.j2', data = data)

@app.route('/export', methods=['POST'])
def export():
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='Aucun fichier sélectionné')
    if file and file.filename.endswith('.txt'):
        # Lire le fichier TXT
        emails = []
        for line in file:
            email = line.decode('utf-8').strip()
            if re.match(r'^[\w\-\.]+@[\w\-\.]+\.[a-zA-Z]{2,}$', email):
                emails.append(email)

        domains = {"gmail": [], "yahoo": [], "hotmail": [], "outlook": [], "aol": [], "icloud": [], "msn": [], "live": [], "orange": [], "free": [], "sfr": [], "wanadoo": [], "laposte": [], "bbox": [], "gmx": [], "mail": [], "protonmail": [], "hotmail.fr": [], "hotmail.com": [], "gmail.com": [], "yahoo.fr": [], "yahoo.com": [], "outlook.fr": [], "outlook.com": [], "aol.fr": [], "aol.com": [], "icloud.com": [], "msn.com": [], "live.fr": [], "live.com": [], "orange.fr": [], "orange.com": [], "free.fr": [], "free.com": [], "sfr.fr": [], "sfr.com": [], "wanadoo.fr": [], "wanadoo.com": [], "laposte.net": [], "laposte.fr": [], "bbox.fr": [], "bbox.com": [], "gmx.fr": [], "gmx.com": [], "mail.com": [], "protonmail.com": [], "pro-domain": []}
        for email in emails:
            domain = email.split('@')[1]
            if domain in domains:
                domains[domain].append(email)
            else:
                domains["pro-domain"].append(email)

        sorted_domains = sorted(domains.items(), key=lambda x: len(x[1]), reverse=True)

        return render_template('index.html.j2', emails=emails, domains=sorted_domains)
    else:
        flash("Le fichier n'est pas valide, assurez-vous qu'il est au format .txt.")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
