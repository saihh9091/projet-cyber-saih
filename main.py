import subprocess
import socket
from emailfinder.extractor import *
from colorama import Fore, Style

##-------------------------------------)
#(INPUT demandé à l'utilisateur
url = input(Fore.RED + "Indiquer l'URL cible : ")
print(Style.RESET_ALL)


##-------------------------------------)
# La fonction va résoudre l'url en IP afin de procéder au NMAP par la suite
def resoudre_url_en_ip(url):
    try:
        adresse_ip = socket.gethostbyname(url)
        return adresse_ip
    except socket.gaierror:
        return None

ip = resoudre_url_en_ip(url)
with open('output.txt', 'w') as f:
    if ip:
        print(Fore.BLUE+ f"L'adresse IP de {url} est {ip}")
        f.write(f"L'adresse IP de {url} est {ip}" + "\n")
    else:
        print(f"Impossible de résoudre l'adresse IP de {url}")

##-------------------------------------)
#Fonction qui va enlever les www, http://, https:// et extension .com,.fr ...
def extract_domain_name(url):
    url = url.replace("http://", "").replace("https://", "")
    domain_parts = url.split('.')
    if len(domain_parts) < 2:
        return None

    if domain_parts[0] == 'www':
        domain_parts = domain_parts[1:]

    return domain_parts[0]

clean_domain_name = extract_domain_name(url)
print("Recherche des employés " + clean_domain_name)

##-------------------------------------)
#La fonction va ouvrir NMAP avec la library subprocess afin de demander à l'OS de lancer en parallèle un scan
def nmap():
    print(Style.RESET_ALL)
    print("\n"+"Lancement du scan NMAP, cela peux prendre quelques instants")
    commande = ["nmap", "-sV", url]
    with open('output.txt', 'a') as f:
        f.write('\n'+"Lancement du scan NMAP"+'\n')
        resultat_nmap = subprocess.run(commande, text=True, check=True, stdout=f)

    print("Le scan NMAP est terminé, vous trouverez le résultat du scan dans le rapport qui sera envoyé par mail")

##-------------------------------------)

#Fonction qui va faire du scrapping / dorking pour trouver des employés du domaine visé
def google_dork(clean_domain_name):
    import requests
    from bs4 import BeautifulSoup
    query = "site:linkedin.com/in AND " + clean_domain_name
    url = "https://www.google.com/search?q=" + query
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de la requête: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = []

    for g in soup.find_all('div', class_='tF2Cxc'):
        title_element = g.find('h3')
        if title_element:
            title = title_element.text
        else:
            title = "Titre non disponible"
        link = g.find('a')['href']
        search_results.append((title, link))

    try:
        for title, link in results:
            print(title)
            print(link)
            print()
    except:
        pass

    return search_results

#Print les personnes sur linkedin
results = google_dork(clean_domain_name)
for title, link in results:
    with open('output.txt', 'a') as f:
        f.write(title + "\n")
        f.write(link + "\n")
        f.write("")
    print(title)
    print(link)
    print("")

##-------------------------------------)
# La fonction va chercher des mails à partir du domaine sur google, bing et baidu
def search_mail():
    try : 
        result_google = get_emails_from_google(url)
        result_bing = get_emails_from_bing(url)
        result_baidu = get_emails_from_baidu(url)
        with open("output.txt", 'a') as f:
            f.write(''+'\n')
            print("")
            f.write("Les mails pour le domaines " + url + '\n' )
            f.write("-"*30 + '\n')
            print("Les mails pour le domaines " + url + '\n' )
            for i in result_google:
                print(Fore.YELLOW + i)
                f.write(i+'\n')
            for i in result_bing:
                print(i)
                f.write(i+'\n')
            for i in result_baidu:
                print(i)
                f.write(i+'\n')
    except:
        print("Le module search_mail() n'a pas fonctionné")
        pass
print(Style.RESET_ALL)
##-------------------------------------)

#La fonction à pour but d'envoyer le mail avec le rapport en pièce jointes
def envoyer_email(destinataire, sujet, corps, expediteur, mot_de_passe):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    try:
        # Création de l'e-mail
        message = MIMEMultipart()
        message['From'] = expediteur
        message['To'] = destinataire
        message['Subject'] = sujet

        # Corps du message
        message.attach(MIMEText(corps, 'plain'))

        # Pièce jointe
        fichier_piece_jointe = 'output.txt'
        piece_jointe = open(fichier_piece_jointe, 'rb')

        mime_base = MIMEBase('application', 'octet-stream')
        mime_base.set_payload(piece_jointe.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', 'attachment', filename=fichier_piece_jointe)

        message.attach(mime_base)
        piece_jointe.close()

        # Connexion au serveur SMTP de Gmail
        serveur_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        serveur_smtp.starttls()
        serveur_smtp.login(expediteur, mot_de_passe)

        # Envoi de l'e-mail
        serveur_smtp.sendmail(expediteur, destinataire, message.as_string())

        # Déconnexion du serveur SMTP
        serveur_smtp.quit()

        print("L'e-mail a été envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {str(e)}")

##-------------------------------------)
#(Lancement des fonctions)
search_mail()
nmap()


##-------------------------------------)
#(Finalisation du script et envoi)
destinataire = input("Indiquer votre email pour obtenir le rapport complet : ")
sujet = 'Rapport scan - Hossein Saihi'
corps = 'Bonjour, vous trouverez le rapport du scan en PJ'
expediteur = 'saihh9091@gmail.com'
mot_de_passe = 'hgoypyzvbipnhnaa'




