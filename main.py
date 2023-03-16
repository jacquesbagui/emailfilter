from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import re
import os
from collections import defaultdict
import pandas as pd
import csv

app = Flask(__name__)

# Définir la regex pour les adresses e-mail
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

LIST_DOMAINES = {"gmail", "yahoo", "hotmail", "outlook", "aol", "icloud", "msn", "live", "orange", "free", "sfr", "wanadoo", "laposte", "bbox", "gmx", "mail", "protonmail", "hotmail.fr", "hotmail.com", "gmail.com", "yahoo.fr", "yahoo.com", "yahoo.in", "outlook.fr", "outlook.com", "outlook.in", "outlook.om", "aol.fr", "aol.com", "icloud.com", "msn.com", "live.co", "live.in", "live.fr", "live.com", "orange.fr", "orange.com", "free.fr", "free.com", "sfr.fr", "sfr.com", "wanadoo.fr", "wanadoo.com", "laposte.net", "laposte.fr", "bbox.fr", "bbox.com", "gmx.fr", "gmx.com","yahoo.co.uk" , "yahoo.co.in" , "gmail.in", "gmail.co", "mail.com", "protonmail.com", "pro-domain"}
emails = []

def read_xlsx(file):
    global emails
    df = pd.read_excel(file, engine='openpyxl')
    emails += df['email'].tolist()

def read_csv(file):
    global emails
    df = pd.read_csv(file)
    emails += df['email'].tolist()
    print(f"Nombre d'emails lus depuis {file.filename}: {len(df)}")
    print(f"Les emails extraits de {file.filename}: {emails}")

def read_txt(file):
    global emails
    with open(file) as f:
        emails += f.read().splitlines()
    print(f"Nombre d'emails lus depuis {file.filename}: {len(emails)}")
    print(f"Les emails extraits de {file.filename}: {emails}")


def parse_csv(file):
    _, ext = os.path.splitext(file.filename)
    if ext == '.xlsx':
        read_xlsx(file)
    elif ext == '.csv':
        read_csv(file)
    elif ext == '.txt':
        read_txt(file, sep='\t')
    else:
        raise ValueError('Format de fichier invalide')

def group_by_domain(emails):
    domains = defaultdict(set)
    for email in emails:
         if re.findall(regex, email):
            domain = email.split('@')[1].lower()
            if domain in LIST_DOMAINES:
                domains[domain].add(email.lower())
            else:
                domains['pro'].add(email.lower())
    return domains

#route index
@app.route('/', methods=['GET', 'POST'])
def index():
    global emails
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html.j2', error='Aucun fichier sélectionné')
        
        # Récupérer le fichier et vérifier s'il a une extension autorisée
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html.j2', message='Aucun fichier n\'a été sélectionné')
        if not allowed_file(file.filename):
            return render_template('index.html.j2', message='Le fichier doit être au format XLSX ou CSV ou TXT')
        
        parse_csv(file)
        domains = group_by_domain(emails)
        return render_template('download.html.j2', domains=domains)
    else:
        return render_template('index.html.j2')

@app.route('/download/<domain>', methods=['GET'])
def download(domain):
    global emails

    filename = f"{domain}.txt"

    if domain == 'pro':
        domain_emails = list(group_by_domain(emails)['pro'])
        print(domain_emails)
        with open(filename, 'w') as f:
            for line in domain_emails:
                f.write(line)
                f.write('\n')
    else:
        domain_emails = list(group_by_domain(emails)[domain])
        print(domain_emails)
        with open(filename, 'w') as f:
            for line in domain_emails:
                f.write(line)
                f.write('\n')
    return send_file(filename, as_attachment=True)

# Fonction pour vérifier si le fichier a une extension autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'csv', 'txt'}

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
