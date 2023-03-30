from asyncio.windows_events import NULL
from email.policy import default
from importlib.metadata import requires
import json
from msilib import Table
from multiprocessing.sharedctypes import Value
from tkinter import N
from typing_extensions import Required
from marshmallow import fields, Schema, post_load,post_dump
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,jsonify,make_response,Response
from sqlalchemy import VARCHAR, ForeignKey
from datetime import date, datetime
from ntpath import join
from cgitb import text
from dataclasses import dataclass
import hashlib
from .utile import md5






db=SQLAlchemy()




class UserSchema_Roles(Schema):
    id=fields.Integer(required=True)
    role=fields.String(required=True)

@dataclass
class Roles(db.Model):
    id:int
    role:VARCHAR=None

    __name_table__="roles"
    id=db.Column(db.Integer(),primary_key=True)
    role=db.Column(db.String(100),default=NULL)



class UserSchema_Ville(Schema):
    id = fields.String(required=True)
    nom_comm = fields.String(required=True)


@dataclass
class Ville(db.Model):
    id : VARCHAR
    nom_comm : VARCHAR = None

    __name_table__="ville"
    id=db.Column(db.String(11),primary_key = True)
    nom_comm=db.Column(db.String(100),default = NULL)



class UserSchema_Users(Schema):
    id=fields.Integer(required = True)
    nom = fields.String(required=True)
    prenom = fields.String(required=True)
    mail = fields.String(required=True)
    photo=fields.String(required=True)
    id_session=fields.String(required=True)
    roles=fields.Nested(UserSchema_Roles)
    super_admin=fields.Integer(required=True)
    admin_restreint=fields.Integer(required=True)
    role_auto=fields.String(required=True)
    mobile=fields.String(required=True)
    entreprise_id=fields.Integer(required=True)

@dataclass
class Users(db.Model):
    id : int
    nom: VARCHAR = None
    prenom : VARCHAR = None
    mail: VARCHAR=None
    photo : VARCHAR=None
    id_session:VARCHAR=None
    role:int=None
    super_admin:int=None
    admin_restreint:int=None
    role_auto:VARCHAR=None
    mobile:VARCHAR=None
    entreprise_id:int=None

    __name_table__ = "users"
    id=db.Column(db.Integer(),primary_key=True)
    nom = db.Column(db.String(45),default = NULL)
    prenom = db.Column(db.String(45),default = NULL)
    mail = db.Column(db.String(45),default = NULL)
    photo= db.Column(db.String(1000),default = NULL)
    id_session=db.Column(db.String(255),default = NULL)

    role=db.Column(db.Integer(),ForeignKey("roles.id"),default=NULL)
    roles=db.relationship("Roles",foreign_keys=[role],backref = "users_roles_1")

    super_admin=db.Column(db.Integer(),default = NULL)
    admin_restreint=db.Column(db.Integer(),default = NULL)
    role_auto=db.Column(db.String(255),default = NULL)
    mobile=db.Column(db.String(50),default = NULL)
    entreprise_id=db.Column(db.Integer(),default = NULL)

    def get(self,_id):
        res=db.session.query(Users).filter(
        self.id==_id)
        sch=UserSchema_Users()
        q=sch.dump(res)[0]
        return q

    def get_id_user_by_session(self):
        req=db.session.query(Users).filter(
        Users.id_session==self.id_session)
        sch=UserSchema_Users(many=True,only=["id"])
        res=sch.dump(req)
        if res !=[]:
            return res[0]["id"]
        return 0

    def get_prenom_id(self,affect):
        req=db.session.query(Users).filter(
        Users.id==affect)
        sch=UserSchema_Users(many=True,only=["prenom"])
        res=sch.dump(req)
        return res

    def get_mail_id(self,affect):
        req=db.session.query(Users).filter(
        Users.id==affect)
        sch=UserSchema_Users(many=True,only=["mail"])
        res=sch.dump(req)
        if res !=[]:
            return res[0]["mail"]
        return ""


    def getUserId(self,id_session):
        req=db.session.query(Users).join(
        Roles,Roles.id==Users.role).filter(
        Users.id_session==id_session)
        sch=UserSchema_Users(many=True,exclude=["photo","id_session"])
        res=sch.dump(req)
        if res!=[]:
            for d in res:
                d1={
                    "user_full_name":d["nom"]+" "+d["prenom"],
                    "id_role":d["roles"]["id"],
                    "role":d["roles"]["role"]
                }
                del d["roles"]
                del d["nom"]
                del d["prenom"]
                d.update(d1)
            return res
        return []



class UserSchema_Campagnes(Schema):
    id = fields.Integer(required = True)


@dataclass
class Campagnes(db.Model):
    id : int

    __name_table__ = "campagnes"
    id=db.Column(db.Integer(),primary_key = True)


class UserSchema_Adresses(Schema):
    id = fields.Integer(required = True)
    streetName = fields.String(required=True)
    streetNumber = fields.String(required=True)
    CP = fields.String(required=True)
    villes = fields.Nested(UserSchema_Ville)


@dataclass
class Adresses(db.Model):
    id : int
    streetName : VARCHAR = None
    streetNumber : VARCHAR = None
    CP : VARCHAR = None
    ville : VARCHAR = None

    __name_table__ ="adresses"
    id= db.Column(db.Integer(),primary_key = True)
    streetName = db.Column(db.String(150),default = NULL)
    streetNumber = db.Column(db.String(200),default = NULL)
    CP=db.Column(db.String(5),default = NULL)

    ville = db.Column(db.String(11),ForeignKey("ville.id"),default = NULL)
    villes = db.relationship("Ville",foreign_keys=[ville],backref="addresses_ville")

class UserSchema_Prospects(Schema):
    id = fields.Integer(required = True)
    name = fields.String(required=True)
    surname = fields.String(required=True)
    tel=fields.String(required=True)
    tel2=fields.String(required=True)
    mobile = fields.String(required=True)
    adresse_mail = fields.String(required=True)
    description = fields.String(required=True)
    campagnes_1 = fields.Nested(UserSchema_Campagnes)
    campagnes_2 = fields.Nested(UserSchema_Campagnes)
    adresses = fields.Nested(UserSchema_Adresses)
    last_update=fields.Time(required = True)
    fiche_dec = fields.String(required=True)
    civilite = fields.String(required=True)
    DN = fields.Date(required = True)
    situation = fields.String(required=True)
    nb_enfants = fields.Integer(required=True)
    securite_sociale = fields.String(required=True)
    short_description = fields.String(required=True)
    users = fields.Nested(UserSchema_Users)
    password = fields.String(required=True)
    rib_prelevemer = fields.String(required=True)
    rib_prestation = fields.String(required=True)



