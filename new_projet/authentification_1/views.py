from asyncio.windows_events import NULL
from this import d
from tokenize import String
from typing_extensions import Required
from flask import request,jsonify,session,make_response,Response,json
from . import (type_ticket_namespace,
                type_tache_ticket_namespace,
                type_categories_ticket_namespace,
                type_actions_ticket_namespace,
                type_statuts_ticket_namespace,
                type_statuts_ticket_count_namespace,
                type_commentaire_ticket_namespace,
                post_ticket_namespace,
                update_ticket_namespace,
                type_statuts_ticket_list__namespace)
from marshmallow import Schema,pre_dump
from .models import (Affaire,
                    Ticket,
                    UserSchema_Ticket,
                    Users,
                    UserSchema_Users,
                    Categorie_ticket,
                    UserSchema_Tache,
                    Tache_priorite,
                    Prospects,
                    Statuts_ticket,
                    Taches_categorie_ticket,
                    Actions_ticket,
                    Commentaire_ticket,
                    UserSchema_Commentaire_ticket,
                    Tache_ticket,
                    Tache,
                    UserSchema_Tache_ticket,
                    UserSchema_Actions_ticket,
                    Ticket_users,
                    Param_app,
                    Actions_dossier,
                    UserSchema_Affaire,
                    UserSchema_Prospects,
                    UserSchema_categorie_ticket)
from .models import db
from datetime import date, datetime
import hashlib
from copy import copy
from flask_restx import Resource,Api,fields
from .utile import md5,add_child


@type_ticket_namespace.route("/<_id>", methods=["GET"])
class get_info_ticket_by_id(Resource):
    def get(self,_id):
        try:
            d=Ticket(id=_id).get_1()
            return d, 200
        except Exception as e:
            return {"error":str(e)}, 406




@type_tache_ticket_namespace.route("/<id>", methods=["GET"])
class get_info_taches_ticket_by_id(Resource):
    def get(self,id):
        real_id=0
        req=db.session.query(Ticket)
        sch = UserSchema_Ticket(many=True,only=["id"])
        _id_ticket=sch.dump(req)
        for d in _id_ticket:
            if ((md5(d["id"])==md5(id)) or(str(id)==md5(d["id"]))) :
                real_id = d["id"]
                break
        if real_id==0:
            response = {"error": True, "message": f"aucune ticket correspond a id : {id}"}
            return response
        list=Tache_ticket(id_ticket=id).list_taches()
        return list




@type_commentaire_ticket_namespace.route("/<id_ticket>", methods=["GET"])
class get_comentaire_ticket(Resource):
    def get(self,id_ticket):
        try:
            result_comm = Commentaire_ticket(id=id_ticket).select()
            return result_comm
        except:
            return "unvalide syntaxe"




#-------------------------------------------------------------------------------------

@type_categories_ticket_namespace.route("/<id_ticket>", methods=["GET"])
class get_info_specifique_ticket_by_id(Resource):
    def get(self,id_ticket):
        _id_ticket=0
        req=db.session.query(Ticket)
        sch = UserSchema_Ticket(many=True,only=["id"])
        ticket=sch.dump(req)
        for d in ticket:
            if ((md5(d["id"])==md5(id_ticket)) or(str(id_ticket)==md5(d["id"]))) :
                _id_ticket = d["id"]
                break
        if _id_ticket==0:
            response = {"error": True, "message": f"aucune ticket correspond a id : {id_ticket}"}
            return response
        req=db.session.query(Ticket).filter(
        Ticket.id==_id_ticket)
        sch=UserSchema_Ticket(many=True,only=["form","categories_ticket"])
        result =sch.dump(req)
        if result:
            try:
                form =Categorie_ticket(id_parent=result[0]["categories_ticket"]["categories"]["id_parent"]).get_categorie_tree()["form"]
                data =result[0]["categories_ticket"]["categories"]["form"]
                form["data"] = data
            except :
                return {
                        "form": {
                            "error": "impossible de decoder le JSON. Verifiez le format des données dans la bdd"
                        },
                        "error": True,
                    },200
            d={"form": form, "error": False}
            return d, 200
        return {"form": {}}, 200

#-------------------------------------------------------------------------------------------------------------------------------



@type_actions_ticket_namespace.route("/<_id>", methods=["GET"])
class get_historique_ticket_by_id(Resource):
    def get(self,_id):
        real_id=0
        req=db.session.query(Ticket)
        sch = UserSchema_Ticket(many=True,only=["id"])
        ticket=sch.dump(req)
        for d in ticket:
            if ((md5(d["id"])==md5(_id)) or(str(_id)==md5(d["id"]))) :
                real_id = d["id"]
                break
        if real_id==0:
            response = {"error": True, "message": f"aucune ticket correspond a id : {_id}"}
            return response
        historique = Actions_ticket(id_ticket=real_id).list_historique()
        response = {"result": historique}
        return jsonify(response)




