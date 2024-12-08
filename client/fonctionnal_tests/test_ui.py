from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore

#Fonction pour tester la connexion
def test_login () :
    
    # Initialise le driver sur Google Chrome (navigateur disponible)
    driver = webdriver.Chrome()

    # Essaye de se connecter
    try :
        
        # Ouvrir la page de connexion
        driver.get("http://localhost:8000/login")

        # Saisir l'email et le mot de passe
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        # Entrer une adresse mail et un mot de passe valide
        email_field.send_keys("user@example.com")
        password_field.send_keys("correct_password")

        # Cliquer sur le bouton de connexion
        login_button = driver.find_element(By.ID, "login")
        login_button.click()

        # Attendre la redirection vers la page dashboard
        WebDriverWait(driver, 10).until(EC.url_to_be("http://localhost:8000/dashboard"))

        # Vérifie la bonne redirection
        assert driver.current_url == "http://localhost:8000/dashboard"

        # Vérifie la présence du token d'authentification
        token = driver.get_cookie("auth_token")
        assert token is not None, "Token d'authentification non trouvé."
    
    # Gére les exceptions en affichant un message d'erreur
    except Exception as exception :
        
        print(f"Une erreur s'est produite : {exception}")
    
    # Quitte la connexion
    finally:
        
        driver.quit()