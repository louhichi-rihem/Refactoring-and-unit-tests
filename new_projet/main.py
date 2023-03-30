from flask import Flask,request,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from authentification_1 import(type_ticket_namespace,
                                type_tache_ticket_namespace,
                                type_categories_ticket_namespace,
                                type_actions_ticket_namespace,
                                type_statuts_ticket_namespace,
                                type_statuts_ticket_count_namespace,
                                type_commentaire_ticket_namespace,
                                post_ticket_namespace,
                                update_ticket_namespace,
                                type_statuts_ticket_list__namespace)
from authentification_1.models import db


app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.app_context().push()
db.init_app(app)
api=Api(app,doc='/')



api.add_namespace(type_ticket_namespace)
api.add_namespace(type_tache_ticket_namespace)
api.add_namespace(type_categories_ticket_namespace)
api.add_namespace(type_actions_ticket_namespace)
api.add_namespace(type_statuts_ticket_namespace)
api.add_namespace(type_statuts_ticket_count_namespace)
api.add_namespace(type_commentaire_ticket_namespace)
api.add_namespace(type_statuts_ticket_list__namespace)

api.add_namespace(post_ticket_namespace)

api.add_namespace(update_ticket_namespace)


#pp.register_blueprint(app_api)


#db.create_all()

if __name__=='__main__':
    app.run(debug=True)

