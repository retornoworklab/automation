from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime, timedelta
import os
import sys

URL_LOGIN = "https://app2.worklabweb.com.br/index.php"
ID_LAB = os.environ.get('ID_LAB', '3769')
USUARIO = os.environ.get('USUARIO', 'Retorno')
SENHA = os.environ.get('SENHA', 'WrkLb@AutoRet0rno#2026!')

def criar_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    # Desabilitar notificações e infobars
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def calcular_data_uma_semana_atras():
    data = datetime.now() - timedelta(days=7)
    return data.strftime("%d/%m/%Y")

def esperar_elemento(driver, by, valor, tempo=10):
    return WebDriverWait(driver, tempo).until(
        EC.visibility_of_element_located((by, valor))
    )

def esperar_clicavel(driver, by, valor, tempo=10):
    return WebDriverWait(driver, tempo).until(
        EC.element_to_be_clickable((by, valor))
    )

def main():
    driver = criar_driver()
    try:
        print("Acessando página de login...")
        driver.get(URL_LOGIN)

        print("Marcando checkbox para liberar campo ID...")
        checkbox_label = esperar_clicavel(driver, By.XPATH, "/html/body/div/div/div[2]/div[1]/form/div[2]/div/label")
        checkbox_label.click()
        time.sleep(0.5)

        print("Preenchendo ID do laboratório...")
        campo_id = esperar_elemento(driver, By.XPATH, "//*[@id='new_login_cliente']")
        campo_id.click()
        campo_id.clear()
        campo_id.send_keys(ID_LAB)

        print("Preenchendo usuário...")
        campo_login = esperar_elemento(driver, By.XPATH, "//*[@id='new_login']/div[2]/input")
        campo_login.click()
        campo_login.clear()
        campo_login.send_keys(USUARIO)

        print("Preenchendo senha...")
        campo_senha = esperar_elemento(driver, By.XPATH, "//*[@id='new_login']/div[3]/input")
        campo_senha.click()
        campo_senha.clear()
        campo_senha.send_keys(SENHA)

        print("Clicando no botão Entrar...")
        botao_login = esperar_clicavel(driver, By.XPATH, "//*[@id='logar']")
        botao_login.click()

        # Tratamento do modal de aviso de senha
        try:
            modal_ok = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='OK'] | //input[@value='OK'] | //*[text()='OK']"))
            )
            modal_ok.click()
            print("Modal de aviso de senha fechado.")
            time.sleep(1)
        except TimeoutException:
            print("Nenhum modal de aviso encontrado, prosseguindo...")

        print("Aguardando menu Integrações...")
        esperar_elemento(driver, By.XPATH, "//*[@id='topo-megamenu-integracao']/div[1]/img")

        print("Abrindo menu Integrações...")
        menu_integracoes = esperar_clicavel(driver, By.XPATH, "//*[@id='topo-megamenu-integracao']/div[1]/img")
        menu_integracoes.click()

        print("Clicando em Retorno...")
        submenu_retorno = esperar_clicavel(driver, By.XPATH, "//*[@id='megamenu-integracao']/ul[1]/li[5]/ul/li[2]/a")
        submenu_retorno.click()

        data_inicio = calcular_data_uma_semana_atras()
        print(f"Preenchendo data de início: {data_inicio}")
        campo_data = esperar_elemento(driver, By.XPATH, "//*[@id='dtCadastroInicio']")
        campo_data.click()
        campo_data.clear()
        campo_data.send_keys(data_inicio)

        print("Marcando conferido...")
        checkbox_conferido = esperar_clicavel(driver, By.XPATH, "//*[@id='conferido']")
        if not checkbox_conferido.is_selected():
            checkbox_conferido.click()

        print("Marcando visto...")
        checkbox_visto = esperar_clicavel(driver, By.XPATH, "//input[@type='checkbox' and @value='Resultado Conferido']")
        if not checkbox_visto.is_selected():
            checkbox_visto.click()

        print("Enviando formulário...")
        botao_enviar = esperar_clicavel(driver, By.XPATH, "//*[@id='formWsRetornoIntegracaoCadastro']/table/tbody/tr[2]/td[5]/input")
        botao_enviar.click()

        # Aguarda um pouco para o envio ser processado (opcional)
        time.sleep(2400)
        print("Automação concluída com sucesso!")

    except Exception as e:
        print(f"Erro durante a automação: {e}")
        sys.exit(1)
    finally:
        driver.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()
