import requests
from bs4 import BeautifulSoup
from lxml import html
import time
base_url = 'https://www.genecards.org'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'cookie': 'ASP.NET_SessionId=fbn1f52ppnbotksqpszu4lhe; rvcn=0Kpw76RjQWVPghHk_eHFMzdye5bqaMDGx5BUmO0BCiQv5NL9fBg_F6DHp2D7zcU955B-K0moDdWWLEgyLvPPU8H7vRY1; ARRAffinity=bbda99ae9f2cbea3a7894c6d34604e73c55fed16cf5f41fadce3a25415ea24f4; visid_incap_146342=JJg8EvqnRL21kFlyDqoJtVp4jF4AAAAAQUIPAAAAAADoDyfKhHCxYjc4Esv7sFIl; nlbi_146342=3Z3Bda14by/DQ4RJmewSQgAAAABIDL4M3uKW9Nn5B+a0Tx19; _ga=GA1.2.1127478822.1586264159; _gid=GA1.2.772327545.1586264159; __gads=ID=00050bb968e74cd0:T=1586264160:S=ALNI_MZrmbqyOxyLDo2Z5_k5rcoA7tMkLg; incap_ses_433_146342=JsQwcq4j9GPUtFdrVVQCBrF/jF4AAAAA4L1izrsxqq8bGasGou8j5g=='
}




def get_cookies(url):
    try:
        requests.session()
        sessions = requests.get(url, headers=headers)
        cookie = sessions.cookies
    except:
        cookie = ''
    return cookie
    
def get_genecards_info(gene_symbol, cookies):
    url = f'https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene_symbol}'
        
    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')


        # 使用 lxml 库解析响应文本
        tree = html.fromstring(response.content)

         #获取别名信息
        aliases_xpath1 = '/html/body/div[2]/div[2]/div/div/main/div[2]/div/div/section[1]/div[1]/div[1]/div[1]/div[1]/ul/li/span'
        aliases_xpath2 = '/html/body/div[2]/div[2]/div/div/main/div[2]/div/div/section[1]/div[1]/div[1]/div[1]/div[2]/ul/li/span'
        aliases_xpath3 = '/html/body/div[1]/div[2]/div/div/main/div[2]/div/div/section[1]/div[1]/div[1]/div[1]/div/ul/li/span'
                          
        aliases_element1 = tree.xpath(aliases_xpath1)
        aliases_element2 = tree.xpath(aliases_xpath2)
        aliases_element3 = tree.xpath(aliases_xpath3)

        aliases_list = []

        if aliases_element1:
            aliases_list.extend([alias.text_content().strip() for alias in aliases_element1])

        if aliases_element2:
            aliases_list.extend([alias.text_content().strip() for alias in aliases_element2])

        if aliases_element3:
            aliases_list.extend([alias.text_content().strip() for alias in aliases_element3])

        aliases = '; '.join(aliases_list)

        return aliases
    else:
        print(f'请求失败，无法获取 {gene_symbol} 的信息。')
        return None, None

# 从文件中读取基因符号列表
with open('gene_symbols.txt', 'r') as f:
    gene_symbols = [line.strip() for line in f]

with open('genealias.tsv', 'w') as alias_file:
    
    alias_file.write("Gene Symbol\tGene Aliases\n")
    
    for gene_symbol in gene_symbols:
        time.sleep(1)
        cookies=get_cookies(base_url)
        #print(cookies)
        aliases = get_genecards_info(gene_symbol, cookies)
        if aliases:
            alias_file.write(f"{gene_symbol}\t{aliases}\n")

            