@type_statuts_ticket_namespace.route("/", methods=["GET"])
class get_all_status_tickets_by_all_id(Resource):
    def get(self):
        try:
            statut_ticket = Statuts_ticket()
            get_statut = statut_ticket.list()
            if get_statut is not None:
                response = {
                    "error": False,
                    "list_statut": get_statut
                    }
                return jsonify(response)
            response = {"error": True, "message": "aucun  statut est dissponible "}
            return jsonify(response)
        except:
            return "invalide syntaxe"



@type_statuts_ticket_count_namespace.route("/", methods=["GET"])
class get_count_ticket_by_categorie(Resource):
    def get(self):
        statuts = Statuts_ticket().list()
        response = {"totale": 0}
        statut_ticket = Statuts_ticket()
        for statut in statuts:
            statut_ticket.libelle = statut["libelle"]
            count = statut_ticket.count_ticket_by_categorie()
            response["totale"] = response["totale"] + count
            response[statut_ticket.libelle.replace(" ", "_").replace("é", "e")] = count
        return response




#recursive
#---------------------------------------------------------------------

type_statuts_ticket_list__namespace.route("/", methods=["GET"])
class list_cat_ticket(Resource):
    def get(self):
        result = Categorie_ticket().list()
        if result:
            result_etats = []
            while result:
                d=result.pop(0)
                id_parent=d["id_parent"]
                if not id_parent or d["id"] == id_parent:
                    d["child"] = []
                    result_etats.append(d)
                    continue
                add_child(result_etats,d)
                if "child" in d:
                    continue
                result.append(d)
            return jsonify({"categories_ticket":result_etats }), 200
        return jsonify([]), 200

#-----------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------------
model_ticket=post_ticket_namespace.model("ticket",{
    "title":fields.String(required=False),
    "id_opp":fields.Integer(required=False),
    "id_prospect":fields.Integer(required=False),
    "id_affaire":fields.String(required=False),
    "commentaire":fields.String(required=False),
    "date_creation":fields.DateTime(required=False),
    "last_update" :fields.DateTime(required=False) ,
    "date_traitement" :fields.DateTime(required=False) ,
    "date_limit" :fields.Date(required=False) ,
    "createur" :fields.Integer(required=False) ,
    "affect" :fields.Integer(required=False) ,
    "categorie" :fields.Integer(required=False) ,
    "statut" : fields.Integer(required=False),
    "url_files" :fields.String(required=False) ,
    "date_fermeture" :fields.DateTime(required=False),
    "alerter" :fields.Integer(required=False) ,
    "form" :fields.String(required=False) ,
    "date_reouverture" : fields.DateTime(required=False)

})

