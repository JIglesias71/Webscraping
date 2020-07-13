#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 19:00:46 2020

@author: jaimeiglesias
"""

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime

e = datetime.datetime.now()
dt = str("%s" % e)

vendor = []
p_type = []
products = []
prices = []


# Mariscos Cibeira
driver = webdriver.Chrome("/Users/jaimeiglesias/Documents/Jobs/5.DPEP/5.New_projects/chromedriver")
driver.get('https://mariscoslaureano.com/tienda/')
cibeira_content = driver.page_source
cibeira_shop0 = bs(cibeira_content)
cibeira_shop1 = cibeira_shop0.find('ul', attrs = {'class': "products columns-3"})

for products1 in cibeira_shop1.findAll('li'):
    driver.get(products1.find('a').attrs['href'])
    cibeira_content2 = driver.page_source
    cibeira_shop2 = bs(cibeira_content2)
    cibeira_shop3 = cibeira_shop2.find('ul', attrs = {'class': "products columns-3"})
    
    for products2 in cibeira_shop3.findAll('li'):
        name = products2.find('h2', attrs = {'class': "woocommerce-loop-product__title"})
        price = products2.find('span', attrs = {'class': "woocommerce-Price-amount amount"})
        vendor.append('Cibeira')
        p_type.append(products1.find('h2').text)
        products.append(name.text)
        if price is None:
            prices.append('n/a')
        else:
            prices.append(float(price.text.replace(',', '.').replace('€', '').replace(' ', '')))
        

# Selectos de Castilla
driver.get('https://tienda.selectosdecastilla.com/es/')
selectos_content = driver.page_source
selectos_shop0 = bs(selectos_content)
selectos_shop1 = selectos_shop0.find('div', attrs = {'class': 'wrap_submenu'})

for products1 in selectos_shop1.findAll('li'):
    driver.get(products1.find('a').attrs['href'])
    selectos_content2 = driver.page_source
    selectos_shop2 = bs(selectos_content2)
    
    for products2 in selectos_shop2.findAll('li',
                                            attrs = {'class': "ajax_block_product col-phone-12 col-xs-6 col-sm-4 col-md-4 col-lg-3"}):
        name = products2.find('a', attrs = {'class': 'product-name'})
        price = products2.find('span', attrs = {'itemprop': 'price'})
        vendor.append('Selectos')
        p_type.append(products1.find('a').attrs['title'])
        products.append(name.text)
        prices.append(float(price.text.replace(',', '.').replace('€', '').replace(' ', '')))


driver.quit()


# Saving in df and subsequently storing in Excel
df = pd.DataFrame({'Vendor': vendor, 'Type': p_type, 'Product': products,
                   'Price'+' '+ dt: prices})
    
globals().update({'df_'+v: df[df['Vendor']==v] for v in df['Vendor'].unique()})

writer = pd.ExcelWriter('Website_pricing.xlsx', engine = 'xlsxwriter')
df_Cibeira.to_excel(writer, sheet_name = 'Cibeira')
df_Selectos.to_excel(writer, sheet_name = 'Selectos')
writer.save()
