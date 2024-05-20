import os           # 운영체제의 명령들을 처리할 수 있는 모듈
import json         # json 데이터를 처리하기 위함
import requests


class NewsConfig:
    '''news api를 처리하기 위한 congif.json 파일을 읽어서 처리하는 클래스'''
    def __init__(self, config_file:str) -> None:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)                     # config는 딕셔너리 형태로 반환됨
                self.__base_url = config['base_url']
                self.__api_key = config['api_key']
                self.__category = config['category']
                self.__language = config['language']
               
        except Exception as e:                            # Exception은 최상위 예외 클래스이다  # except는 여러개 작성 가능
            print(f'Error : {e}')
            raise Exception(f'Error : {e}')
        
    def __repr__(self) -> str:
        return f'NewsConfig :  {self.__base_url}, {self.__api_key}, {self.__category}, {self.__language}'
    
    def get_language(self) -> iter:                 # iter = 반복가능한 객체의 최상위 
        return self.__language
    
    def get_lang_code(self, i:int) -> str:
        return self.__language[i]['code'].lower()
    
    def get_categories(self) -> iter:
        return self.__category
    
    def get_category(self, i:int) -> str:
        return self.__category[i].lower()
    
    def get_api_key(self) -> str:
        return self.__api_key
    
    def get_base_url(self) -> str:
        return self.__base_url
    
        
class NewsLoader:
    '''News API 사이트로부터 뉴스 기사를 로드하고 정보를 제공'''
    def __init__(self) -> None:
        self.status = 'not yet'
        self.total_results = 0
        self.articles = []
        self.pages = 0
        self.vpp = 20
            
    def remove_quotes(self) -> None:
        for article in self.articles:
            # di = {'title':null}
            # s1 = None #di['title']
            # s1 = s1.replace('"', '') if s1 is not None else ''          
            article['title'] = article['title'].replace('"','') if article['title'] is not None else ''           # DATA의 실체를 만들어 주기 위해, 값이 없으면 '빈문자열'을 입력함
            article['description'] = article['description'].replace('"','') if article['description'] is not None else ''
            article['author'] = article['author'].replace('"','') if article['author'] is not None else ''
        
    def load_news_from_url(self, url:str) -> None:
        try:
            response = requests.get(url)
            news_json = response.json()       # response 객체로부터 json 데이터를 추출한다
            if news_json['status'] != 'ok':
                raise Exception('Error : Unable to load news')
            
            self.articles += news_json['articles']
            self.status = news_json['status']
            self.total_results = int(news_json['totalResults'])
            self.remove_quotes
                                          
        except Exception as e:
            print(f'Error : {e}')
            raise Exception(f'Error : {e}')

    def load_news(self, base_url:str, api_key:str, lang:str, category:str, vpp:int=20):
        try:
            url = f'{base_url}?country={lang}&apiKey={api_key}'
            if category.lower() != 'topic':
                url += f'&category={category}'
            
            self.load_news_from_url(url)
            self.vpp = vpp                          
                
            self.__calculate_total_pages()
            for i in range(2, self.pages+1):
                page_url = url + f'&page={i}'
                self.load_news_from_url(page_url)
                
        except Exception as e:
            print(f'Error : {e}')
            raise Exception(f'Error : {e}')
        
    def __calculate_total_pages(self) -> None:
        if self.vpp == 0:
            return
        
        page = self.total_results // self.vpp
        nam = self.total_results % self.vpp
        self.pages = page if nam == 0 else page + 1
    
    def get_total_results(self) -> int:
        return self.total_results








   
def clear_screen():
     os.system('cls' if os.name=='nt' else 'clear')         # nt = windows
    
if __name__ == '__main__':
    news_conf = NewsConfig('config.json')
    print(news_conf)
    
    clear_screen()                                          # 화면을 청소한다
    
    for i, lang in enumerate(news_conf.get_language()):
        print(f'{i+1} : {lang["code"]}, {lang["name"]}')
    
    sel = int(input('나라를 선택하세요 >>>'))
    lang_code = news_conf.get_lang_code(sel-1)
    
    print()    
    
    for i, cate in enumerate(news_conf.get_categories()):
        print(f'{i+1} : {cate}')
        
    sel = int(input('카테고리를 선택하세요 >>>'))
    category = news_conf.get_category(sel-1)
    
    clear_screen()
    
    news_loader = NewsLoader()
    news_loader.load_news(news_conf.get_base_url(),
                          news_conf.get_api_key(),
                          lang_code,
                          category)
    
    
    print(f'Total Results: {news_loader.get_total_results()}')
    print()
    print(f'Count of articles: {len(news_loader.articles)}')
    print()
    
    for i, article in enumerate(news_loader.articles):
        print('---------------------------------------------')
        print(f'No : {i+1}')
        print(f'Title : {article["title"]}')
        print(f'Description : {article["description"]}')
        print(f'URL : {article["url"]}')
        print(f'Image URL : {article["urlToImage"]}')
        print(f'Author : {article["author"]}')
        print(f'Published At : {article["publishedAt"]}')
        print(f'Source : {article["source"]["name"]}')