@post_ticket_namespace.route("/", methods=["POST"])
class add_new_ticket(Resource):
    @post_ticket_namespace.expect(model_ticket)
    def post(self):
        try:
            dictionary = request.get_json()
            dictionary["id_affaire"] = request.args.get("id_affaire")
            dictionary["id_opp"] = request.args.get("id_opp")
            dictionary["id_prospect"] = request.args.get("id_prospect")
            files = request.files.getlist("file[]")
            ticket = Ticket(**dictionary)
            ticket.check_ids()
            breadcrumb_cat_ticket = request.args.get("breadcrumb_cat_ticket")
        except TypeError as e:
            if "__init__" in str(e):
                return (
                    {"error": True, "message": f"parametre non present: {e}"},
                    406,
                )
            return (
                {"error": True, "message": "body application/json non present"},
                406,
            )
        except ValueError as e:
            return {"error": True, "message": str(e)}, 406

        session = request.headers.get("idSession")
        id_utilisateur =Users(id_session=session).get_id_user_by_session()

        id_ticket=ticket.insert()

        if id_ticket is None:
            response = {"error": True, "message": "Erreur d'ajout du ticket "}
            return response, 304

        name_document_ticket = ""
        if len(files) > 0:
            name_document_ticket = str(id_ticket)
            #upload_doc_ticket(
            #files, id_ticket, "divers", name_document_ticket, ticket.createur
            #)

        if ticket.affect:
            subject = "Notification sur ticket" + str(id_ticket) + " " + ticket.title
            prenom_user_cree = Users().get_prenom_id(ticket.createur)

            n=Ticket_users().update_affect_ticket_user(id_ticket, ticket.affect)
            prenom_user_affect =Users().get_prenom_id(ticket.affect)

            mail_affect = Users().get_mail_id(ticket.affect)
            body = (
            "<p style='color: #666666'>Bonjour '"
            + str(prenom_user_affect)
            + "', '"
            + str(prenom_user_cree)
            + "' vous a affecté un ticket.</p>"
            + "<p><ul  style='color: #666666'><li>Sujet : <b>"
            + ticket.title
            + "</b></li>"
            + "<li>Numéro : <span style='color: #fff; background-color:#666666;' >"
            + str(id_ticket)
            + "</span></li>"
            + "<li>Catégorie : "
            )
            if breadcrumb_cat_ticket :
                body=(
                    body
                    +breadcrumb_cat_ticket
                    +"</li>"
                )
            if ticket.date_limit and ticket.date_limit != "null":
                body = (
                    body
                    + "<li>Date limite de résolution : <span style='color: #fff; background-color:#666666;' >"
                    + str(ticket.date_limit)
                    + "</span></li></ul></p>"
                )
            params =Param_app().get_info_url_ticket()

            #url = params.DOMAIN_HOST + params.URL_TICKET_DETAILS + hashlib.md5(str(id_ticket).encode("utf-8")).hexdigest()

            body = (
                body
                + "<br><br><br><p style='text-align: center;'><a style='color: #666666; font-size: 16px;text-align: "
                "center;' href='"
                #+ url
                + "' target='_blank'>Cliquez ici pour ouvrir </a></p><br>"
            )
            body = (
                body
                + "<p style='font-size: 12px;text-align: center;'><span style='color: red; "
                "background-color:yellow;'><u>Il est important de répondre sur l'interface</u>, <b>la réponse par "
                "mail à ce message ne sera pas prise en considération.</b></span></p> "
            )
            mail_user =Users().get_mail_id(id_utilisateur)
            args = {
                "id_utilisateur": id_utilisateur,
                "id_opp": ticket.id_opp,
                "id_prospect": ticket.id_prospect,
                "id_affaire": ticket.id_affaire,
                "mail_utilisateur": mail_user,
                "mail_prospect": mail_affect,
                "modele_reel": body,
                "statut": "P",
                "subject": subject,
                "url_files": name_document_ticket
                }
        commentaire_action = "ticket ajouté "

        req=db.session.query(Affaire)
        sch = UserSchema_Affaire(many=True,only=["id"])
        _id_ticket=sch.dump(req)
        for d in _id_ticket:
            if ((md5(d["id"])==md5(dictionary["id_affaire"])) or (dictionary["id_affaire"]==md5(d["id"]))) :
                break
 
        _id=d["id"]
        if _id:
            user=Users().getUserId(session)
            if user!=[]:
                user=Users().getUserId(session)["id"]
            else:
                user=""
            pros=Affaire().get_pros_affaire(dictionary["id_affaire"])
            if pros!=[]:
                pors=Affaire().get_pros_affaire(dictionary["id_affaire"])["id"]
            else:
                pros=""
            Actions_dossier(
                dossier=dictionary["id_affaire"],
                pros=pros,
                user=user,
                commentaire=commentaire_action).insert()
                #json_object=dictionary["json_object"] if dictionary["json_object"] else None).insert()
        response = {
            "messaage": "Votre ticket a été ajouté avec succès",
            "error": False,
            "id_ticket":id_ticket,
            "id": md5(id_ticket)
            }
        return response , 200




model_update_ticket=update_ticket_namespace.model("update_ticket",{
    "id":fields.Integer(required=True),
    "title":fields.String(required=False),
    "id_opp":fields.Integer(required=False),
    "id_prospect":fields.Integer(required=False),
    "id_affaire":fields.String(required=False),
    "commentaire":fields.String(required=False),
    "date_creation":fields.DateTime(required=False),
    "last_update" :fields.DateTime(required=False) ,
    "date_traitement" :fields.DateTime(required=False) ,
    "date_limit" :fields.Date(required=False) ,
    "createur" :fields.Integer(required=False) ,
    "affect" :fields.Integer(required=False) ,
    "categorie" :fields.Integer(required=False) ,
    "statut" : fields.Integer(required=False),
    "url_files" :fields.String(required=False) ,
    "date_fermeture" :fields.DateTime(required=False),
    "alerter" :fields.Integer(required=False) ,
    "form" :fields.String(required=False) ,
    "date_reouverture" : fields.DateTime(required=False)
})