@dataclass
class Prospects(db.Model):
    id : int
    name : VARCHAR = None
    surname : VARCHAR = None
    tel : VARCHAR = None
    tel2 : VARCHAR = None
    mobile : VARCHAR = None
    adresse_mail : VARCHAR = None
    description : text = None
    first_campagne : int = None
    last_campagne : int = None
    loaction : int = None
    last_update : datetime.time = None
    fiche_dec : text = None
    civilite : VARCHAR = None
    DN : datetime = None
    situation : VARCHAR = None
    nb_enfants : int = None
    securite_sociale : VARCHAR = None
    short_description : VARCHAR = None
    created_by : int = None
    password : VARCHAR = None
    rib_prelevemer : VARCHAR = None
    rib_prestation : VARCHAR = None
    

    __name_table__ = "prospects"
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(45),default = NULL)
    surname = db.Column(db.String(45),default = NULL)
    tel = db.Column(db.String(20),default = NULL)
    tel2 = db.Column(db.String(20),default = NULL)
    mobile = db.Column(db.String(20),default = NULL)
    adresse_mail = db.Column(db.String(45),default = NULL)
    description = db.Column(db.String(),default = NULL)

    loaction = db.Column(db.Integer(),ForeignKey("adresses.id"),default = NULL)
    adresses = db.relationship("Adresses", foreign_keys=[loaction], backref="prospects_adresse")

    first_campagne = db.Column(db.Integer(),ForeignKey("campagnes.id"),default = NULL)
    campagnes_1 = db.relationship("Campagnes",foreign_keys=[first_campagne],backref = "prospects_campagne_1")

    last_campagne = db.Column(db.Integer(),ForeignKey("campagnes.id"),default = NULL)
    campagnes_2 =db.relationship("Campagnes",foreign_keys=[last_campagne],backref = "prospects_campagne_2")

    created_by = db.Column(db.Integer(),ForeignKey("users.id"),default = NULL)
    users = db.relationship("Users",foreign_keys=[created_by],backref = "prospects_user")

    last_update = db.Column(db.Time())
    fiche_dec = db.Column(db.String,default = NULL)
    civilite = db.Column(db.String(10),default = NULL)
    DN = db.Column(db.Date(),default = NULL)
    situation = db.Column(db.String(50),default = NULL)
    nb_enfants = db.Column(db.Integer(),default = NULL)
    securite_sociale = db.Column(db.String(50),default = NULL)
    short_description = db.Column(db.String(255),default = NULL)
    password = db.Column(db.String(45),default = NULL)
    rib_prelevemer = db.Column(db.String(100),default = NULL)
    rib_prestation = db.Column(db.String(100),default = NULL)

    

    def get(id):
        res=db.session.query(Prospects).join(
            Adresses, Adresses.id==Prospects.loaction
            ).join(
                Prospects, Ticket.id_prospect==Prospects.id
            ).join(
                Ville, Ville.id==Adresses.ville).filter(
                Ticket.id==id
            )
        sch=UserSchema_Prospects(many=True)
        req=sch.dump(res)
        q=req[0]
        d={"id":q["id"],
           "name":q["name"],
           "surname":q["surname"],
           "DN":q["DN"],
           "situation":q["situation"],
           "nb_enfants":q["nb_enfants"],
           "adresse_mail":q["adresse_mail"],
           "tel":q["tel"],
           "tel2":q["tel2"],
           "mobile":q["mobile"],
           "description":q["description"],
           "short_description":q["short_description"],
           "nom_comm":q["villes"]["nom_comm"],
           "CP":q["adresses"]["CP"],
           "streetName":q["adresses"]["streetName"],
           "streerNumber":q["adresses"]["streerNumber"]
        }
        return d


class UserSchema_Taches_categorie_ticket(Schema):
    id = fields.Integer(required = True)
    titre=fields.String(required=True)
    description=fields.String(required=True)
    id_categorie=fields.Integer(required=True)


@dataclass
class Taches_categorie_ticket(db.Model):
    id : int
    titre : text = None
    description:text = None
    id_categorie:int=None

    __name_table__ ="taches_categorie_ticket"
    id=db.Column(db.Integer(),primary_key=True)
    titre=db.Column(db.String(),default=NULL)
    description=db.Column(db.String(),default=NULL)
    id_categorie=db.Column(db.Integer(),default = NULL)

    def get(self):
        req=db.session.query(Taches_categorie_ticket).filter(
        Taches_categorie_ticket.id_categorie==self.id_categorie)
        sch=UserSchema_Taches_categorie_ticket(many=True,only=["titre","description"])
        res=sch.dump(req)
        return res


class UserSchema_categorie_ticket_parant(Schema):
    id = fields.Integer(required = True)
    libelle = fields.String(required=True)
    id_parent = fields.Integer(required = True)
    form = fields.String(required=True)
    delai_traitement = fields.String(required=True)
    users = fields.Nested(UserSchema_Users)
    tickets_categories = fields.Integer(required = True)

class UserSchema_categorie_ticket(Schema):
    id = fields.Integer(required = True)
    libelle = fields.String(required=True)
    categories = fields.Nested(UserSchema_categorie_ticket_parant)
    form = fields.String(required=True)
    delai_traitement = fields.String(required=True)
    users = fields.Nested(UserSchema_Users)


class UserSchema_Type_document(Schema):
    id=fields.Integer(required=True)
    libelle=fields.String(required=True)
    description=fields.String(required=True)
    form=fields.String(required=True)
    active=fields.Integer(required=True)


@dataclass
class Type_document(db.Model):
    id : int
    libelle : VARCHAR=None
    description : VARCHAR=None
    form : text=None
    active : int=None

    __name_table__="type_document"
    id=db.Column(db.Integer(),primary_key=True)
    libelle=db.Column(db.String(50),default=NULL)
    description=db.Column(db.String(255),default=NULL)
    form=db.Column(db.String(),default=NULL)
    active =db.Column(db.Integer(),default=NULL)


class UserSchema_Document_categorie_ticket(Schema):
    id=fields.Integer(required=True)
    oblig=fields.Integer(required=True)
    categories_ticket=fields.Nested(UserSchema_categorie_ticket)
    types_document=fields.Nested(UserSchema_Type_document)

