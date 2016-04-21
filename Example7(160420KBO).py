from bs4 import BeautifulSoup
import requests

url = 'http://www.koreabaseball.com/Record/Player/HitterDetail/Game.aspx?playerId=76325'

with requests.Session() as session:
    session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}

    # parsing parameters
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    data = {
        'ctl00$ctl00$cphContainer$cphContents$ddlYear': '2013',
        'ctl00$ctl00$txtSearchWord': '',
        '__EVENTTARGET': soup.find('input', {'name': '__EVENTTARGET'}).get('value', ''),
        '__EVENTARGUMENT': soup.find('input', {'name': '__EVENTARGUMENT'}).get('value', ''),
        '__LASTFOCUS': soup.find('input', {'name': '__LASTFOCUS'}).get('value', ''),
        '__VIEWSTATE': soup.find('input', {'name': '__VIEWSTATE'}).get('value', ''),
        '__VIEWSTATEGENERATOR': soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value', ''),
        '__EVENTVALIDATION': soup.find('input', {'name': '__EVENTVALIDATION'}).get('value', ''),
    }

    # parsing data
    response = session.post(url, data=data)

    soup = BeautifulSoup(response.content, 'lxml')

    for row in soup.select('table.tData01 tr'):
        print([td.text for td in row.find_all('td')])