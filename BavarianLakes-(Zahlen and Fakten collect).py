import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm #progress bar
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sys import exit

start_time = time.time()

webpages = ['https://www.wassertemperatur.org/arendsee/',
'https://www.wassertemperatur.org/attersee/',
'https://www.wassertemperatur.org/deutschland/bayern/attlesee/',
'https://www.wassertemperatur.org/deutschland/bayern/auensee/',
'https://www.wassertemperatur.org/oesterreich/ausee/',
'https://www.wassertemperatur.org/deutschland/bayern/autobahnsee/',
'https://www.wassertemperatur.org/deutschland/bayern/badsee/',
'https://www.wassertemperatur.org/seen/schweiz/baldeggersee/',
'https://www.wassertemperatur.org/deutschland/bayern/bannwaldsee/',
'https://www.wassertemperatur.org/deutschland/sachsen-anhalt/barleber-see/',
'https://www.wassertemperatur.org/deutschland/bayern/barmsee/',
'https://www.wassertemperatur.org/seen/schweiz/bielersee/',
'https://www.wassertemperatur.org/deutschland/hessen/aartalsee/',
'https://www.wassertemperatur.org/deutschland/nrw/aasee/',
'https://www.wassertemperatur.org/deutschland/bayern/abtsdorfer-see/',
'https://www.wassertemperatur.org/oesterreich/afritzer-see/',
'https://www.wassertemperatur.org/oesterreich/aichwaldsee/',
'https://www.wassertemperatur.org/deutschland/nrw/alberssee/',
'https://www.wassertemperatur.org/seen/schweiz/alpnachersee/',
'https://www.wassertemperatur.org/altmuehlsee/',
'https://www.wassertemperatur.org/ammersee/',
'https://www.wassertemperatur.org/deutschland/nrw/biggesee/',
'https://www.wassertemperatur.org/deutschland/bayern/blaibacher-see/',
'https://www.wassertemperatur.org/deutschland/nrw/bleibtreusee/',
'https://www.wassertemperatur.org/bodensee/',
'https://www.wassertemperatur.org/bolsenasee/',
'https://www.wassertemperatur.org/braccianosee/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/breitenauer-see/',
'https://www.wassertemperatur.org/oesterreich/brennsee/',
'https://www.wassertemperatur.org/seen/schweiz/brienzersee/',
'https://www.wassertemperatur.org/brombachsee/',
'https://www.wassertemperatur.org/seen/schweiz/burgaeschisee/',
'https://www.wassertemperatur.org/seen/schweiz/canovasee/',
'https://www.wassertemperatur.org/seen/schweiz/caumasee/',
'https://www.wassertemperatur.org/chiemsee/',
'https://www.wassertemperatur.org/comer-see/',
'https://www.wassertemperatur.org/seen/schweiz/davosersee/',
'https://www.wassertemperatur.org/deutschland/hessen/diemelsee/',
'https://www.wassertemperatur.org/deutschland/hessen/dutenhofener-see/',
'https://www.wassertemperatur.org/deutschland/nrw/duerener-badesee/',
'https://www.wassertemperatur.org/deutschland/bayern/echinger-see/',
'https://www.wassertemperatur.org/deutschland/nrw/echtzer-see/',
'https://www.wassertemperatur.org/edersee/',
'https://www.wassertemperatur.org/seen/schweiz/egelsee/',
'https://www.wassertemperatur.org/deutschland/bayern/eibsee/',
'https://www.wassertemperatur.org/deutschland/schleswig-holstein/einfelder-see/',
'https://www.wassertemperatur.org/deutschland/bayern/eixendorfer-see/',
'https://www.wassertemperatur.org/deutschland/schleswig-holstein/eutiner-see/',
'https://www.wassertemperatur.org/deutschland/nrw/eyller-see/',
'https://www.wassertemperatur.org/faaker-see/',
'https://www.wassertemperatur.org/deutschland/nrw/feldmarksee/',
'https://www.wassertemperatur.org/deutschland/bayern/feringasee/',
'https://www.wassertemperatur.org/deutschland/bayern/fichtelsee/',
'https://www.wassertemperatur.org/oesterreich/flatschacher-see/',
'https://www.wassertemperatur.org/deutschland/bayern/fohnsee/',
'https://www.wassertemperatur.org/forggensee/',
'https://www.wassertemperatur.org/oesterreich/forstsee/',
'https://www.wassertemperatur.org/deutschland/bayern/freibergsee/',
'https://www.wassertemperatur.org/deutschland/bayern/friedenhain-see/',
'https://www.wassertemperatur.org/deutschland/bayern/froschhauser-see/',
'https://www.wassertemperatur.org/deutschland/bayern/funtensee/',
'https://www.wassertemperatur.org/oesterreich/fuschlsee/',
'https://www.wassertemperatur.org/deutschland/nrw/fuehlinger-see/',
'https://www.wassertemperatur.org/gardasee/',
'https://www.wassertemperatur.org/deutschland/sachsen-anhalt/geiseltalsee/',
'https://www.wassertemperatur.org/genfer-see/',
'https://www.wassertemperatur.org/deutschland/bayern/geroldsee/',
'https://www.wassertemperatur.org/deutschland/sachsen-anhalt/goitzschesee/',
'https://www.wassertemperatur.org/oesterreich/gosausee/',
'https://www.wassertemperatur.org/oesterreich/grabensee/',
'https://www.wassertemperatur.org/seen/schweiz/greifensee/',
'https://www.wassertemperatur.org/deutschland/bayern/griessee/',
'https://www.wassertemperatur.org/deutschland/nrw/grossenbaumer-see/',
'https://www.wassertemperatur.org/deutschland/bayern/grosser-alpsee/',
'https://www.wassertemperatur.org/deutschland/bayern/grubsee/',
'https://www.wassertemperatur.org/deutschland/bayern/gruentensee/',
'https://www.wassertemperatur.org/oesterreich/goesselsdorfer-see/',
'https://www.wassertemperatur.org/oesterreich/hafnersee/',
'https://www.wassertemperatur.org/deutschland/bayern/hahnenkammsee/',
'https://www.wassertemperatur.org/oesterreich/hallstaettersee/',
'https://www.wassertemperatur.org/seen/schweiz/hallwilersee/',
'https://www.wassertemperatur.org/deutschland/bayern/hammersee/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/hardtsee/',
'https://www.wassertemperatur.org/deutschland/nrw/heider-bergsee/',
'https://www.wassertemperatur.org/deutschland/schleswig-holstein/hemmelsdorfer-see/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/hemsbacher-wiesensee/',
'https://www.wassertemperatur.org/deutschland/nrw/hennesee/',
'https://www.wassertemperatur.org/oesterreich/heratinger-see/',
'https://www.wassertemperatur.org/deutschland/bayern/hintersee/',
'https://www.wassertemperatur.org/oesterreich/hintersee/',
'https://www.wassertemperatur.org/deutschland/bayern/hollerner-see/',
'https://www.wassertemperatur.org/deutschland/bayern/hopfensee/',
'https://www.wassertemperatur.org/deutschland/bayern/hoeglwoerther-see/',
'https://www.wassertemperatur.org/seen/schweiz/huettwilersee/',
'https://www.wassertemperatur.org/idrosee/',
'https://www.wassertemperatur.org/deutschland/bayern/igelsbachsee/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/illmensee/',
'https://www.wassertemperatur.org/bodensee/immenstaad-am-bodensee/',
'https://www.wassertemperatur.org/oesterreich/irrsee/',
'https://www.wassertemperatur.org/iseosee/',
'https://www.wassertemperatur.org/deutschland/schleswig-holstein/itzstedter-see/',
'https://www.wassertemperatur.org/deutschland/nrw/kaarster-see/',
'https://www.wassertemperatur.org/deutschland/bayern/kahler-see/',
'https://www.wassertemperatur.org/kalterer-see/#AktuelleWassertemperatur',
'https://www.wassertemperatur.org/deutschland/bayern/karlsfelder-see/',
'https://www.wassertemperatur.org/seen/schweiz/katzensee/',
'https://www.wassertemperatur.org/oesterreich/keutschacher-see/',
'https://www.wassertemperatur.org/deutschland/bayern/kirchsee/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/kirnbergsee/',
'https://www.wassertemperatur.org/deutschland/bayern/klausensee/',
'https://www.wassertemperatur.org/deutschland/bayern/kleiner-alpsee/',
'https://www.wassertemperatur.org/kleiner-brombachsee/',
'https://www.wassertemperatur.org/oesterreich/kleinsee/',
'https://www.wassertemperatur.org/klopeiner-see/',
'https://www.wassertemperatur.org/seen/schweiz/kloentalersee/',
'https://www.wassertemperatur.org/kochelsee/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/krauchenwieser-see/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/kressbachsee/',
'https://www.wassertemperatur.org/deutschland/bayern/kuhsee/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/koenigseggsee/',
'https://www.wassertemperatur.org/koenigssee/',
'https://www.wassertemperatur.org/deutschland/schleswig-holstein/kuechensee/',
'https://www.wassertemperatur.org/oesterreich/langbathsee/',
'https://www.wassertemperatur.org/deutschland/hessen/langener-waldsee/',
'https://www.wassertemperatur.org/lago-maggiore/',
'https://www.wassertemperatur.org/deutschland/bayern/langwieder-see/',
'https://www.wassertemperatur.org/seen/schweiz/lauerzersee/',
'https://www.wassertemperatur.org/ledrosee/',
'https://www.wassertemperatur.org/deutschland/bayern/leitgeringer-see/',
'https://www.wassertemperatur.org/oesterreich/linsendorfer-see/',
'https://www.wassertemperatur.org/luganer-see/',
'https://www.wassertemperatur.org/seen/schweiz/lungerersee/',
'https://www.wassertemperatur.org/deutschland/bayern/lusssee/',
'https://www.wassertemperatur.org/oesterreich/laengsee/',
'https://www.wassertemperatur.org/deutschland/bayern/loedensee/',
'https://www.wassertemperatur.org/deutschland/schleswig-holstein/luetauer-see/',
'https://www.wassertemperatur.org/seen/schweiz/luetzelsee/',
'https://www.wassertemperatur.org/oesterreich/maltschacher-see/',
'https://www.wassertemperatur.org/oesterreich/mattsee/',
'https://www.wassertemperatur.org/deutschland/hessen/meinhardsee/',
'https://www.wassertemperatur.org/millstaetter-see/',
'https://www.wassertemperatur.org/deutschland/bayern/mittersee/',
'https://www.wassertemperatur.org/mondsee/',
'https://www.wassertemperatur.org/seen/schweiz/moossee/',
'https://www.wassertemperatur.org/deutschland/bayern/murner-see/',
'https://www.wassertemperatur.org/seen/schweiz/murtensee/',
'https://www.wassertemperatur.org/deutschland/nrw/moehnesee/',
'https://www.wassertemperatur.org/deutschland/bayern/neubaeuer-see/',
'https://www.wassertemperatur.org/seen/schweiz/neuenburgersee/',
'https://www.wassertemperatur.org/deutschland/hessen/neuenhainer-see/',
'https://www.wassertemperatur.org/oesterreich/neufelder-see/',
'https://www.wassertemperatur.org/neusiedler-see/',
'https://www.wassertemperatur.org/deutschland/sachsen-anhalt/neustaedter-see/',
'https://www.wassertemperatur.org/deutschland/hessen/nidda-stausee/',
'https://www.wassertemperatur.org/deutschland/bayern/niedersonthofener-see/',
'https://www.wassertemperatur.org/deutschland/hessen/niederweimarer-see/',
'https://www.wassertemperatur.org/deutschland/sachsen-anhalt/niegripper-see/',
'https://www.wassertemperatur.org/nordsee/',
'https://www.wassertemperatur.org/deutschland/bayern/oberer-lechsee/',
'https://www.wassertemperatur.org/deutschland/bayern/obersee/',
'https://www.wassertemperatur.org/oesterreich/obertrumer-see/',
'https://www.wassertemperatur.org/deutschland/bayern/obinger-see/',
'https://www.wassertemperatur.org/seen/schweiz/oeschinensee/',
'https://www.wassertemperatur.org/oesterreich/offensee/',
'https://www.wassertemperatur.org/ortasee/',
'https://www.wassertemperatur.org/ossiacher-see/',
'https://www.wassertemperatur.org/ostsee/',
'https://www.wassertemperatur.org/deutschland/nrw/otto-maigler-see/',
'https://www.wassertemperatur.org/deutschland/bayern/perlsee/',
'https://www.wassertemperatur.org/seen/schweiz/pfaeffikersee/',
'https://www.wassertemperatur.org/deutschland/bayern/pilsensee/',
'https://www.wassertemperatur.org/oesterreich/pirkdorfer-see/',
'https://www.wassertemperatur.org/oesterreich/pleschinger-see/',
'https://www.wassertemperatur.org/deutschland/schleswig-holstein/ploener-see/',
'https://www.wassertemperatur.org/oesterreich/pressegger-see/',
'https://www.wassertemperatur.org/bodensee/radolfzell/',
'https://www.wassertemperatur.org/ratzeburger-see/',
'https://www.wassertemperatur.org/oesterreich/rauschelesee/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/riedsee/',
'https://www.wassertemperatur.org/deutschland/bayern/riegsee/',
'https://www.wassertemperatur.org/rothsee/',
'https://www.wassertemperatur.org/deutschland/bayern/rottachsee/',
'https://www.wassertemperatur.org/deutschland/nrw/rursee/',
'https://www.wassertemperatur.org/seen/schweiz/sarnersee/',
'https://www.wassertemperatur.org/schaalsee/',
'https://www.wassertemperatur.org/schierensee/',
'https://www.wassertemperatur.org/schliersee/',
'https://www.wassertemperatur.org/schluchsee/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/schluechtsee/',
'https://www.wassertemperatur.org/deutschland/bayern/schwansee/',
'https://www.wassertemperatur.org/seen/schweiz/schwarzsee/',
'https://www.wassertemperatur.org/seen/schweiz/seealpsee/',
'https://www.wassertemperatur.org/seen/schweiz/sempachersee/',
'https://www.wassertemperatur.org/seen/schweiz/sihlsee/',
'https://www.wassertemperatur.org/seen/schweiz/silsersee/',
'https://www.wassertemperatur.org/seen/schweiz/silvaplanersee/',
'https://www.wassertemperatur.org/simssee/',
'https://www.wassertemperatur.org/deutschland/hessen/singliser-see/',
'https://www.wassertemperatur.org/oesterreich/sonnegger-see/',
'https://www.wassertemperatur.org/deutschland/nrw/sorpesee/',
'https://www.wassertemperatur.org/deutschland/bayern/spitzingsee/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/st-leoner-see/',
'https://www.wassertemperatur.org/staffelsee/',
'https://www.wassertemperatur.org/starnberger-see/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/steeger-see/',
'https://www.wassertemperatur.org/deutschland/bayern/steinberger-see/',
'https://www.wassertemperatur.org/oesterreich/steinbrunner-see/',
'https://www.wassertemperatur.org/deutschland/bayern/steinsee/',
'https://www.wassertemperatur.org/deutschland/nrw/stemmer-see/',
'https://www.wassertemperatur.org/deutschland/nrw/straberger-see/',
'https://www.wassertemperatur.org/deutschland/bayern/sulzberger-see/',
'https://www.wassertemperatur.org/deutschland/bayern/sylvensteinsee/',
'https://www.wassertemperatur.org/deutschland/bayern/tachinger-see/',
'https://www.wassertemperatur.org/tegernsee/',
'https://www.wassertemperatur.org/deutschland/nrw/tenderingssee/',
'https://www.wassertemperatur.org/deutschland/bayern/thumsee/',
'https://www.wassertemperatur.org/seen/schweiz/thunersee/',
'https://www.wassertemperatur.org/titisee/',
'https://www.wassertemperatur.org/deutschland/nrw/toeppersee/',
'https://www.wassertemperatur.org/lago-trasimeno/',
'https://www.wassertemperatur.org/oesterreich/traunsee/',
'https://www.wassertemperatur.org/oesterreich/turnersee/',
'https://www.wassertemperatur.org/deutschland/hessen/twistesee/',
'https://www.wassertemperatur.org/seen/schweiz/tuerlersee/',
'https://www.wassertemperatur.org/deutschland/nrw/unterbacher-see/',
'https://www.wassertemperatur.org/deutschland/bayern/unterschleissheimer-see/',
'https://www.wassertemperatur.org/deutschland/bayern/untreusee/',
'https://www.wassertemperatur.org/oesterreich/urbansee/',
'https://www.wassertemperatur.org/seen/schweiz/urnersee/',
'https://www.wassertemperatur.org/oesterreich/vassacher-see/',
'https://www.wassertemperatur.org/vierwaldstaettersee/',
'https://www.wassertemperatur.org/waginger-see/',
'https://www.wassertemperatur.org/deutschland/baden-wuerttemberg/waidsee/',
'https://www.wassertemperatur.org/walchensee/',
'https://www.wassertemperatur.org/deutschland/bayern/waldsee/',
'https://www.wassertemperatur.org/walensee/',
'https://www.wassertemperatur.org/oesterreich/wallersee/',
'https://www.wassertemperatur.org/deutschland/nrw/wankumer-heidesee/',
'https://www.wassertemperatur.org/bodensee/obersee/',
'https://www.wassertemperatur.org/bodensee/untersee/',
'https://www.wassertemperatur.org/bodensee/ueberlinger-see/',
'https://www.wassertemperatur.org/weissensee/',
'https://www.wassertemperatur.org/deutschland/bayern/weitsee/',
'https://www.wassertemperatur.org/deutschland/bayern/weissensee/',
'https://www.wassertemperatur.org/deutschland/bayern/weissenstaedter-see/',
'https://www.wassertemperatur.org/deutschland/bayern/wesslinger-see/',
'https://www.wassertemperatur.org/deutschland/nrw/wisseler-see/',
'https://www.wassertemperatur.org/wolfgangsee/',
'https://www.wassertemperatur.org/deutschland/bayern/wolfsee/',
'https://www.wassertemperatur.org/seen/schweiz/waegitalersee/',
'https://www.wassertemperatur.org/worthersee/',
'https://www.wassertemperatur.org/woerthsee/',
'https://www.wassertemperatur.org/deutschland/nrw/xantener-suedsee/',
'https://www.wassertemperatur.org/oesterreich/zeller-see/',
'https://www.wassertemperatur.org/deutschland/bayern/zellersee/',
'https://www.wassertemperatur.org/seen/schweiz/zugersee/',
'https://www.wassertemperatur.org/deutschland/nrw/zuelpicher-see/',
'https://www.wassertemperatur.org/zuerichsee/',
'https://www.wassertemperatur.org/seen/schweiz/aegerisee/'
]