@dataclass
class Document_categorie_ticket(db.Model):
    id:int
    id_categorie:int = None
    id_document:int=None
    oblig:int=None

    __name_table__ ="document_categorie_ticket"
    id=db.Column(db.Integer(),primary_key=True)
    oblig=db.Column(db.Integer(),default=NULL)

    id_categorie=db.Column(db.Integer, ForeignKey("categorie_ticket.id"),default=NULL)
    categories_ticket=db.relationship("Categorie_ticket", foreign_keys=[id_categorie],backref="document_categorie")

    id_document=db.Column(db.Integer,ForeignKey("type_document.id"),default=NULL)
    types_document=db.relationship("Type_document",foreign_keys=[id_document],backref="document_type")

    def get_document_categorie(self):
        req=db.session.query(Document_categorie_ticket).join(
        Type_document,Type_document.id==Document_categorie_ticket.id_document).filter(
        Document_categorie_ticket.id_categorie==self.id_categorie)
        sch=UserSchema_Document_categorie_ticket(many=True,only=["oblig","types_document"])
        res=sch.dump(req)
        if res:
            d={
                "id_document":res[0]["types_document"]["id"],
                "libelle":res[0]["types_document"]["libelle"]
            }
            del res[0]["types_document"]
            res[0].update(d)
        return res







@dataclass
class Categorie_ticket(db.Model):
    id : int
    libelle : VARCHAR = None
    id_parent : int = None
    form : text = None
    delai_traitement : int = None
    affect_a : int = None


    __name_table__ = "categorie_ticket"
    id = db.Column(db.Integer(),primary_key=True)
    libelle = db.Column(db.String(),default = NULL)

    id_parent = db.Column(db.Integer, ForeignKey('categorie_ticket.id'),default = NULL)
    categories = db.relationship("Categorie_ticket", remote_side=id,backref ='categorie_categorie')

    form = db.Column(db.String(),default = NULL)

    delai_traitement = db.Column(db.Integer(),default = NULL)

    affect_a = db.Column(db.Integer(),ForeignKey("users.id"),default = NULL)
    users= db.relationship("Users",foreign_keys=[affect_a],backref = "categorie_user")



    def list(self):
        q=db.session.query(Categorie_ticket)
        sch=UserSchema_categorie_ticket(many=True,exclude=["form","users"])
        res=sch.dump(q)
        for d in res :
            d1={
                "libelle_cat_parent":d["categories"]["libelle"],
                "id_parent":d["categories"]["id"]
            }
            del d["categories"]
            d.update(d1)
        return res

    def get_tache_ticket_by_cat(self,id_cat):
        L=Taches_categorie_ticket(id_categorie=id_cat).get()
        return L

    def get_form_categorie(self, id_parent):
        req=db. session.query(Categorie_ticket).filter(
        Categorie_ticket.id==id_parent)
        sch=UserSchema_categorie_ticket(many=True,only=["form"])
        res=sch.dump(req)
        return res

    def get_categorie_parente(self):
        req=db.session.query(Categorie_ticket).filter(
        Categorie_ticket.id==self.id)
        sch=UserSchema_categorie_ticket(many=True,only=["categories"])
        res=sch.dump(req)[0]["categories"]["id"] if sch.dump(req) else None
        return res


    def get_document_categorie(self):
        L=Document_categorie_ticket(id_categorie=self.id_parent).get_document_categorie()
        return L


    def get_categorie_tree(self):
        form = {"schema": {"properties": []}}
        list_doc = []
        list_tache = []
        while self.id_parent :
            list_doc_parent=Categorie_ticket(id_parent=self.id_parent).get_document_categorie()
            list_tache_parent = Categorie_ticket().get_tache_ticket_by_cat(self.id_parent)

            form_cat=Categorie_ticket().get_form_categorie(self.id_parent)

            list_doc = list_doc + list_doc_parent
            list_tache = list_tache + list_tache_parent

            if form_cat:
                form_cat_prop = form_cat
            else:
                form_cat_prop=[]
            form["schema"]["properties"] = form["schema"]["properties"] + form_cat_prop
            self.id_parent = Categorie_ticket(id_parent=self.id_parent).get_categorie_parente()
        return {"list_document": list_doc, "list_taches": list_tache, "form": form}


class UserSchema_Opportunite(Schema):
    id=fields.Integer(required=True)

@dataclass
class Opportunite(db.Model):
    id:int

    __name_table__ ="opportunite"
    id= db.Column(db.Integer(),primary_key=True)



class UserSchema_Affaire(Schema):
    id=fields.Integer(required=True)
    prospects=fields.Nested(UserSchema_Users)



@dataclass
class Affaire(db.Model):
    id:VARCHAR
    id_prospect:int=None

    __name_table__ ="affaire"
    id= db.Column(db.String(),primary_key=True)

    id_prospect=db.Column(db.Integer(),ForeignKey("prospects.id"),default=NULL)
    prospects=db.relationship("Prospects",foreign_keys=[id_prospect],backref = "affaire_proscpects")


    def get_pros_affaire(self,id_affaire):
        req=db.session.query(Affaire).join(
        Prospects,Prospects.id==Affaire.id_prospect).filter(
        Affaire.id==id_affaire)
        sch=UserSchema_Affaire(many=True,only=["prospects"])
        res=sch.dump(req)
        if res!=[]:
            d=res[0]
            d1={
                "id":d["prospects"]["id"],
                "name":d["prospects"]["name"],
                "surname":d["prospects"]["surname"],
                "tel":d["prospects"]["tel"],
                "tel2":d["prospects"]["tel2"],
                "adresse_mail":d["prospects"]["adresse_mail"],
                "mobile":d["prospects"]["mobile"]
            }
            return d1
        return []



class UserSchema_statuts_ticket(Schema):
    id = fields.Integer(required = True)
    libelle = fields.String(required=True)
    icone = fields.String(required=True)
    color = fields.String(required=True)
    background_color = fields.String(required=True)



class UserSchema_Ticket(Schema):
    id=fields.Integer(required = True)
    title=fields.String(required=True)
    id_opp=fields.Integer(required = True)
    prospects=fields.Nested(UserSchema_Prospects)
    id_affaire=fields.String(required=True)
    commentaire=fields.String(required=True)
    date_creation=fields.DateTime(required=True)
    last_update = fields.Time(required=True)
    date_limit = fields.Date(required = True)
    users_2 = fields.Nested(UserSchema_Users)
    users_1 = fields.Nested(UserSchema_Users)
    categories_ticket=fields.Nested(UserSchema_categorie_ticket)
    statuts_ticket=fields.Nested(UserSchema_statuts_ticket)
    url_files = fields.String(required = True)
    date_fermeture=fields.Time(required=True)
    alerter=fields.Integer(required=True)
    form=fields.String(required=True)
    date_reouverture = fields.Time(required=True)
    date_traitement=fields.DateTime(required=True)

