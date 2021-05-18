# installations nécessaires
!pip install facebook-sdk
!pip install facebook-scraper

# On fait les imports
import urllib3, facebook, requests
from facebook_scraper import get_posts
import pymongo
from pymongo import MongoClient
import json


"""
Cette fonction permet de récupérer des données relatives à un sujet "topic" dans une page "page"
Les données récupérées sont le message du poste, les commentaires, et les probables photos

Cette fonction renvoie la liste des posts qui correspondants au critère.

"""
def main(topic = "le décès du président Jacques Chirac", page):
	page_token = "--------"
	graph = facebook.GraphAPI(access_token = page_token, version="10.0")
	pages_data = graph.get_object(page)
	page_id = pages_data["data"]["id"]

	posts = graph.get_all_connections(id=page_id,
                                 connection_name='posts',
                                 fields='type, name, created_time, object_id')

	real_posts = []

	# On recupère les postes dont le message parle du sujet qu'on veut
	for post in posts:
		data_post = graph.get_object(id=post['id'], fields="""message,
                                      comments, picture""")

		if data_post['message'].contains(topic):
			post["data_post"] = data_post
			real_posts.append(post)

    return real_posts


"""
On utilise la méthode main pour prendre les posts dans la page "kaisens" qui parlent du 
décès de chirac puis on insère dans la base de données.
"""

if __name__ == '__main__':
	
	final_posts = main(page="kaisens")
	
	try:
		conn = MongoClient()
		print("Connected to mongo !")
	except:
		print("Could not connect")

	# database
	database = conn["kaisens"]

	# collection
	deces_chirac = database["decesChirac"]

	# insertion des posts qui parlent du décès de chirac
	deces_chirac.insert_many(final_posts)




