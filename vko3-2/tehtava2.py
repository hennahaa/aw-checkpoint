import argparse
from google.cloud import storage
import os.path
import time

def lataa_amparista(amparinimi: str, tiedostonimi:str, uusi_nimi:str):

    storage_client = storage.Client()
    bucket = storage_client.bucket(amparinimi)

    blob = bucket.blob(tiedostonimi)
    blob.download_to_filename(uusi_nimi)

    print(f"Ladattiin filu {tiedostonimi} ämpäristä {amparinimi} nimellä {uusi_nimi}.")

def tulostetaan_rivit(tied:str):
  
  lista = []
  #luetaan tiedosto
  try:
    with open(tied) as tiedosto:
      for rivi in tiedosto:
        rivi = rivi.replace("\n", "")
        lista.append(rivi)
  except IOError:
    print("Tiedoston avaamisessa kävi jotain hupsua!")

  #järjestetään sisältö, ensin sanan pituus sitten sanan aakkosjärjestys
  def jarjestys(str):
    return len(str), str.lower()

  jarjestetty_lista = sorted(lista, key=jarjestys)

  print("Pyydetty määrä rivejä, lyhyimmästä pisimpään:")
  for i in range(len(jarjestetty_lista)):
    if i < args.rivit:
      print(jarjestetty_lista[i])


checkpoint_tiedosto = "checkpoint.txt"

parser = argparse.ArgumentParser()
parser.add_argument("rivit", help="tulostettavien rivien määrä", type=int)
args = parser.parse_args()

lataa_amparista("aw-checkpoint-bucket", "checkpoint1", checkpoint_tiedosto)

#odotellaan, kunnes tieodosto on luettu ja kansiossa vko3-2
while not os.path.exists(checkpoint_tiedosto):
    time.sleep(1)

if os.path.isfile(checkpoint_tiedosto):
    tulostetaan_rivit(checkpoint_tiedosto)
else:
    raise ValueError(f"{checkpoint_tiedosto} ei ole tiedosto!")