@dataclass
class Ticket(db.Model):
    id : int
    title : VARCHAR = None
    id_opp : int = None
    id_prospect : int = None
    id_affaire : VARCHAR = None
    commentaire : text = None
    date_creation : datetime = None
    last_update : datetime.timestamp = None
    date_traitement : datetime = None
    date_limit : date = None
    createur : int = None
    affect : int = None
    categorie : int = None
    statut : int = None
    url_files: text = None
    date_fermeture : datetime.timestamp= None
    alerter : int = None
    form : text = None
    date_reouverture : datetime.timestamp = None


    __name_table__ ="ticket"
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(255),default = NULL)
    id_opp = db.Column(db.Integer(),default = NULL)
    id_affaire = db.Column(db.String(255),default = NULL)
    commentaire = db.Column(db.Text(),default = NULL)
    date_creation = db.Column(db.DateTime())
    last_update = db.Column(db.DateTime(),default = NULL)
    date_traitement = db.Column(db.DateTime(),default = NULL)
    date_limit = db.Column(db.Date(),default = NULL)

    createur = db.Column(db.Integer(),ForeignKey("users.id"),default = NULL)
    users_2=db.relationship("Users",foreign_keys=[createur],backref = "ticket_users_2")

    affect = db.Column(db.Integer(),ForeignKey("users.id"),default = NULL)
    users_1=db.relationship("Users",foreign_keys=[affect],backref="ticket_users")

    categorie = db.Column(db.Integer(),ForeignKey("categorie_ticket.id"),default = NULL)
    categories_ticket = db. relationship("Categorie_ticket",foreign_keys=[categorie],backref = "ticket_categorie_ticket")

    id_prospect = db.Column(db.Integer(),ForeignKey("prospects.id"),default = NULL)
    prospects = db.relationship("Prospects",foreign_keys=[id_prospect],backref = "ticket_prospects")

    statut = db.Column(db.Integer(),ForeignKey("statuts_ticket.id"),default = NULL)
    statuts_ticket = db.relationship("Statuts_ticket",foreign_keys = [statut], backref = "ticket_statuts_ticket")

    url_files = db.Column(db.Text(),default = NULL)
    date_fermeture = db.Column(db.DateTime(),default = NULL)
    alerter = db.Column(db.Integer(),default = 1)
    form = db.Column(db.Text(),default = NULL)
    date_reouverture = db.Column(db.DateTime(),default = NULL)

    def update(self):
        ticket=db.session.query(Ticket).filter_by(id=self.id).first()
        n=0
        if ticket.title!=self.title:
            ticket.title =self.title
            n=1
        if ticket.id_opp!=self.id_opp:
            ticket.id_opp =self.id_opp
            n=1
        if ticket.id_prospect!=self.id_prospect:
            ticket.id_prospect =self.id_prospect
            n=1
        if ticket.id_affaire !=self.id_affaire:
            ticket.id_affaire =self.id_affaire
            n=1
        if ticket.commentaire !=self.commentaire:
            ticket.commentaire =self.commentaire
            n=1
        if ticket.date_creation !=self.date_creation:
            ticket.date_creation =self.date_creation
            n=1
        if ticket.last_update !=self.last_update:
            ticket.last_update =self.last_update
            n=1
        if ticket.date_traitement !=self.date_traitement :
            ticket.date_traitement =self.date_traitement
            n=1
        if ticket.date_limit !=self.date_limit:
            ticket.date_limit =self.date_limit
            n=1
        if ticket.createur !=self.createur:
            ticket.createur =self.createur
            n=1
        if ticket.affect !=self.affect:
            ticket.affect =self.affect
            n=1
        if ticket.categorie !=self.categorie:
            ticket.categorie =self.categorie
            n=1
        if ticket.statut !=self.statut:
            ticket.statut =self.statut
            n=1
        if ticket.url_files!=self.url_files:
            ticket.url_files=self.url_files
            n=1
        if ticket.date_fermeture !=self.date_fermeture:
            ticket.date_fermeture =self.date_fermeture
            n=1
        if ticket.alerter !=self.alerter:
            ticket.alerter =self.alerter
            n=1
        if ticket.form !=self.form:
            ticket.form =self.form
            n=1
        if ticket.date_reouverture!=self.date_reouverture:
            ticket.date_reouverture=self.date_reouverture
            n=1
        db.session.commit()
        return n



    def get_specifique(self):
        req=db.session.query(Ticket).filter(
        Ticket.id==self.id)
        sch = UserSchema_Ticket(many=True)
        _id_ticket=sch.dump(req)
        if not _id_ticket:
            return jsonify(
                {
                    "error": True,
                    "mesage": f" Identifiant ne correspond a aucun id_ticket : {self.id}"
                })
        res=db.session.query(Ticket).join(
        Categorie_ticket,Categorie_ticket.id==Ticket.categorie).filter(
        Ticket.id==self.id)
        sc=UserSchema_Ticket(many=True,only=["form","categories_ticket"])
        result=sc.dump(res)
        if result[0]["categories_ticket"]["categories"]:
            form=Categorie_ticket(id_parent=result[0]["categories_ticket"]["categories"]["id_parent"],form=result[0]["categories_ticket"]["categories"]["form"]).get_categorie_tree()
            return form
        return jsonify({"form": {}})


    def md5(self):
        req=db.session.query(Ticket)
        sch = UserSchema_Ticket(many=True,only=["id"])
        _id_ticket=sch.dump(req)
        for d in _id_ticket:
            if ((md5(d["id"])==md5(self.id)) or(str(self.id)==md5(d["id"]))) :
                break
        return d["id"]


    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id



    def get(self):
        res_1 = db.session.query(Ticket).join(
            Categorie_ticket, Categorie_ticket.id==Ticket.categorie).join(
            Statuts_ticket, Statuts_ticket.id==Ticket.statut).join(
            Users, Ticket.createur==Users.id).filter(
            Ticket.id == self.id)
        sch_1=UserSchema_Ticket(many=True,only=["id",
                                              "title",
                                              "date_limit",
                                              "date_traitement",
                                              "date_fermeture",
                                              "commentaire",
                                              "date_creation",
                                              "id_affaire",
                                              "date_reouverture",
                                              "categories_ticket",
                                              "statuts_ticket",
                                              "users_2"
                                            ])
        real_id_1 = sch_1.dump(res_1)[0]


        res_2= db.session.query(Ticket).join(
            Categorie_ticket, Categorie_ticket.id==Ticket.categorie).join(
            Statuts_ticket, Statuts_ticket.id==Ticket.statut).join(
            Users, Ticket.affect==Users.id).filter(
            Ticket.id == self.id)
        sch_2=UserSchema_Ticket(many=True,only=["users_1"])
        real_id_2 = sch_2.dump(res_2)
        real_id_1["users_1"]=real_id_2[0]["users_1"]

        dt={"libelle_cat":real_id_1["categories_ticket"]["libelle"],
           "delai_traitement":real_id_1["categories_ticket"]["delai_traitement"],
           "statuts_libelle":real_id_1["statuts_ticket"]["libelle"],
            "icon":real_id_1["statuts_ticket"]["icone"],
            "color":real_id_1["statuts_ticket"]["color"],
            "background_color":real_id_1["statuts_ticket"]["background_color"],
            "statut":real_id_1["statuts_ticket"]["id"],
            "nom":real_id_1["users_1"]["nom"],
            "prenom":real_id_1["users_1"]["prenom"],
            "affect_nom":real_id_1["users_2"]["nom"],
            "affect_prenom":real_id_1["users_2"]["prenom"]
            }
        #return jsonify(dt)
        del real_id_1["categories_ticket"]
        del real_id_1["statuts_ticket"]
        del real_id_1["users_1"]
        del real_id_1["users_2"]
        real_id_1.update(dt)
        #return jsonify(real_id_1)

        if real_id_1:
            response = {}
            response["date_limit"] = real_id_1["date_limit"]
            response["date_creation"] = real_id_1["date_creation"]
            response["date_reouverture"] = real_id_1["date_reouverture"]
            response["date_fermeture"] =real_id_1["date_fermeture"]
            response["date_traitement"] =real_id_1["date_traitement"]
            response["sujet"] = real_id_1["title"]
            response["prospect"] = real_id_1["nom"] + " " + real_id_1["prenom"]
            response["categorie"] = real_id_1["libelle_cat"]
            response["statut_details"] = {
                                            "id": hex(real_id_1["statut"]),
                                            "libelle": real_id_1["statuts_libelle"],
                                            "icon": real_id_1["icon"],
                                            "color": real_id_1["color"],
                                            "background_color": real_id_1["background_color"]
                                        }
            #return jsonify(response)
            response["affecte_a"] = real_id_1["affect_prenom"] + " " + real_id_1["affect_nom"]
            response["affect"] = real_id_1["nom"]+" "+real_id_1["prenom"]
            response["id_affaire"] =real_id_1["id_affaire"]
            response["id_ticket_md5"] = hex(real_id_1["id"])
            response["id_ticket"] = self.id
            response["commentaire"] = real_id_1["commentaire"]
            response["delai_traitement"] = real_id_1["delai_traitement"]
            return response
        response = {"error": False, "message": "aucun details ticket pour cet id "}
        return response

    def get_1(self):
        real_id=0
        req=db.session.query(Ticket)
        sch = UserSchema_Ticket(many=True,only=["id"])
        _id_ticket=sch.dump(req)
        for d in _id_ticket:
            if ((md5(d["id"])==md5(self.id)) or(str(self.id)==md5(d["id"]))) :
                real_id = d["id"]
                break
        if real_id==0:
            response = {"error": True, "message": f"aucune ticket correspond a id : {self.id}"}
            return response
        res_1 = db.session.query(Ticket).join(
            Categorie_ticket, Categorie_ticket.id==Ticket.categorie).join(
            Statuts_ticket, Statuts_ticket.id==Ticket.statut).join(
            Users, Ticket.createur==Users.id).filter(
            Ticket.id == real_id)
        sch_1=UserSchema_Ticket(many=True,only=["id",
                                              "title",
                                              "date_limit",
                                              "date_traitement",
                                              "date_fermeture",
                                              "commentaire",
                                              "date_creation",
                                              "id_affaire",
                                              "date_reouverture",
                                              "categories_ticket",
                                              "statuts_ticket",
                                              "prospects",
                                              "users_2"
                                            ])
        real_id_1 = sch_1.dump(res_1)[0]

        res_2= db.session.query(Ticket).join(
            Categorie_ticket, Categorie_ticket.id==Ticket.categorie).join(
            Statuts_ticket, Statuts_ticket.id==Ticket.statut).join(
            Users, Ticket.affect==Users.id).filter(
            Ticket.id == real_id)
        sch_2=UserSchema_Ticket(many=True,only=["users_1"])
        real_id_2 = sch_2.dump(res_2)[0]
        real_id_1["users_1"]=real_id_2["users_1"]

        dt={"libelle_cat":real_id_1["categories_ticket"]["libelle"],
           "delai_traitement":real_id_1["categories_ticket"]["delai_traitement"],
           "statuts_libelle":real_id_1["statuts_ticket"]["libelle"],
            "icon":real_id_1["statuts_ticket"]["icone"],
            "color":real_id_1["statuts_ticket"]["color"],
            "background_color":real_id_1["statuts_ticket"]["background_color"],
            "statut":real_id_1["statuts_ticket"]["id"],
            "nom":real_id_1["users_1"]["nom"],
            "prenom":real_id_1["users_1"]["prenom"],
            "affect_nom":real_id_1["users_2"]["nom"],
            "affect_prenom":real_id_1["users_2"]["prenom"],
            }
        del real_id_1["categories_ticket"]
        del real_id_1["statuts_ticket"]
        del real_id_1["users_1"]
        del real_id_1["users_2"]
        real_id_1.update(dt)

        if real_id_1:
            response = {}
            response["date_limit"] = real_id_1["date_limit"]
            response["date_creation"] = real_id_1["date_creation"]
            response["date_reouverture"] = real_id_1["date_reouverture"]
            response["date_fermeture"] =real_id_1["date_fermeture"]
            response["date_traitement"] =real_id_1["date_traitement"]
            response["sujet"] = real_id_1["title"]
            response["createur"] = real_id_1["nom"] + " " + real_id_1["prenom"]
            response["categorie"] = real_id_1["libelle_cat"]
            response["statut_details"] = {
                        "id": hex(real_id_1["statut"]),
                        "libelle": real_id_1["statuts_libelle"],
                        "icon": real_id_1["icon"],
                        "color": real_id_1["color"],
                        "background_color": real_id_1["background_color"],
                        }
            response["affecte_a"] = real_id_1["affect_prenom"] + " " + real_id_1["affect_nom"]
            response["affect"] = real_id_1["nom"]+" "+real_id_1["prenom"]
            response["id_affaire"] =real_id_1["id_affaire"]
            #response["id_prospect"]=real_id_1["prospects"]["id"],
            #response["real_id_affaire"] = real_id_1["real_id_affaire"]
            response["id_ticket_md5"]=hex(real_id_1["id"])
            response["id_ticket"] = self.id
            response["commentaire"] = real_id_1["commentaire"]
            response["delai_traitement"] = real_id_1["delai_traitement"]
            return response
        response = {"error": False, "message": "aucun details ticket pour cet id "}
        return response


    def __to_dict__(self):
        items = Ticket.query.all()
        T=()
        for tick in items :
            schema = UserSchema_Ticket()
            result = schema.dump(tick)
            T+=(result,)
        return jsonify(T)

    def check_ids(self):
        if self.statut:
            req=db.session.query(Statuts_ticket)
            sch = UserSchema_statuts_ticket(many=True,only=["id"])
            _id_ticket=sch.dump(req)
            for d in _id_ticket:
                if ((md5(d["id"])==md5(self.statut)) or (str(self.statut)==md5(d["id"]))) :
                    break
            self.statut=d["id"]

        if self.categorie:
            req=db.session.query(Categorie_ticket)
            sch = UserSchema_categorie_ticket(many=True,only=["id"])
            _id_ticket=sch.dump(req)
            for d in _id_ticket:
                if ((md5(d["id"])==md5(self.categorie)) or (str(self.categorie)==md5(d["id"]))) :
                    break
            self.categorie=d["id"]

        if self.affect:
            req=db.session.query(Users)
            sch = UserSchema_Users(many=True,only=["id"])
            _id_ticket=sch.dump(req)
            for d in _id_ticket:
                if ((md5(d["id"])==md5(self.affect)) or(str(self.affect)==md5(d["id"]))) :
                    break
            self.affect=d["id"]

        if self.id_affaire:
            req=db.session.query(Affaire)
            sch = UserSchema_Affaire(many=True,only=["id"])
            _id_ticket=sch.dump(req)
            for d in _id_ticket:
                if ((md5(d["id"])==md5(self.id_affaire)) or (str(self.id_affaire)==md5(d["id"]))) :
                    break
            self.id_affaire=d["id"]

        if self.id_opp:
            req=db.session.query(Opportunite)
            sch = UserSchema_Opportunite(many=True,only=["id"])
            _id_ticket=sch.dump(req)
            for d in _id_ticket:
                if ((md5(d["id"])==md5(self.id_opp)) or (str(self.id_opp)==md5(d["id"]))) :
                    break
            self.id_opp=d["id"]

        if self.id_prospect:
            req=db.session.query(Prospects)
            sch = UserSchema_Prospects(many=True,only=["id"])
            _id_ticket=sch.dump(req)
            for d in _id_ticket:
                if ((md5(d["id"])==md5(self.id_prospect)) or(str(self.id_prospect)==md5(d["id"]))) :
                    break
            self.id_prospect=d["id"]



