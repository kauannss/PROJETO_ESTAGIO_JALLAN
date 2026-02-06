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
df = pd.read_csv("dados2.csv", sep=";")


df_novo = df[["Produto", "Valor", "NCM", "CSOSN"]]

df_novo.loc[:, "NCM"] = df_novo["NCM"].str.replace(".", "", regex=False)
df_novo.loc[:, "Valor"] = df_novo["Valor"].astype(str)
df_novo.loc[:, "Produto"] = df_novo["Produto"].astype(str)
df_novo.loc[:, "CSOSN"] = df_novo["CSOSN"].astype(str)




## fazer o login no site
    # abrir navegador
navegador = webdriver.Chrome()

    # colocar navergador em tela cheia
navegador.maximize_window()

    # abrir site na tela de login
navegador.get("https://zweb.com.br/#/sign-in")

    # selecionar elementos e passar os dados para login 
        #email
navegador.find_element("class name", "form-control").send_keys(input("QUAL O EMAIL DO CLIENTE: "))

        #senha
navegador.find_element("xpath", "/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/input").send_keys(input("QUAL A SENHA DO CLIENTE: "))

button_entrar = navegador.find_element("xpath", "/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/div[4]/button")

    # clicar no botao entrar
button_entrar.click()


espera10 = WebDriverWait(navegador, 10)
espera = WebDriverWait(navegador, 50)
espera.until(EC.presence_of_element_located(("xpath", "/html/body/div[1]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/a/span/span")))

## operação de cadastramento dos itens 

    #abrindo modulo de produtos
navegador.get("https://zweb.com.br/#/register/stock/product")

## criando o loop para edição dos produtos
for index, row in df_novo.iterrows():
    desc = row["Produto"]
    ncm = row["NCM"]
    value = row["Valor"]
    origem = "0"
    csosn_c = row["CSOSN"]
    csosn_nc = row["CSOSN"]
    
    # espera do search
    espera.until(EC.presence_of_element_located(("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div/thead/tr/div/div/div[3]/div[1]/div[1]/div/div/input")))

    # clicando no botão de cadastro
    cadastro = navegador.find_element("id", "grid.primaryButton")

    cadastro.click()

    # digitando descrição
    espera.until(EC.presence_of_element_located(("id", "product.description")))

    navegador.find_element("id", "product.description").send_keys(desc)
    # digitando valor
    navegador.find_element("id", "product.price").send_keys(value)


    # esperar a tela de carregamento abrir para clicar no modulo fiscal
    espera.until(EC.presence_of_element_located(("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/form/div[2]/div/div[1]/button")))

    time.sleep(1)

    navegador.find_element("xpath", "/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/form/div[2]/div/div[1]/button").click()

    time.sleep(2)

    #espera para cadastramento
    espera.until(EC.presence_of_element_located(("id", "product.fiscal.produto.NCM")))

    ### cadastramento fiscal
    # cadastro origem
    navegador.find_element("id", "product.fiscal.produto.origem").send_keys(origem)

    try:
        espera10.until(EC.presence_of_element_located(("id", "product.fiscal.produto.origem-0")))

        navegador.find_element("id", "product.fiscal.produto.origem-0").click()

    except TimeoutException:
        # elemento não existe > ignora o click
        pass

    # cadastro csosn contribuinte e não contribuinte(csosn_c e csosn_nc)    
    navegador.find_element("id", "product.fiscal.produto.CSOSN").send_keys(csosn_c)


    try:
        espera10.until(EC.presence_of_element_located(("id", "product.fiscal.produto.CSOSN-0")))

        navegador.find_element("id", "product.fiscal.produto.CSOSN-0").click()

    except TimeoutException:
        # elemento não existe > ignora o click
        pass

    navegador.find_element("id", "product.fiscal.produto.CSOSNNaoContribuinte").send_keys(csosn_nc)

    try:
        espera10.until(EC.presence_of_element_located(("id", "product.fiscal.produto.CSOSNNaoContribuinte-0")))

        navegador.find_element("id", "product.fiscal.produto.CSOSNNaoContribuinte-0").click()

    except TimeoutException:
        # elemento não existe > ignora o click
        pass


    #esperar a barra do ncm ser liberada
    navegador.find_element("id", "product.fiscal.produto.NCM").send_keys(ncm)

    # edita o ncm
    time.sleep(2)

    try:
        espera10.until(EC.presence_of_element_located(("id", "product.fiscal.produto.NCM-0")))

        navegador.find_element("id", "product.fiscal.produto.NCM-0").click()

    except TimeoutException:
        # elemento não existe > ignora o click
        pass









        # salva 
    navegador.find_element(By.CSS_SELECTOR,".btn.btn-primary.btn-sm").click()



    

time.sleep(10)