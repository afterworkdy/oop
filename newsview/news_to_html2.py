from newsview2 import NewsConfig, NewsLoader
from myutil import clear_screen
import datetime


class NewsToHtml:
    def __init__(self, country_name:str='Korea', category:str='topic') -> None:
        self.html_top = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style.css">
  <title>Document</title>
</head>
<body>
  <div class="country">
    <div>
      <img src="resources/kr.svg" alt="">
    </div>
    <div class="country_name">
      <h1>South Korea</h1>
      <h3>Topic</h3>
    </div>
  </div>
  <div class="articles">'''
  
        self.html_bottom = f'''  </div>  <!-- articles -->
</body>
</html>'''

        self.html_mid = ''
    
    def add_article(self, image_url, url, title, desc, author, date): 
        self.html_mid += f'''    <div class="article">                      
      <div class="news_image">
        <img src="{image_url}" alt="">
      </div> <!-- news_image -->
      <div class="news_block">
        <div class="news_title"><a href="{url}">{title}</a></div>
        <div class="news_desc">{desc}</div>
        <div class="news_author">{author}</div>
        <div class="news_date">{date}</div>    
      </div>  <!-- news_block -->
    </div>  <!-- article -->        
    '''

    def save(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.html_top)
                f.write(self.html_mid)
                f.write(self.html_bottom)
        except Exception as e:
            print(f'Error : {e}')
            raise Exception(f'Error : {e}')
        


if __name__ == '__main__':
    conf = NewsConfig('config.json')
    news_loader = NewsLoader
    
    clear_screen()
    for i, lang in enumerate(conf.get_language()):
        print(f'{i+1} : {lang["code"]}, {lang["name"]} ')
        
    sel = int(input('Select Language : '))
    lang_code = conf.get_lang_code(sel-1)
    lang_name = conf.get_language()[sel-1]["name"]
    
    
    clear_screen
    for i, cate in enumerate(conf.get_categories()):
        print(f'{i+1} : {cate}')
        
    sel = int(input('Select Category : '))
    category = conf.get_category(sel-1)
    
    news_loader.load_news(conf.get_base_url(),
                          conf.get_api_key(),
                          lang_code,
                          category)

    
    news_html = NewsToHtml(lang_name, category)
    for article in news_loader.articles:
        news_html.add_article(article['urlToIage'],
                              article['url'],
                              article['title'],
                              article['description'],
                              article['author'],
                              article['publishedAt'])
    
    now = datetime.datetime.now()    
    current_datetime = now.strftime("%Y%m%d_%H%M%S")
    html_filename = f'{lang_code}_{category}_{current_datetime}.html'
    news_html.save(html_filename)
    
    print(f'HTML file saved as {html_filename}')


