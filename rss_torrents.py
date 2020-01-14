import feedparser
import sys
import qbittorrentapi
import click
import config as cfg

# instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(host=cfg.qbittorrent['host'], username=cfg.qbittorrent['user'], password=cfg.qbittorrent['password'])

# the Client will automatically acquire/maintain a logged in state in line with any request.
# therefore, this is not necessary; however, you many want to test the provided login credentials.
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

url = 'http://nyaa.si/?page=rss&q='

for i, arg in enumerate(sys.argv):
    if(i > 0):
        url_final = url + arg
    else:
        url_final = url

response = feedparser.parse(url_final)

print(url_final)

if (len(response.entries) != 0):
    for titles in response.entries:
        if (len(sys.argv) > 1):
            if( '1_3' in titles.nyaa_categoryid):
                print(titles.title)
                print(titles.link)
                if click.confirm('Do you want to download ?'):
                    click.echo('Downloading...')
                    qbt_client.torrents_add(titles.link, savepath=cfg.savepath['path'])
            elif ( '1_2' in titles.nyaa_categoryid):
                if click.confirm('Do you want to download ?'):
                    click.echo('Downloading...')
                    qbt_client.torrents_add(titles.link, savepath=cfg.savepath['path'])

        else:
            if( '1_2' in titles.nyaa_categoryid):
                print(titles.title)
                print(titles.link)

else:
    print("Didn't find any anime, sorry")

