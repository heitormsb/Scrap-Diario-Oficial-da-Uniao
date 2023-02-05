import cfscrape 
from bs4 import BeautifulSoup 
import json
 
scraper = cfscrape.create_scraper() 
response = scraper.get('https://www.in.gov.br/leiturajornal') 
soup = BeautifulSoup(response.text, 'html.parser') 
 

json_content = soup.find_all(type="application/json")
urlTitle = []

# pega todos os links de cada edição
for i in json_content:
  jsn = i.get_text()
  jsn_obj = json.loads(jsn)
  if len(jsn_obj) == 1:
    continue

  len_links = len(jsn_obj['jsonArray'])
  for j in range(len_links):
    urlTitle.append(jsn_obj['jsonArray'][j]['urlTitle'])


scrp = {}
for i in urlTitle:
  url = 'https://www.in.gov.br/en/web/dou/-/' + i
  response = scraper.get(url)
  print(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  
  # print(soup.find(id='versao-certificada').get('href'))
  versao_certificada = soup.find(id='versao-certificada').get('href')
  scrp["versao_certificada"] = versao_certificada

  # print(soup.find(class_='publicado-dou-data').get_text())
  scrp["publicado_dou_data"] = soup.find(class_='publicado-dou-data').get_text()

  # print(soup.find(class_='edicao-dou-data').get_text())
  scrp["edicao_dou_data"] = soup.find(class_='edicao-dou-data').get_text()

  # print(soup.find(class_='secao-dou-data').get_text())
  scrp["secao_dou_data"] = soup.find(class_='secao-dou-data').get_text()

  # print(soup.find(class_='orgao-dou-data').get_text())
  scrp["orgao_dou_data"] = soup.find(class_='orgao-dou-data').get_text()



  scrp["title"] = [[]]
  scrp["dou_paragraph"] = [[]]
  scrp["assina"] = [[]]
  scrp["cargo"] = [[]]

  get_prox_title = 0
  get_prox_paragraph = 0
  get_prox_assina = 0
  get_prox_cargo = 0


  paragraph = soup.find_all(class_='identifica')
  while True:
    try:
      ## TITULO, Caso tenha mais de um titulo pega todos e coloca em uma lista de listas sendo cada indice da lista um titulo
      if paragraph[0].get_attribute_list('class') == ['identifica']:
        scrp["title"][get_prox_title].append(paragraph[0].get_text())
        scrp["title"].append([])
        get_prox_title += 1

        if paragraph[0].find_next_sibling().get_attribute_list('class') == ['ementa']:
          paragraph[0] = paragraph[0].find_next_sibling()

        ## PARAGRAFOS, Caso tenha mais de um paragrafo pega todos e coloca em uma lista de listas sendo cada indice da lista um paragrafo
        # Pega todos os paragrafos abaixo do titulo, caso tenha outro titulo ele vai adicionar na lista de paragrafos em outro indice
        while paragraph[0].find_next_sibling().get_attribute_list('class') == ['dou-paragraph']:
          scrp["dou_paragraph"][get_prox_paragraph].append(paragraph[0].find_next_sibling().get_text())
          paragraph[0] = paragraph[0].find_next_sibling()

      paragraph[0] = paragraph[0].find_next_sibling()
          

      ## ASSINA
      if paragraph[0].get_attribute_list('class') == ['assina']:
        scrp["assina"][get_prox_assina].append(paragraph[0].get_text())
        scrp["assina"].append([])
        get_prox_assina += 1


      ## CARGO
      if paragraph[0].get_attribute_list('class') == ['cargo']:
        scrp["cargo"][get_prox_cargo].append(paragraph[0].get_text())
        scrp["cargo"].append([])
        get_prox_cargo += 1

      # caso tenha outro titulo ele vai adicionar na lista de paragrafos em outro indice
      if paragraph[0].find_next_sibling().get_attribute_list('class') == ['dou-paragraph'] and paragraph[0].get_attribute_list('class') != ['dou-paragraph']:
        scrp["dou_paragraph"].append([])
        get_prox_paragraph += 1

    except:
      scrp["title"].pop()
      scrp["assina"].pop()
      scrp["cargo"].pop()
      break

  print(json.dumps(scrp, indent=4))
  # print(scrp)
  # break


  

    