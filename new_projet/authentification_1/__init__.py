from flask import Blueprint
from flask_restx import Namespace


#app = Blueprint("auth API", __name__)

type_ticket_namespace = Namespace('get_info_ticket',description = 'namespace for ticket')
type_tache_ticket_namespace = Namespace('list_taches_ticket',description = 'namespace for tache_ticket')
type_categories_ticket_namespace = Namespace('get_info_specifique_ticket',description = 'namespace for categories_ticket')
type_actions_ticket_namespace=Namespace('get_historique_ticket',description = 'namespace for actions_ticket')
type_statuts_ticket_namespace=Namespace('get_all_status_tickets',description = 'namespace for statuts_ticket')
type_statuts_ticket_count_namespace=Namespace('get_count_ticket_by_categorie',description ='namespace for statuts_ticket_count_by_categorie' )
type_commentaire_ticket_namespace=Namespace('get_comentaire_ticket',description = 'namespace for commentaire ticket')
type_statuts_ticket_list__namespace=Namespace('list_cat_ticket',description='namespace for statuts_ticket_list-cat')



post_ticket_namespace=Namespace('add_ticket',description = 'namespace for adding ticket')

update_ticket_namespace=Namespace('update_ticket',description = 'namespace for updating ticket')

import authentification_1.views


