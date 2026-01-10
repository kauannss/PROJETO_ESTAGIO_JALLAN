import selenium
import time 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


## manipulação de dados 
    #lendo o arquivo csv
df = pd.read_csv("dados.csv")

    # tratando o arquivo csv
df_novo = df[["Código", "Descrição", "NCM_Correto"]]


df_novo.loc[:, "Código"] = df_novo["Código"].astype(str)
df_novo.loc[:, "NCM_Correto"] = df_novo["NCM_Correto"].str.replace(".", "", regex=False)


## fazer o login no site
    # abrir navegador
navegador = webdriver.Chrome()

    # colocar navergador em tela cheia
navegador.maximize_window()

    # abrir site na tela de login
navegador.get("https://zweb.com.br/#/sign-in")

    # selecionar elementos e passar os dados para login 
        #email
navegador.find_element("class name", "form-control").send_keys("")

        #senha
navegador.find_element("xpath", "/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/input").send_keys("")

button_entrar = navegador.find_element("xpath", "/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/div[4]/button")

    # clicar no botao entrar
button_entrar.click()


espera10 = WebDriverWait(navegador, 10)
espera = WebDriverWait(navegador, 30)
espera.until(EC.presence_of_element_located(("xpath", "/html/body/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/a/span/span")))

## operação de cadastramento dos itens 

    #abrindo modulo de produtos
navegador.get("https://zweb.com.br/#/register/stock/product")

## criando o loop para edição dos produtos
for index, row in df_novo.iterrows():
    cod = row["Código"]
    desc = row["Descrição"]
    ncm = row["NCM_Correto"]
    
    # espera do search
    espera.until(EC.presence_of_element_located(("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/thead/tr/div/div/div[3]/div[1]/div[1]/div/div/input")))

    search = navegador.find_element("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/thead/tr/div/div/div[3]/div[1]/div[1]/div/div/input")

    search.send_keys(cod + Keys.ENTER)

    # espera do edit 
    espera.until(EC.presence_of_element_located(("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div[10]/a[1]")))

    # clicando no edit
    navegador.find_element("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div[10]/a[1]").click()

    # esperar a tela de carregamento abrir para clicar no modulo fiscal
    espera.until(EC.presence_of_element_located(("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/form/div[2]/div/div[1]/button")))

    time.sleep(1)

    navegador.find_element("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/form/div[2]/div/div[1]/button").click()

    time.sleep(2)

    #esperar a barra do ncm ser liberada
    espera.until(EC.presence_of_element_located(("id", "product.fiscal.produto.NCM")))

    barra_ncm = navegador.find_element("id", "product.fiscal.produto.NCM")

    # edita o ncm
    barra_ncm.send_keys(ncm)
    time.sleep(2)

    try:
        espera10.until(EC.presence_of_element_located(("id", "product.fiscal.produto.NCM-0")))

        navegador.find_element("id", "product.fiscal.produto.NCM-0").click()

    except TimeoutException:
        # elemento não existe → ignora o click
        pass

        # salva 
    navegador.find_element("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/footer/div/div/button[4]").click()



    

time.sleep(10)