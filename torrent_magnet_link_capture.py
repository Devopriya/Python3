def link_catcher(url, fin_url):
  
  # Importing Libraries
  import requests
  from bs4 import BeautifulSoup as bs
  import pandas as pd
  
  # Setting Parameters
  response = requests.get(url)
  html_page = bs(response.content, "html.parser")
  all_links = html_page.find_all('a')

  links = {'link':[], 'category':[]}
  for link in all_links:
    href = link['href']
    if href:
      if r'magnet:?' in href:
        links['link'].append(f"{href}")
        links['category'].append('magnet')
      if r'torrent' in href:
        links['link'].append(f"{fin_url}{href}")
        links['category'].append('internal')
      if href[0] == "#":
        links['link'].append(href)
        links['category'].append('internal')
      if href.split(":")[0] in ["https", "http"] and not r'torrent' in href:
        links['link'].append(href)
        links['category'].append('external')

  data = pd.DataFrame(links)

  data_internal = data[(data["category"]=='internal') | (data["category"]=='magnet')].reset_index()
  return data_internal

    
	
def extract_magnet(keyword, url, fin_url):

  magnet_link_set = []
  for i in link_catcher(url, fin_url)['link']:
  
    if keyword in i:
      url_int = i

      data_internal = link_catcher(url_int, fin_url)

      magnet_link_set.append(data_internal[data_internal["category"]=="magnet"]['link'].drop_duplicates().reset_index(drop=True).to_string().split(' ')[-1])
    

  return set(magnet_link_set)



def main():
	url = input("\n\nPlease enter the torrent search link : \n\n")
	fin_url = "https://www.1377x.to"
	
	keyword = input("\n\nPlease enter the keyword you want to seacrh : ")
	
	magnet_link_set = extract_magnet(keyword, url, fin_url)
	
	print("\n\nBelow are the Magnet values extracted : \n")
 
	for i in magnet_link_set:
		print(i)
	


if __name__ == "__main__":
    main()	