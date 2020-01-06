# -*- coding: utf-8 -*-
import scrapy


# Chose tenté dans la console :
# - scrapy shell
# - fetch("https://www.woolworths.com.au/shop/browse/drinks/cordials-juices-iced-teas/iced-teas")
# - view(response) -> Génère une erreur 404 d'où le fait de ne pas trouver les info voulu
# Tentative en changeant le user agent -> Rien

# Le code est donc realisé sur une autre page que celle donné dans l'exercice
class AmazonspiderSpider(scrapy.Spider):
    name = 'AmazonSpider'

    # start_urls = ['https://www.amazon.fr/gp/browse.html?node=13910711&ref_=nav_em_T1_0_4_11_1__tele']

    def start_requests(self):
        start_urls = ['https://www.amazon.fr/gp/browse.html?node=13910711&ref_=nav_em_T1_0_4_11_1__tele']
        for url in start_urls:
            # On realise une requete sur chaque url de la liste et on appelle la fonction parse sur la reponse
            yield scrapy.Request(url=url, callback=self.parse)

    # response -> Reponse a la requete effecuté dans start_requests
    def parse(self, response):

        print("procesing:" + response.url)
        # Extract data using css selectors
        # On extrait les nom avec les differents selecteur
        product_names = response.css('.octopus-pc-item-link').xpath('@title').extract()
        # On extrait la valeur entiere du prix de l'objet
        product_prices_whole = response.css('.a-price-whole::text').extract()
        # On extrait la valeur decimal du prix de l'objet
        product_prices_decimal = response.css('.a-price-fraction::text').extract()
        # On extrait le symbole de la monnaie du prix de l'objet
        product_prices_symbol = response.css('.a-price-symbol::text').extract()

        # On remet la valeur entiere et la valeur decimal en 1 seul valeur
        product_prices_full = []

        for i in range(0, len(product_prices_whole)):
            product_prices_full.append(product_prices_whole[i] + '.' + product_prices_decimal[i])

        # On zip les 3 list pour avoir des triplet qu'on va parser pour générer le csv
        row_data = zip(product_names, product_prices_full, product_prices_symbol)
        for item in row_data:
            scraped_info = {
                'product_name': item[0][:60],  # On limite la à 60 caractère pour des raison de lisibilité
                'product_price': item[1],
                'product_currency': item[2]
            }
            print(scraped_info)
            yield scraped_info
