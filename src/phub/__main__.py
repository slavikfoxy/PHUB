'''
PHUB 4 CLI.

Contains a bunch of features
that can be accessed quickly. 
'''

import phub
import click
import getpass

@click.group()
def cli(): pass

@cli.command()
@click.argument('entry')
@click.option('--quality', '-q', help = 'Video quality', default = 'best')
@click.option('--output',  '-o', help = 'Output video file', default = '.')
def download(entry: str, quality: str, output: str) -> None:
    '''
    Download a specific video.
    '''
    
    client = phub.Client()
    
    urls = [entry]
    if entry.endswith('.txt'):
        with open(entry, 'r') as file:
            urls = file.read().split()
    
    for url in urls:
        video = client.get(url)
        print(f'Downloading video \033[92m{video.key}\033[0m')
        video.download(output, quality)

@cli.command()
@click.argument('query')
@click.option('--pages', '-p', help = 'Pages to search', default = '1')
def search(query: str, pages: str) -> None:
    '''
    Search for videos.
    '''
    
    client = phub.Client()
    
    q = client.search(query)
    
    for i in range(int(pages) * 32):
        
        video = q[i]
        print(f'* \033[93m{video.title}\033[0m ({video.duration}) - {video.key}')

def init_pass_client(user: str = None) -> phub.Client:
    '''
    Get credentials and load a client
    '''
    
    if not user: user = input('Username: ')
    password = getpass.getpass()
    return phub.Client(user, password)

@cli.command()
@click.option('-n', help = 'Video count', default = '1')
@click.option('-o', '--output', help = 'Output dir', default = '.')
@click.option('-u', '--user', help = 'Account username')
@click.option('-q', '--quality', help = 'Video quality', default = 'best')
def watched(n: str, output: str, user: str, quality: str) -> None:
    '''
    Download the n-last watched videos.
    '''
    client = init_pass_client(user)
    q = client.account.watched

    for i in range(int(n)):
        
        video = q[i]
        
        video.download(output, quality, display = phub.display.bar(f'Downloading {video.key}'))

@cli.command()
@click.option('-n', help = 'Video count', default = '1')
@click.option('-o', '--output', help = 'Output dir', default = '.')
@click.option('-u', '--user', help = 'Account username')
@click.option('-q', '--quality', help = 'Video quality', default = 'best')
def liked(n: str, output: str, user: str, quality: str) -> None:
    '''
    Download the n-last watched videos.
    '''
    
    client = init_pass_client(user)
    q = client.account.liked

    for i in range(int(n)):
        
        video = q[i]
        
        video.download(output, quality, display = phub.display.bar(f'Downloading {video.key}'))

if __name__ == '__main__':
    cli()

# EOF