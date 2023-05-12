#!/bin/bash

apt-get update
apt-get install nmap -y
apt-get install python3 -y
apt-get install python3-pip -y

# Installer les modules PIP
pip install emailfinder
pip install requests
pip install colorama
pip install bs4

# Vérifier si l'installation a réussi
if [ $? -eq 0 ]
then
    echo "Les module ont étés installés avec succès."
else
    echo "Une erreur est survenue lors de l'installation des modules."
fi