@dataclass
class Statuts_ticket(db.Model):
    id : int
    libelle : VARCHAR = None
    icone : VARCHAR = None
    color : VARCHAR = None
    background_color : VARCHAR = None

    __name_table__ = "statuts_ticket"
    id =  db.Column(db.Integer(),primary_key=True)
    libelle =  db.Column(db.String(255),default = NULL)
    icone =  db.Column(db.String(20) ,default = NULL)
    color =  db.Column(db.String(7),default = NULL)
    background_color =  db.Column(db.String(7),default = NULL)

    def count_ticket_by_categorie(self):
        res=db.session.query(Statuts_ticket).filter(
                Statuts_ticket.libelle==self.libelle)
        sch=UserSchema_statuts_ticket(many=True)
        q=sch.dump(res)
        return len(q)

    def md5(self,statut):
        req=db.session.query(Statuts_ticket)
        sch = UserSchema_statuts_ticket(many=True,only=["id"])
        _id_ticket=sch.dump(req)
        for d in _id_ticket:
            if ((hashlib.md5(str(d["id"]).encode("utf-8")).hexdigest()==hashlib.md5(str(statut).encode("utf-8")).hexdigest()) or
            (str(self.id)==(hashlib.md5(str(d["id"]).encode("utf-8")).hexdigest()))) :
                id_1=d["id"]
                break
        return id_1

    def list_2(self):
        item=db.session.query(Statuts_ticket)
        schema = UserSchema_statuts_ticket(many=True)
        statuts = schema.dump(item)
        for d in statuts :
            d["id"]=hex(d["id"])
        response = {"totale": 0}
        statut_ticket = Statuts_ticket()
        for statut in statuts:
            statut_ticket.libelle = statut["libelle"]
            count = statut_ticket.count_ticket_by_categorie()
            response["totale"] = response["totale"] + count
            response[statut_ticket.libelle.replace(" ", "_").replace("é", "e")] = count
        return jsonify(response)


    def list(self):
        item=db.session.query(Statuts_ticket)
        schema = UserSchema_statuts_ticket(many=True)
        result = schema.dump(item)
        for d in result :
            d["id"]=hex(d["id"])
        return result
    
    def list_1(self):
        item=db.session.query(Statuts_ticket)
        schema = UserSchema_statuts_ticket(many=True)
        result = schema.dump(item)
        for d in result :
            d["id"]=hex(d["id"])
        response = {
            "error": False,
            "list_statut": result
        }
        return jsonify(response)






    def __to_dict__(self):
        schema = UserSchema_statuts_ticket()
        result = schema.dump(self)
        return result



