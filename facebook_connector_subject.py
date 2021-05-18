# installations nécessaires
!pip install facebook-sdk
!pip install facebook-scraper

# On fait les imports
import facebook
from facebook_scraper import get_posts
import pymongo
from pymongo import MongoClient


# Token utilisateur pour l'application Facebook mise sur pied
PAGE_TOKEN = "--------"

"""
Cette fonction permet de récupérer des posts relatifs à un sujet "topic" dans une page "page"
Les données récupérées sont le message du poste, les commentaires, et les probables photos
- utilise l'api Facebook Graph
Cette fonction renvoie la liste des posts qui correspondants au critère.

"""
def main(topic = "le décès du président Jacques Chirac", page):
	graph = facebook.GraphAPI(access_token = PAGE_TOKEN, version="10.0")
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

		if topic in data_post['message']:
			post["data_post"] = data_post
			real_posts.append(post)

    return real_posts


"""
Cette fonction permet de récupérer des posts relatifs à un sujet "topic" dans une page "page". 
Le message du poste, les commentaires, et les probables photos sont contenues dans les données récupérées.

- utilise la librairie Facebook-scraper

Cette fonction renvoie la liste des posts qui correspondants au critère.
"""
def post_scrapper(topic = "le décès du président Jacques Chirac", page):
	listposts = []
	for post in get_posts(page, pages=20, options={"comments": True}):

    	if topic in post['text']: 
        	listposts.append(post)
        	
    return listposts


"""
On utilise la méthode main pour prendre les posts dans la page "kaisens" qui parlent du 
décès de chirac puis on insère dans la base de données.
"""
if __name__ == '__main__':
	
	final_posts = main(page="kaisens")
	# final_posts = post_scrapper(page="kaisens")
	
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




