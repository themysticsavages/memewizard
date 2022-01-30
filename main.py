print( '\x1b[32m\x1b[1m',
'''
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
  ███   ███   ███████   ███   ███   ███████          ███████   ██       ██
  ████ ████   ██        ████ ████   ██               ██        ██       ██
  ██ ███ ██   ███████   ██ ███ ██   ███████   █████  ██        ██       ██
  ██ ███ ██   ██        ██ ███ ██   ██               ██        ██       ██
  ██     ██   ███████   ██     ██   ███████          ███████   ███████  ██
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
''',
'\x1b[0m' )

from library import fetchd, meme_object, predict
from thefuzz import fuzz as difflib
from html2image import Html2Image
from bs4 import BeautifulSoup
from tabulate import tabulate
from tqdm import tqdm
import PyInquirer
import statistics
import requests
import random
import json
import os

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def predict_meme():
  r = requests.get('https://knowyourmeme.com/memes/',
  headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'})
  s = BeautifulSoup(r.text, 'html.parser')

  try:
    m = s.find('tbody', {'class':['entry-grid-body', 'infinite']}).text.split('    ')

    for i, s in enumerate(m):
        m[i] = s.strip()
        if m[i] == '': del m[i]
    for i, s in enumerate(m): m[i] = s.strip()
    for i, s in enumerate(m):
        if 'NSFW' in m[i] or m[i] == 'NSFW':
            del m[i+1]
            del m[i]
    while '' in m:
      m.remove('')
    for i, s in enumerate(m):
        if 'Updated' in m[i]: del m[i]
  except AttributeError:
    print(color.RED+'Uh oh! This script failed! You may be banned from knowyourmemes.com.'+color.END)
    open('error.log','w').write(r.text)
    exit(0)
  m = list(set(m))
  l = ['/memes/'+e.lower().replace(' ', '-') for e in m]
  x = input(color.BOLD+color.BLUE+'Enter a meme (Enter ? for memes) > '+color.END)

  if x == '?':
    print('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'+'\n'.join([h.strip() for h in m]), '\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬')
    predict_meme()

  y = int(input(color.BOLD+color.YELLOW+'How many memes should I fetch? (current amount to fetch is {}) '.format(len(m))+color.END))

  memes = []
  for en in tqdm(l[:y]):
      memes.append(fetchd(en))
  print(memes)

  keys = [list(d.keys())[0] for d in memes[:10]]
  resp = {}

  for t in keys:
      ratio = difflib.token_set_ratio(x, t)
      resp[str(ratio)] = t

  val = resp[str(max([int(k) for k in resp.keys()]))]
  json = next(item for item in memes if list(item.keys())[0] == val)

  print(color.BOLD+color.GREEN+val+'\n'+color.END+tabulate(json[val]))
  show = input(color.BOLD+color.BLUE+'Would you like to view the trend history for this meme ({}) [Y/n] ? '.format(val)+color.END)

  if show == 'n' or show == 'N':
    exit(0)
  else:
    print(color.BOLD+'Saving trend history to "figure.png"...'+color.END)
    predict(val)
    exit(0)

def make_pie():
  def rgb_to_hex(rgb):
      return '#%02x%02x%02x' % rgb
  def colors(amount):
      return [rgb_to_hex((random.randrange(200,255),random.randrange(200,255),random.randrange(200,255))) for _ in range(amount)]

  doc = requests.get('https://raw.githubusercontent.com/ajskateboarder/stuff/main/meme.js/pie.html').text
  page = meme_object.fetch_memes('1')

  resp = {}
  for sn in page:
        s, v = meme_object.fetch_trend_history([sn])
        try:
            resp[sn]=statistics.mean(s[0])
        except IndexError:
            pass

  data, colors = json.dumps(resp).replace('{','').replace('}',''), str(colors(len(resp))).replace('[','').replace(']','')

  open('document.html', 'w').write(doc.replace('/*data*/', data).replace('/*colors*/', colors))
  Html2Image(custom_flags=['--virtual-time-budget=5000', '--default-background-color=0']).screenshot(html_file='document.html', save_as='chart.png', size=(600,600))
  show = input(color.BOLD+color.BLUE+'Would you like to keep the document.html used by the program? [Y/n]'+color.END)

  if show == 'n' or show == 'N':
    os.remove('document.html')
    exit(0)
  else:
    exit(0)

if __name__ == '__main__':
  prompt = PyInquirer.prompt([
    {
        'type':'list',
        'name':'choice',
        'message':'What do you want to do?',
        'choices':[
            'Create a meme popularity pie chart',
            'Fetch information for a single meme',
            'Exit'
        ]
    }
  ])

  if prompt['choice'] == 'Create a meme popularity pie chart':
    make_pie()
  elif prompt['choice'] == 'Fetch information for a single meme':
    predict_meme()
  else:
    exit(0)
