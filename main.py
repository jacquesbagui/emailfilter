from flask import Flask, render_template, request, redirect, url_for, flash
import re
import os
import pandas as pd

app = Flask(__name__)

#route index
@app.route('/', methods = ['GET'])
def index():
    data = {
        "title": "Welcome Filter Import",
        "body": "Filter Import is a simple web application that allows you to import your filters"
    }
    return render_template('index.html.j2', data = data)

# Définir la regex pour les adresses e-mail
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@app.route('/export', methods=['POST'])
def export():

    column_name = request.form['column_name']

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='Aucun fichier sélectionné')
    
    # Récupérer le fichier et vérifier s'il a une extension autorisée
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', message='Aucun fichier n\'a été sélectionné')
    if not allowed_file(file.filename):
        return render_template('index.html', message='Le fichier doit être au format XLSX ou CSV ou TXT')
    
    emails = []
    # Lire le fichier TXT
    if file and file.filename.endswith('.txt'):
        for line in file:
            email = line.decode('utf-8').strip()
            if re.findall(regex, email):
                emails.append(email)
    elif(file and file.filename.endswith('.csv')):
        # Lire le fichier CSV
        df = pd.read_csv(file)
        for email in df[column_name]:
            if isinstance(email, str):
                if re.findall(regex, email):
                    emails.append(email)
    elif(file and file.filename.endswith('.xlsx')):
        # Lire le fichier XLSX
        df = pd.read_excel(file)
        for email in df[column_name]:
            if isinstance(email, str):
                if re.findall(regex, email):
                    emails.append(email)
    
    # Supprimer les doublons de la liste d'e-mails
    emails = list(set(emails))

    domains = {"gmail": [], "yahoo": [], "hotmail": [], "outlook": [], "aol": [], "icloud": [], "msn": [], "live": [], "orange": [], "free": [], "sfr": [], "wanadoo": [], "laposte": [], "bbox": [], "gmx": [], "mail": [], "protonmail": [], "hotmail.fr": [], "hotmail.com": [], "gmail.com": [], "yahoo.fr": [], "yahoo.com": [], "outlook.fr": [], "outlook.com": [], "aol.fr": [], "aol.com": [], "icloud.com": [], "msn.com": [], "live.fr": [], "live.com": [], "orange.fr": [], "orange.com": [], "free.fr": [], "free.com": [], "sfr.fr": [], "sfr.com": [], "wanadoo.fr": [], "wanadoo.com": [], "laposte.net": [], "laposte.fr": [], "bbox.fr": [], "bbox.com": [], "gmx.fr": [], "gmx.com": [], "mail.com": [], "protonmail.com": [], "pro-domain": []}
    for email in emails:
        domain = email.split('@')[1]
        if domain in domains:
            domains[domain].append(email)
        else:
            domains["pro-domain"].append(email)

    sorted_domains = sorted(domains.items(), key=lambda x: len(x[1]), reverse=True)

    return render_template('index.html.j2', emails=emails, domains=sorted_domains)

# Fonction pour vérifier si le fichier a une extension autorisée
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'xlsx', 'csv', 'txt'}

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
