from unittest import result
import requests
import pytest
from flask import request



BASE = "http://127.0.0.1:5000/"

body={
  "title": "string",
  "id_opp": 0,
  "id_prospect": 0,
  "id_affaire": "1",
  "commentaire": "string",
  "date_creation": "2022-08-19T13:45:22.987Z",
  "last_update": "2022-08-19T13:45:22.987Z",
  "date_traitement": "2022-08-19T13:45:22.987Z",
  "date_limit": "2022-08-19",
  "createur": 0,
  "affect": 0,
  "categorie": 0,
  "statut": 0,
  "url_files": "string",
  "date_fermeture": "2022-08-19T13:45:22.987Z",
  "alerter": 0,
  "form": "string",
  "date_reouverture": "2022-08-19T13:45:22.987Z"
}

update={
   "id":4,
  "title": "string",
  "id_opp": 0,
  "id_prospect": 0,
  "id_affaire": "1",
  "commentaire": "string",
  "date_creation": "2022-08-19T13:45:22.987Z",
  "last_update": "2022-08-19T13:45:22.987Z",
  "date_traitement": "2022-08-19T13:45:22.987Z",
  "date_limit": "2022-08-19",
  "createur": 0,
  "affect": 0,
  "categorie": 0,
  "statut": 0,
  "url_files": "string",
  "date_fermeture": "2022-08-19T13:45:22.987Z",
  "alerter": 0,
  "form": "string",
  "date_reouverture": "2022-08-19T13:45:22.987Z"
}



#----------------------------GET----------------------------------------------------
def test_get_info_specifique_ticket_id():
    result = requests.get("http://127.0.0.1:5000/get_info_specifique_ticket/10000").json()
    assert result["error"]==True and result["message"]=="aucune ticket correspond a id : 10000"


def test_get_info_specifique_ticket_json():
    result = requests.get("http://127.0.0.1:5000/get_info_specifique_ticket/3").json()
    #import pdb;pdb.set_trace()
    assert result["error"]==True and result["form"]["error"]=="impossible de decoder le JSON. Verifiez le format des données dans la bdd"



#-----------------------POST---------------------------------------------------------
def test_add_new_ticket_1():
    result=requests.post("http://127.0.0.1:5000/add_ticket",json=body).json()
    assert result["error"]==True and result["message"]=="parametre non present"



def test_add_new_ticket_json():
    result=requests.post("http://127.0.0.1:5000/add_ticket",json=body).json()
    assert result["error"]==True and result["message"]=="body application/json non present"

def test_add_new_ticket():
    result=requests.post("http://127.0.0.1:5000/add_ticket",json=body).json()
    assert result["error"]==True and result["message"]=="Erreur d'ajout du ticket"


#---------------------------------PUT-------------------------------------------------
#test
def test_update_ticket():
    result = requests.put("http://127.0.0.1:5000/update_ticket",json=update).json()
    assert result["erreur"]== True and result["messsage"]=="paramétre non présent"

def test_update_ticket_id():
    result=requests.put("http://127.0.0.1:5000/update_ticket",json={"id":update["id"]}).json()
    assert result["error"]== True and result["messsage"]=="Aucune ticket correspond au id"+str(update["id"])


def test_update_ticket_prospect():
    result=requests.put("http://127.0.0.1:5000/update_ticket",json={"id_prospect":update["id_prospect"]}).json()
    assert result["error"]== True and result["messsage"]=="Aucune prospect ticket correspond au id prospect"+str(update["id_prospect"])


def test_update_ticket_categorie():
    result=requests.put("http://127.0.0.1:5000/update_ticket",json={"categorie":update["categorie"]}).json()
    assert result["error"]== True and result["messsage"]=="Aucune categorie ticket correspond au categorie"+str(update["categorie"])

def test_update_ticket_affect():
    result=requests.put("http://127.0.0.1:5000/update_ticket",json={"affect":update["affect"]}).json()
    assert result["error"]== True and result["messsage"]=="Aucune user correspond au id"+str(update["affect"])