@update_ticket_namespace.route("/", methods=["PUT"])
class update_ticket(Resource):
    @post_ticket_namespace.expect(model_update_ticket)
    def put(self):
        session = request.headers.get("idSession")
        try:
            details = request.get_json()
        except KeyError as e:
            response = {"erreur": True, "messsage": f"paramétre non présent : {e}"}
            return jsonify(response), 406

        ticket = Ticket(**details)

        #comm_ticket = details.get("comm_ticket")

        req=db.session.query(Ticket)
        sch = UserSchema_Ticket(many=True,only=["id"])
        _id_ticket=sch.dump(req)
        for d in _id_ticket:
            if ((md5(d["id"])==md5(ticket.id)) or (str(ticket.id)==md5(d["id"]))) :
                break
        id_ticket =d["id"]
        if not id_ticket:
            response = {
                "error": True,
                "message": f"Aucune ticket correspond au id : {ticket.id}",
            }
            return response, 406
        ticket.id = id_ticket

        prospect = None
        if ticket.id_prospect:
            req=db.session.query(Prospects)
            sch = UserSchema_Prospects(many=True,only=["id"])
            _id_ticket=sch.dump(req)
            for d in _id_ticket:
                if ((md5(d["id"])==md5(ticket.id_prospect)) or(str(ticket.id_prospect)==md5(d["id"]))) :
                    break
            prospect =d["id"]
            if not prospect:
                response = {
                    "error": True,
                    "message": f"Aucune prospect ticket correspond au id prospect : {ticket.id_prospect}",
                }
                return response, 406
        ticket.id_prospect = prospect

        categorie = None
        if ticket.categorie:
            req=db.session.query(Categorie_ticket)
            sch = UserSchema_categorie_ticket(many=True,only=["id"])
            _id_ticket=sch.dump(req)
            for d in _id_ticket:
                if ((md5(d["id"])==md5(ticket.categorie)) or (str(ticket.categorie)==md5(d["id"]))) :
                    break
            categorie =d["id"]
            if not categorie:
                response = {
                "error": True,
                "message": f"Aucune categorie ticket correspond au categorie : {ticket.categorie}",
                }
                return response, 406
        ticket.categorie = categorie


        affect = None
        if ticket.affect:
            req=db.session.query(Users)
            sch = UserSchema_Users(many=True,only=["id"])
            _id_ticket=sch.dump(req)
            for d in _id_ticket:
                if ((md5(d["id"])==md5(ticket.affect)) or(str(ticket.affect)==md5(d["id"]))) :
                    break
            affect = d["id"]
            if not affect:
                response = {
                "error": True,
                "message": f"Aucune user correspond au id : {ticket.affect}",
                }
                return response, 406
        ticket.affect = affect

        result=ticket.update()

        mail_user =Users().get_mail_id(affect)

        comm_ticket = "**" + mail_user + "**"  #+comm_ticket
        commentaire_statut = "Modification des donneés sans changement du statut "
        body = ""
        if comm_ticket != "" and comm_ticket != None:
            body = body + "<p>Message: '" + comm_ticket + "'</p><br>"
        body = (
            body
            + "<p style='font-style: italic;'><ul  style='color: #666666'><li>Sujet : <b>"
            + ticket.title
            + "</b></li>"
        )
        body = (
            body
            + "<li>Numéro : <span style='color: #fff; background-color:#666666;' >"
            + str(ticket.id)
            + "</span></li>"
        )
        if ticket.categorie:
            body = body + "<li>Catégorie : " + str(ticket.categorie) + "</li>"
        if ticket.date_limit and ticket.date_limit != "null":
            body = (
                body
                + "<li>Date limite de résolution : <span style='color: #fff; background-color:#666666;' >"
                + ticket.date_limit
                + "</span></li></ul></p>"
            )
        
        params = Param_app().get_info_url_ticket()

        body = (
            body
            + "<br><br><br><p style='text-align: center;'><a style='color: #666666; font-size: 16px;text-align: center;' href='"
            #+ params.DOMAIN_HOST
            #+ params.URL_TICKET_DETAILS
            + md5(ticket.id)
            + "' target='_blank'>Cliquez ici pour ouvrir </a></p><br>"
        )
        body = (
            body
            + "<p style='font-size: 12px;text-align: center;'><span style='color: red; background-color:yellow;'><u>Il est important de répondre sur Geoprod</u>, <b>la réponse par mail à ce message ne sera pas prise en considération.</b></span></p>"
        )

        subject = "Notification sur Ticket #" + str(id_ticket) + " " + ticket.title
        id_user =Users(id_session=session).get_id_user_by_session()
        user_mail = Users().get_mail_id(id_user)
        mail_affect = Users().get_mail_id(ticket.affect)
        args = {
            "id_utilisateur": id_user,
            "id_prospect": prospect,
            "mail_utilisateur": user_mail,
            "mail_prospect": mail_affect,
            "modele_reel": body,
            "statut": "P",
            "subject": subject,
        }

        if result == 1:
            return {"error": False, "message": "Votre ticket a été modifié"}, 200
        return {"error": True, "message": "Erreur lors de la modification car il n' ya pas de modification"}, 304





