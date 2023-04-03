#导入需要使用的包
import requests
from bs4 import BeautifulSoup
from lxml import html
import time

#headers，防止被网站反爬虫机制检测
base_url = 'https://www.genecards.org'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'cookie': 'ASP.NET_SessionId=fbn1f52ppnbotksqpszu4lhe; rvcn=0Kpw76RjQWVPghHk_eHFMzdye5bqaMDGx5BUmO0BCiQv5NL9fBg_F6DHp2D7zcU955B-K0moDdWWLEgyLvPPU8H7vRY1; ARRAffinity=bbda99ae9f2cbea3a7894c6d34604e73c55fed16cf5f41fadce3a25415ea24f4; visid_incap_146342=JJg8EvqnRL21kFlyDqoJtVp4jF4AAAAAQUIPAAAAAADoDyfKhHCxYjc4Esv7sFIl; nlbi_146342=3Z3Bda14by/DQ4RJmewSQgAAAABIDL4M3uKW9Nn5B+a0Tx19; _ga=GA1.2.1127478822.1586264159; _gid=GA1.2.772327545.1586264159; __gads=ID=00050bb968e74cd0:T=1586264160:S=ALNI_MZrmbqyOxyLDo2Z5_k5rcoA7tMkLg; incap_ses_433_146342=JsQwcq4j9GPUtFdrVVQCBrF/jF4AAAAA4L1izrsxqq8bGasGou8j5g=='
}



#每次访问都获取cookie，也是防止被网站检测
def get_cookies(url):
    try:
        requests.session()
        sessions = requests.get(url, headers=headers)
        cookie = sessions.cookies
    except:
        cookie = ''
    return cookie
#用来获取genecards摘要的信息    
def get_genecards_info(gene_symbol, cookies):
    url = f'https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene_symbol}'
        
    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取基因摘要信息
        summary_section = soup.select_one('#summaries > div > p')
        if summary_section:
            summary = summary_section.get_text(strip=True).replace('\n', ' ').replace('\r', ' ')
        else:
            summary = '未找到基因摘要信息'


        return summary
    else:
        print(f'请求失败，无法获取 {gene_symbol} 的信息。')
        return None

# 从文件中读取基因符号列表，每1行有1个gene symbol。
with open('gene_symbols.txt', 'r') as f:
    gene_symbols = [line.strip() for line in f]


#输出所有结果到，genesummary.tsv文件中，每行第一列为gene symbol，第二列该gene symbol对应的genecard summary信息
with open('genesummary.tsv', 'w') as summary_file:
    summary_file.write("Gene Symbol\tGene Summary\n")
    
    for gene_symbol in gene_symbols:
        time.sleep(1)
        cookies=get_cookies(base_url)
        print(cookies)
        summary = get_genecards_info(gene_symbol, cookies)
        if summary:
            summary_file.write(f"{gene_symbol}\t{summary}\n")
            
