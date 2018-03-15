import sys
import os.path

try:
    from urllib.request import urlopen
    from urllib import parse as urlparse
except ImportError:
    from urllib2 import urlopen, urlparse

from bs4 import BeautifulSoup


'''
Scrapes news links and store it to a file
Stores the news links in news-links.txt
'''

def giveMonth(month):
    if month.lower() == 'january':
        return 1
    elif month.lower() == 'february':
        return 2
    elif month.lower() == 'march':
        return 3
    elif month.lower() == 'april':
        return 4
    elif month.lower() == 'may':
        return 5
    elif month.lower() == 'june':
        return 6
    elif month.lower() == 'july':
        return 7
    elif month.lower() == 'august':
        return 8
    elif month.lower() == 'september':
        return 9
    elif month.lower() == 'october':
        return 10
    elif month.lower() == 'november':
        return 11
    elif month.lower() == 'december':
        return 12

def scrape_blogs():
    f = open('checkpoint.txt', 'r')

    main_url = f.read().splitlines()[0]
    # url = "http://balaybalakasoy.blogspot.com/2018/03/sphinx-usa-ka-mangtas-nga-tahas-ug-ang.html"
    # http://www.sunstar.com.ph/superbalita-cebu/balita
    f.close()

    stop_scraping_process = False
    point = main_url
    http = "http://www.sunstar.com.ph"
    while not stop_scraping_process:
        page = urlopen(point)
        print(point) 

        soup = BeautifulSoup(page, 'html.parser')

        # page of superbalita-cebu/balita
        urls = soup.findAll('h3', {'class': 'title'})
        # urls.pop(0)

        for url in urls:
            child = url.findChildren()[0]

            curr_url = http + child.get('href')
            title = child.getText()
            print title

            try:
                curr_page = urlopen(curr_url)
                curr_soup = BeautifulSoup(curr_page, 'html.parser')

                # date
                date = curr_soup.find('div', {'class': 'node-info-item'})
                date = date.getText().replace(',', '').split()
                m = giveMonth(date[1])
                d = date[2]
                y = date[3]

                curr_date = '%s-%s-%s' % (m, d, y)

                # authors
                authors = curr_soup.findAll('a', {'typeof': 'skos:Concept', 'property': 'rdfs:label skos:prefLabel'})

                curr_authors = []

                for author in authors:
                    if '/author/' in author.get('href'):
                        curr_authors.append(author.getText())

                # print curr_authors


                # content

                paragraphs = curr_soup.findAll('p')
                content = ""

                for paragraph in paragraphs:
                    if "latest issues of sunstar superbalita-cebu" in paragraph.getText().lower():
                        break
                    else:
                        content = content + paragraph.getText() + '\n'

                all_text = title + "\n"
                all_text = all_text + curr_date + "\n"

                if len(curr_authors) > 0:
                    all_text = all_text + curr_authors[0]

                    for i in range(1, len(curr_authors)):
                        all_text = all_text + ", " + curr_authors[i]

                all_text = all_text + '\n\n' 

                all_text = all_text + title + '\n\n'
                all_text = all_text + content

                # print all_text 


                # if os.path.exists('data/'+ title +'.txt'):
                #     f = open('data/' + title + '_o.txt', 'w')
                # else:
                f = open('data/' + title + '.txt', 'w')

                f.write(all_text.encode('utf-8') + '\n')
                f.close()

                next_page = soup.find('a', {'title': 'Go to next page'})

                if next_page:
                    next_page = next_page['href']
                    point = http + next_page
                    f = open('checkpoint.txt', 'w')
                    f.write(point + '\n')
                    f.close()
                    stop_scraping_process = False
                else:
                    stop_scraping_process = True


            except IOError:
                print "error reading " + title
                err_file = open('errors.txt', 'a')
                err_file.write(curr_url)
                err_file.close()

            


            


            # print child
            # url.findChildren()[0]

        # stop_scraping_process = True

        # 


        
        # date = soup.find('h2', {'class': 'date-header'})
        # date = date.getText()
        # date = date.replace('.', '-')
        
        # body = soup.find('div', {'class': 'post hentry uncustomized-post-template'})
        # # print(body.getText().strip().splitlines())

        # lines = body.getText().strip().splitlines()
        
        # content = lines.pop(0).strip() + '\n\n'

        # for line in lines:
        #     curr_line = line.strip()
        #     if curr_line:
        #         if curr_line[0] == '-' and curr_line[1] == '-':
        #             break
        #         else:
        #             content = content + curr_line + '\n'
                    

        # # print lines
        # # print content        

        # title = soup.find('h3', {'class': 'post-title entry-title'})
        # title = title.getText()
        # title = title.strip().rstrip('\n')

        # # text = ''
        # # contents = soup.findAll('span', {'style': 'color: #b6d7a8;', 'style': 'color: #b6d7a8; font-family: "georgia";', 'style': 'color: #b6d7a8; font-family: "georgia"; font-size: 12pt;', 'style': 'color: #b6d7a8; font-family: "georgia"; font-size: 12.0pt;'})
        # # # print contents
        # # for content in contents:
        # #     content = content.getText().strip().rstrip()
        # #     if content:
        # #         text += content + '\n'

        # author = soup.find('span', {'style': 'color: #9fc5e8;', 'style': 'color: #9fc5e8; font-family: "georgia";'})
        
        # if not author:
        #     divs = soup.findAll('div', {'style': 'font-family: Georgia;'})
        #     child = divs[-1].findChildren()[0]

        #     if "," in child:
        #         if "." not in child:
        #             child = divs[-2].findChildren()[0]

        #     author = child

        # author = author.getText()
        # author = author.replace('--', '')
        # author = author.strip().rstrip()
        

        # # for title in titles:
        # #     child = title.findChildren()[0]
        # #     write_file("files/news-links.txt", contents=[main_url + child.get('href')], mode="a")
        # #     print(main_url + child.get('href'))
        # #     print("\n")
        # #     i += 1-
        # #     if i == limit:
        # #         break

        # # # next_page = soup.find('a', {'title': 'Go to next page'})
        # # # if next_page:
        # # #     url = main_url + next_page.get('href')
        # # # else:

        # lit = title + '\n'
        # lit = lit + date + '\n'
        # lit = lit + author + '\n\n'
        # lit = lit + content + '\n'

        # # print "--------"
        # # print lit
        # # print "--------"

        # if os.path.exists('data/'+ title+'.txt'):
        #     f = open('data/' + title + '_o.txt', 'w')
        # else:
        #     f = open('data/' + title + '.txt', 'w')

        # f.write(lit.encode('utf-8') + '\n')
        # f.close()

        
        # stop_scraping_process = True

'''
Scrapes news contents from links stored in news-links.txt
Stores the news contents in news-raw.txt
'''
# def scrape_news_contents():
#     checkpoint = read_file("files/news-links-cp.txt")
#     start = int(checkpoint[0])
#     if start == 501:
#         print("Status: Finished!")
#         return

#     urls = read_file("files/news-links.txt", start=start)
#     contents = []
#     for idx, url in enumerate(urls):
#         start += 1
#         print("Link [" + str(start) + "]: "  + url)
#         page = urlopen(url)
#         soup = BeautifulSoup(page, 'html.parser')
#         div = soup.find('div', {'class': 'field-item even', 'property': 'content:encoded'})
#         for child in div.findChildren():
#             contents.append(child.getText())
#         write_file("news-raw.txt", contents=contents, per_line=True, mode="a")
#         contents = []
#         endpoints = [
#             str(start + 1)
#         ]

#         write_file("files/news-links-cp.txt", contents=endpoints, mode="w")


scrape_blogs()