class UserSchema_Actions_ticket(Schema):
    id = fields.Integer(required = True)
    tickets = fields.Nested(UserSchema_Ticket)
    commentaire = fields.String(required = True)
    date_action = fields.DateTime(required = True)
    users_1 = fields.Nested(UserSchema_Users)
    statuts = fields.Nested(UserSchema_statuts_ticket)
    commentaire_action = fields.String(required = True)
    users_2=fields.Nested(UserSchema_Users)


@dataclass
class Actions_ticket(db.Model):
    id : int
    id_ticket : int=None
    commentaire : text = None
    date_action : datetime = None
    user : int = None
    action : int = None
    commentaire_action : text = None
    affect : int = None

    __name_table__ = "actions_ticket"
    id=db.Column(db.Integer(),primary_key=True)

    id_ticket=db.Column(db.Integer(),ForeignKey("ticket.id"),default=NULL)
    tickets=db.relationship("Ticket",foreign_keys=[id_ticket],backref="actions_ticket_1")

    commentaire=db.Column(db.String(),default = NULL)
    date_action=db.Column(db.Date(),default = NULL)

    user=db.Column(db.Integer(),ForeignKey("users.id"),default=NULL)
    users_1=db.relationship("Users",foreign_keys=[user],backref = "actions_users_1")

    action=db.Column(db.Integer(),ForeignKey("statuts_ticket.id"),default = NULL)
    statuts = db.relationship("Statuts_ticket",foreign_keys=[action],backref ="actions_statuts")

    commentaire_action=db.Column(db.String(),default = NULL)

    affect=db.Column(db.Integer(),ForeignKey("users.id"),default = NULL)
    users_2=db.relationship("Users",foreign_keys=[affect],backref = "actions_users_2")

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return "un action ticket added"


    def list_historique(self):
        res=db.session.query(Actions_ticket).join(
        Users,Users.id==Actions_ticket.user).filter(
        Actions_ticket.id_ticket==self.id_ticket)
        sch=UserSchema_Actions_ticket(many=True)
        q=sch.dump(res)
        for d in q :
            d1={
                #"affect":d["users_2"]["id"],
                "id_ticket":d["tickets"]["id"],
                "user":d["users_1"]["id"]
            }
            del d["users_2"]
            del d["tickets"]
            del d["users_1"]
            d.update(d1)
        return q


    def __to_dict__(self):
        res=db.session.query(Actions_ticket)
        sch=UserSchema_Actions_ticket(many=True)
        q=sch.dump(res)
        for d in q:
            d["id"]=hex(d["id"])
            d["tickets"]["id"]=hex(d["tickets"]["id"])
            d["date_action"]=d["date_action"].strftime("%Y-%m-%d %H:%M:%SZ")
        return jsonify(q)




