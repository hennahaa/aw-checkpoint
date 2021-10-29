import requests
from google.cloud import storage

def kirjoita_data():
  r = requests.get("https://2ri98gd9i4.execute-api.us-east-1.amazonaws.com/dev/academy-checkpoint2-json")

  data = r.json()
  lista = []

  for i in range(len(data["items"])):
    lista.append(data["items"][i]["parameter"])

  try:
    with open("checkpoint.txt", "w") as tiedosto:
      for nimi in lista:
        tiedosto.write(nimi+"\n")
    print(f"Data kirjoitettu tiedostoon checkpoint.txt")
  except IOError:
    print("Tiedoston kirjoittamisessa kävi jotain hupsua!")

def luo_ampari(ampari_nimi:str):
  storage_client = storage.Client()

  bucket = storage_client.bucket(ampari_nimi)
  bucket.storage_class = "STANDARD"
  new_bucket = storage_client.create_bucket(bucket, location="us")

  print(f"Luotiin bucket {new_bucket.name} sijaintiin {new_bucket.location} ja sillä on storage class {new_bucket.storage_class}")


def laita_ampariin(ampari_nimi:str,tiedosto_nimi:str,uusi_nimi:str):
  
  storage_client = storage.Client()
  bucket = storage_client.bucket(ampari_nimi)
  blob = bucket.blob(uusi_nimi)

  blob.upload_from_filename(tiedosto_nimi)

  print(f"Tiedosto {tiedosto_nimi} ladattu bucketiin {ampari_nimi} nimellä {uusi_nimi}.")

kirjoita_data()
luo_ampari("aw-checkpoint-bucket")
laita_ampariin("aw-checkpoint-bucket","checkpoint.txt","checkpoint1")