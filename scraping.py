import requests
from bs4 import BeautifulSoup

# URL de la page principale à scraper
url_principale = "https://entreprises.lefigaro.fr/recherche?q=ordre+infirmier"

response = requests.get(url_principale)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # Filtrer uniquement les balises <a> pertinentes
    links = [a for a in soup.find_all('a', href=True) if 'entreprise' in a['href'] and 'Conseil' in a.text]
    
    conseil_noms = []  # Liste pour les noms des conseils
    codes_postaux = []  # Liste pour les codes postaux
    sirens = []  # Liste pour les numéros SIREN
    sirets = []  # Liste pour les numéros SIRET
    
    for a in links:
        conseil_url = a['href']
        conseil_nom = a.text.strip()  # Extraire le nom du "Conseil"
        detail_response = requests.get(conseil_url)
        if detail_response.status_code == 200:
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
            
            siren = detail_soup.find("dt", string=lambda text: "Siren" in text if text else False)
            siren = siren.find_next_sibling("dd").text.strip() if siren else "Non trouvé"
            
            siret = detail_soup.find("dt", string=lambda text: "Siret" in text if text else False)
            siret = siret.find_next_sibling("dd").text.strip() if siret else "Non trouvé"
            
            # Extraction du code postal depuis le nom du conseil
            code_postal = conseil_nom.split(" ")[-1].strip('()')
            
            conseil_noms.append(conseil_nom)
            codes_postaux.append(code_postal)
            sirens.append(siren)
            sirets.append(siret)
            
            print(f"Conseil: {conseil_nom}, Code Postal: {code_postal}, SIREN: {siren}, SIRET: {siret}")
    
    # Vous pouvez maintenant utiliser les listes conseil_noms, codes_postaux, sirens et sirets comme vous le souhaitez.
else:
    print("Échec de la requête HTTP à la page principale, statut:", response.status_code)
   

# Créer un dictionnaire à partir des listes
data = {
    'Conseil': conseil_noms,
    'Code Postal': codes_postaux,
    'SIREN': sirens,
    'SIRET': sirets
}

# Créer un DataFrame à partir du dictionnaire
df = pd.DataFrame(data)

# Afficher le DataFrame
print(df)

df.to_csv('conseils_infirmiers.csv', index=False)
 