class UserSchema_Tache_priorite(Schema):
    id = fields.Integer(required = True)
    libelle = fields.String(required=True)
    icon = fields.String(required=True)
    color = fields.String(required= True)



@dataclass
class Tache_priorite(db.Model):
    id : int
    libelle : VARCHAR = None
    icon : VARCHAR = None
    color : VARCHAR = None

    __name_table__ = "tache_priorite"
    id = db.Column(db.Integer(),primary_key=True)
    libelle = db.Column(db.String(100),default = NULL)
    icon = db.Column(db.String(100),default = NULL)
    color = db.Column(db.String(100),default = NULL)



class UserSchema_Tags(Schema):
    id=fields.Integer(required=True)


@dataclass
class Tags(db.Model):
    id:int

    __name_table__ ="tags"
    id=db.Column(db.Integer(),primary_key=True)

class UserSchema_Tache(Schema):
    id = fields.Integer(required = True)
    titre = fields.String(required=True)
    description = fields.String(required=True)
    users_1 = fields.Nested(UserSchema_Users)
    statut = fields.Integer(required = True)
    prospects = fields.Nested(UserSchema_Prospects)
    date_limit = fields.Date(required=True)
    taches_priorite = fields.Nested(UserSchema_Tache_priorite())
    url = fields.String(required=True)
    users_2 = fields.Nested(UserSchema_Users)


@dataclass
class Tache(db.Model):
    id : int
    titre : text = None
    description : text = None
    affecte_a : int = None
    statut : int = None
    prospect_id : int = None
    date_limit : datetime = None
    priorite : int = None
    url : VARCHAR = None
    created_by : int = None

    __name_table__ = "tache"
    id = db.Column(db.Integer(),primary_key=True)
    titre = db.Column(db.String(),default = NULL)
    description = db.Column(db.String(),default = NULL)

    affecte_a = db.Column(db.Integer(),ForeignKey('users.id'),default = NULL)
    users_1=db.relationship("Users",foreign_keys=[affecte_a],backref = "tache_users_1")

    statut = db.Column(db.Integer(),default = NULL)

    prospect_id = db.Column(db.Integer(),ForeignKey('prospects.id'),default = NULL)
    prospects = db.relationship("Prospects",foreign_keys=[prospect_id],backref = "tache_prospects")


    priorite = db.Column(db.Integer(),ForeignKey('tache_priorite.id'),default = NULL)
    taches_priorite=db.relationship("Tache_priorite",foreign_keys=[priorite],backref="tach_priorite")

    url = db.Column(db.String(255),default = NULL)
    date_limit = db.Column(db.Date(),default = NULL)

    created_by = db.Column(db.Integer(),ForeignKey("users.id"),default = NULL)
    users_2=db.relationship("Users",foreign_keys=[created_by],backref="tache_users_2")

    def insert_tache_ticket(self,id_ticket):
        db.session.add(self)
        db.session.commit()
        if id_ticket:
            Tache_ticket.insert(self.id,id_ticket)





    def list_tache_user(self):
        req=db.session.query(Tache).join(
        Tache_priorite,Tache_priorite.id==Tache.priorite).filter(
        Tache.affecte_a==self.affecte_a)
        sch=UserSchema_Tache(many=True)
        list_affect=sch.dump(req)
        for d in list_affect:
            d["id"]=hex(d["id"])
            d["affecte_a"]=hex(d["affecte_a"])
            d["taches_priorite"]=d["taches_priorite"]["libelle"]
        return jsonify(list_affect)





class UserSchema_Tache_tags(Schema):
    taches=fields.Nested(UserSchema_Tache)
    tags=fields.Nested(UserSchema_Tags)


@dataclass
class Tache_tags(db.Model):
    id_tag:int
    id_tache:int

    __name_table__ = "tache_tags"

    id_tache = db.Column(db.Integer(),ForeignKey("tache.id"),primary_key=True)
    taches=db.relationship("Tache",foreign_keys=[id_tache],backref="tache_tache")

    id_tag= db.Column(db.Integer(),ForeignKey("tags.id"),primary_key=True)
    tags=db.relationship("Tags",foreign_keys=[id_tag],backref="tache_tags")


class UserSchema_Tache_ticket(Schema):
    taches=fields.Nested(UserSchema_Tache)
    tickets=fields.Nested(UserSchema_Ticket)


