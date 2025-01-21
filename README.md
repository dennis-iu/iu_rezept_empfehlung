<center>Projektpräsentation Rezept-Empfehlungs-Anwendung</center>  
<center>DLBSEPPSD01_D - Projekt: Software Development</center>  
<center>Aufgabenstellung 3 -  Entwicklung einer sonstigen Anwendung</center>  

**Voraussetzungen:**  
- Python 3.x
- Standardbrowser hinterlegt (für open_link funktion)
- ggf. make  

**Einrichtung mit make:**  
 - make prepare in der Konsole ausführen  
   
**Einrichtung ohne make:**  
 - virtuelle Python Umgebung erzeugen:  
    python3 -m venv venv  
 - virtuelle Umgebung aktivieren:  
    Windows -> venv\Scripts\activate  
    Linux/Mac -> source venv/bin/activate  
 - Abhängigkeiten aus der requirements.txt installieren:  
    pip install -r requirements.txt  
  
**Aufbau des Projektes:**  
<div align="center">
  <img src="readme_assets/klassendiagramm.png" alt="Klassendiagramm">
</div>

**Nutzung des Projektes:**  
1. Ausführen der main.py  
<div align="center">
  <img src="readme_assets/recipe_startui.png" alt="startui">
</div>

2. Über den Start Button zur Key_Entry Seite gelangen (nur beim ersten mal)
<div align="center">
  <img src="readme_assets/recipe_key_entryui.png" alt="key_entryui">
</div>  

3. Mit dem Key Bekommen Button zur Login Seite der Spoonacular API gelangen  
<div align="center">
  <img src="readme_assets/spoonacularapi_signup.png" alt="spoonacularapi_signup">
</div>

4. Account erstellen und zur Profile Seite navigieren  
<div align="center">
  <img src="readme_assets/spoonacularapi_profile.png" alt="spoonacularapi_profile">
</div>

5. Angezeigten Api Key in die Key_Entry Seite einfügen und zur Search Seite gelangen  
<div align="center">
  <img src="readme_assets/recipe_searchui.png" alt="searchui">
</div> 

6. Individuelle Parameter auf der Search Seite angeben  
<div align="center">
  <img src="readme_assets/recipe_searchui_example.png" alt="searchui_example">
</div> 

7. Über Enter Button das Ergebnis anzeigen lassen 
<div align="center">
  <img src="readme_assets/recipe_resultui.png" alt="resultui">
</div>  

8. Über Rezept Button zum Rezept kommen  
<div align="center">
  <img src="readme_assets/spoonacularapi_recipe_example.png" alt="spoonacularapi_recipe_example">
</div>

8. Nächste Anfrage über den zurück oder reload Button der recipe Seite ausführen  

**Zusatzinfos:**  
 - Der Reload Button zeigt immer das nächst passendste Ergebnis zur vorherigen Anfrage an
 - Die Närhwert-Angaben sind pro Portion
 - Eingaben können auf deutsch erfolgen (wird für die Api übersetzt)
 - Die Ergebnisseite kann ebenfalls über den Browser übersetzt werden