webpagefounds=[]   # store results...

for webpage in webpages:
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, features="lxml")

    #regexp pattern to find Zahlen
    pattern = r"<h2>Zahlen\s*&amp;\s*Fakten\s+.*?</h2>"
    match = re.search(pattern, page.text)
    if match:
        # Find the <h2> tag with the text 'Zahlen & Fakten'
        heading = soup.find('h2', text=lambda t: t and t.startswith('Zahlen & Fakten'))
        # Get the <ul> list that follows the heading
        facts_list = heading.find_next('ul')
        # Extract the list items and store in a list
        facts = [fact.text for fact in facts_list.find_all('li')]
        # Print the list of facts    #  print(facts)
        facts.insert(0, webpage)
        # Add list of Facts to the findings:
        webpagefounds.append(facts)
    else:
        webpagefounds.append([webpage])

#    webpagefounds.append(match)
print(f'Checking all Pages took: {round(time.time()-start_time, 2)} sec')
for everypage in webpagefounds:
    print(everypage)


'''
for line in webpagefounds:
    print(bool(line), line)
    #print('\n')


link1 = 'https://www.wassertemperatur.org/deutschland/hessen/twistesee/'
page1 = requests.get(link1)
soup1 = BeautifulSoup(page1.text, features="lxml")

#regexp pattern to find Zahlen

pattern = r"<h2>Zahlen\s*&amp;\s*Fakten\s+.*?</h2>"
match = re.search(pattern, page1.text)
if match:
    print('Here is the match ! ', bool(match), match)
    # Find the <h2> tag with the text 'Zahlen & Fakten'
    heading = soup1.find('h2', text=lambda t: t and t.startswith('Zahlen & Fakten'))
    # Get the <ul> list that follows the heading
    facts_list = heading.find_next('ul')
    # Extract the list items and store in a list
    facts = [fact.text for fact in facts_list.find_all('li')]
    # Print the list of facts
    print(facts)
'''

# Initialize an empty dictionary
lake_data_dict = {}
key_count_dict = {}

for lake in webpagefounds:
    # The first item in the list is the URL
    url = lake[0]
    # The rest are key-value pairs, we need to split them by ":"
    characteristics = {}

    for attribute in lake[1:]:
        if ":" in attribute:
            key, value = attribute.split(": ", 1)  # Split into two parts only (key and value)
            characteristics[key] = value

            # Track occurrences of each key (characteristic)
            if key in key_count_dict:
                key_count_dict[key] += 1
            else:
                key_count_dict[key] = 1


    # Add the URL as the key and characteristics dictionary as the value
    lake_data_dict[url] = characteristics

# Print the resulting dictionary
for url, characteristics in lake_data_dict.items():
    print(f"{url}:")
    for key, value in characteristics.items():
        print(f"  {key}: {value}")

# Print the unique list of keys along with their count
print("Unique List of Keys (Characteristics) and their Count:\n")
for key, count in key_count_dict.items():
    print(f"{key}: {count}")