@dataclass
class Tache_ticket(db.Model):
    id_tache : int = None
    id_ticket : int = None

    __name_table__ = "tache_ticket"
    id_tache = db.Column(db.Integer(), ForeignKey("tache.id"),primary_key=True)
    taches=db.relationship("Tache",foreign_keys=[id_tache],backref = "tache_tache_1")

    id_ticket = db.Column(db.Integer(),ForeignKey("ticket.id"),primary_key=True)
    tickets = db.relationship("Ticket",foreign_keys=[id_ticket],backref = "tache_ticket")

    def insert(self,tache_id,ticket_id):
        data={
            "id_tache":tache_id,
            "id_ticket":ticket_id
        }
        sch=UserSchema_Tache_ticket()
        res=sch.load(data)
        db.session.add(res)
        db.session.commit()


    def list_taches(self):
        query_affect=db.session.query(Tache_ticket).join(
        Tache,Tache.id==Tache_ticket.id_tache).filter(
        Tache_ticket.id_ticket==self.id_ticket)
        sch=UserSchema_Tache_ticket(many=True,only=["taches"])
        result_query_affect=sch.dump(query_affect)
        d={
        "affecte_a":result_query_affect[0]["taches"]["users_1"],
        "prospect_id":result_query_affect[0]["taches"]["prospects"]
        }
        del result_query_affect[0]["taches"]
        result_query_affect[0].update(d)

        if result_query_affect:
            query=db.session.query(Tache)

            if result_query_affect[0]["affecte_a"]:
                query.join(
                Users, Users.id==Tache.affecte_a)
        if result_query_affect[0]["prospect_id"]:
            query.join(
            Prospects, Prospects.id==Tache.prospect_id)


        query.join(
        Tache_priorite,Tache_priorite.id==Tache.priorite).join(
        Tache,Tache_ticket.id_tache==Tache.id).filter(
        Tache_ticket.id_ticket==self.id_ticket)
        sch=UserSchema_Tache(many=True,exclude=["url","users_2"])
        res=sch.dump(query)
        for d in res:
            d1={
                "id_tache":d["id"],
                "id":md5(d["id"]),
                "affect_a":md5(d["users_1"]["id"]),
                #"prespects_id":d["prospects"]["id"]
            }
            del d["id"]
            d.update(d1)

        if result_query_affect:
            if result_query_affect[0]["affecte_a"]:
                for d in res:
                    d["user_full_name"]=d["users_1"]["nom"]+" "+d["users_1"]["prenom"]
                    del d["users_1"]
            if result_query_affect[0]["prospect_id"]:
                for d in res :
                    d["user_full_name"]=d["prospects"]["name"]+" "+d["prospects"]["surname"]
                    del d["prospects"]
        return jsonify(res)






class UserSchema_Commentaire_ticket(Schema):
    id = fields.Integer(required = True)
    tickets = fields.Nested(UserSchema_Ticket)
    commantaire = fields.String(required=True)
    date = fields.Date(required=True)
    users = fields.Nested(UserSchema_Users)


@dataclass
class Commentaire_ticket(db.Model):
    id : int
    ticket : int = None
    commantaire : VARCHAR = None
    date : datetime = None
    user : int = None

    __name_table__ = "commentaire_ticket"
    id = db.Column(db.Integer(),primary_key=True)

    ticket = db.Column(db.Integer(),ForeignKey("ticket.id"),default = NULL)
    tickets=db.relationship("Ticket",foreign_keys=[ticket],backref = "commentaire_ticket")

    commantaire = db.Column(db.String(),default = NULL)
    date = db.Column(db.Date(),default = NULL)

    user = db.Column(db.Integer(),ForeignKey("users.id"),default = NULL)
    users=db.relationship("Users",foreign_keys=[user],backref="commentaire_users")

    def select(self):
        req=db.session.query(Commentaire_ticket).join(
        Ticket,Ticket.id==Commentaire_ticket.ticket).filter(
        Ticket.id==self.id )
        sch=UserSchema_Commentaire_ticket(many=True,only=["id","commantaire","date","users","tickets"])
        res=sch.dump(req)
        for d in res:
            d1={
                "user_image":d["users"]["photo"],
                "user_name":d["users"]["nom"]+" "+d["users"]["prenom"],
                "user":d["users"]["id"],
                "id_entity":d["tickets"]["id"]
            }
            del d["tickets"]
            del d["users"]
            d.update(d1)
            d["entity"]="T"
        return jsonify(res)



    def __to_dict__(self):
        item=self.query.all()
        sch=UserSchema_Commentaire_ticket()
        q=sch.dump(item)[0]
        q["id"]=hex(q["id"])
        q["date"]=datetime.strptime(q["date"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%SZ")
        if self.user:
            user=Users.get(self.user)
            q["full_name"]=user["nom"]+" "+user["prenom"]
            q["photo"]=user["photo"]
        return q

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return "data added"


class UserSchema_Doc_ticket(Schema):
    id=fields.Integer(required=True)
    name=fields.String(required=True)


@dataclass
class Doc_ticket(db.Model):
    id:int
    name:VARCHAR=None

    __name_table__ ="doc_ticket"
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(255),default=NULL)


class UserSchema_Ticket_users(Schema):
    ticket=fields.Nested(UserSchema_Ticket)
    id_user=fields.Integer(required=True)


@dataclass
class Ticket_users(db.Model):
    id_ticket:int=None
    id_user:int=None

    __name_table__ ="ticket_users"
    id_ticket= db.Column(db.Integer(), ForeignKey("ticket.id"),primary_key=True)
    ticket=db.relationship("Ticket",foreign_keys=[id_ticket],backref = "ticket_users_1")

    id_user= db.Column(db.Integer(),primary_key=True)

    def update_affect_ticket_user(self,ticket, user_affect):
        if user_affect == -1:
            d={
                "id_ticket":ticket,
                "id_user":user_affect
            }
            ticket_users=Ticket_users(**d)
            db.session.add(ticket_users)
            db.session.commit()
            return user_affect
        else:
            return 0


class UserSchema_Param_app(Schema):
    id=fields.Integer(required=True)
    name=fields.String(required=True)
    value=fields.String(required=True)

@dataclass
class Param_app(db.Model):
    id:int
    name:VARCHAR=None
    value:VARCHAR=None

    __name_table__ ="param_app"
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(50),default=NULL)
    value=db.Column(db.String(255),default=NULL)

    def get_info_url_ticket(self):
        req=db.session.query(Param_app).filter(
        Param_app.name=='index_geoprod' or
        Param_app.name=='URL_TICKET_DETAILS')
        sch=UserSchema_Param_app(many=True,exclude=["id"])
        res=sch.dump(req)
        return res

class UserSchema_Param_app(Schema):
    id=fields.Integer(required=True)
    commentaire=fields.String(required=True)
    affaires=fields.Nested(UserSchema_Affaire)
    prospects=fields.Nested(UserSchema_Prospects)
    users=fields.Nested(UserSchema_Users)


@dataclass
class Actions_dossier(db.Model):
    id:int
    dossier:VARCHAR=None
    pros:int=None
    user:int=None
    commentaire:text=None

    __name_table__="actions_dossier"
    id=db.Column(db.Integer(),primary_key=True)
    commentaire=db.Column(db.String(),default=NULL)

    dossier=db.Column(db.String(255),ForeignKey("affaire.id"),default=NULL)
    affaires=db.relationship("Affaire",foreign_keys=[dossier],backref = "action_affaire")

    pros=db.Column(db.Integer(),ForeignKey("prospects.id"),default=NULL)
    prospects=db.relationship("Prospects",foreign_keys=[pros],backref = "action_prospects")

    user=db.Column(db.Integer(),ForeignKey("users.id"),default=NULL)
    users=db.relationship("Users",foreign_keys=[user],backref = "action_users")

    def insert(self):
        db.session.add(self)
        db.session.commit()



