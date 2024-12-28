from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyautogui
import time




class Extracao():
    def __init__(self, horario):
        self.driver = ''
        #self.arquivo=''
        self.modo_jogo=''
        self.hr_inicio=horario


    def definir_navegador(self,jogo):
        self.modo_jogo=jogo
        self.driver = webdriver.Chrome() 
        self.driver.get("https://loterias.caixa.gov.br/Paginas/" + self.modo_jogo +".aspx")
        self.driver.maximize_window()
        #pyautogui.FAILSAFE = True #desfaz a ação padrão, de cancelar a ação caso mouse esteja em um dos cantos.
        #self.arquivo=open(self.modo_jogo +'.txt','a')
        time.sleep(15)
        
    def escrever_resultado(self):
        #armazena o numero/data do concurso e as dezenas sorteadas
        concurso=self.driver.find_element(By.XPATH, "//span[@class='ng-binding']")

        if self.modo_jogo == 'Mega-Sena':
            resultado=self.driver.find_element(By.ID,"ulDezenas")

        elif self.modo_jogo == 'Lotomania':
            resultado=self.driver.find_element(By.XPATH,"//ul[@class='simple-container lista-dezenas lotomania']")

        else:
            resultado=self.driver.find_element(By.XPATH,"//ul[@class='simple-container lista-dezenas lotofacil']")

        with open(self.modo_jogo +'_'+ self.hr_inicio + '.txt','a') as arquivo:
            arquivo.write(concurso.text +'\n' + resultado.text +'\n' + '\n')


    def buscar_concursos(self,numero):
        #realiza a busca do concurso passado em parâmetros
        campo_busca=self.driver.find_element(By.XPATH, '//*[@id="buscaConcurso"]')
        campo_busca.clear()
        campo_busca.click()
        campo_busca.send_keys(numero)
        pyautogui.press("Enter")
        time.sleep(1)
        campo_busca.send_keys(Keys.ENTER)

        #repete o mesmo passo após 3 segundos (tentando evitar erros de carregamento de página)
        time.sleep(3)
        campo_busca.clear()
        campo_busca.click()
        campo_busca.send_keys(numero)
        pyautogui.press("Enter")
        time.sleep(3)
        campo_busca.send_keys(Keys.ENTER)

        time.sleep(3)

        #com os dados em tela chama o metodo escrever_resultado
        self.escrever_resultado()

    def busca_alternativa(self, inicio, fim):
        contador = fim - inicio 
        voltar=self.driver.find_element(By.XPATH,'//*[@id="wp_resultados"]/div[1]/div/div[2]/ul/li[2]/a')
        avancar=self.driver.find_element(By.XPATH,'//*[@id="wp_resultados"]/div[1]/div/div[2]/ul/li[3]/a')
        for x in range(0,contador,1):
            voltar.click()
            time.sleep(4)
        for x in range(0,contador+1,1):
            time.sleep(4)
            self.escrever_resultado()
            time.sleep(1)
            avancar.click()
            


    def __del__(self):
        pass




