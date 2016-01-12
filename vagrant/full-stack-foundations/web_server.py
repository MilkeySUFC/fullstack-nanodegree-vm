# SQLAlchemy 
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

# Web Server
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# Restaurant Database
from database_setup import Base, Restaurant, MenuItem

# Bleach
import bleach

# Set up SQLite database 
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			# Clear output string
			output = ""

			if self.path.endswith("/delete"):
				# Set up delete_restaurant_id
				delete_restaurant_id = self.path.split("/")[2]

				# Return this restaurant
				delete_restaurant = session.query(Restaurant).filter_by(id = delete_restaurant_id).one()

				if delete_restaurant != []:
					# Build HTML output string
					output = "<html><body>"

					# Form for deleting the restaurant
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % delete_restaurant_id
					output += "<h2>Do you want to delete restaurant: %s</h2>" % delete_restaurant.name
					output += "</br>"
					output += "<input type='submit' value='Delete'>"
					output += "</form>"
				
			if self.path.endswith("/edit"):
				# Set up edit_restaurant_id
				edit_restaurant_id = self.path.split("/")[2]

				# Return this restaurant
				edit_restaurant = session.query(Restaurant).filter_by(id = edit_restaurant_id).one()

				if edit_restaurant != []:
					# Build HTML output string
					output = "<html><body>"

					# Form for editing the restaurant
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % edit_restaurant_id
					output += "<h2>Edit restaurant name</h2>"
					output += "<input name='restaurant' type='text' placeholder='%s'>" % edit_restaurant.name
					output += "<input type='submit' value='Rename'>"
					output += "</form>"

			if self.path.endswith("/restaurants/new"):
				# Build HTML output string
				output = "<html><body>"

				# Form for adding the new restaurant
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<h2>What is the name of the new restaurant?</h2>"
				output += "<input name='restaurant' type='text'><input type='submit' value='Submit'>"
				output += "</form>"

			elif self.path.endswith("/restaurants"):
				# Build HTML output string
				output = "<html><body>"

				#Add Link to Make New Restaurant
				output += "<a href='/restaurants/new'>Make a new restaurant</a>"
				output += "</br>"
				output += "</br>"

				# check if any restaurants in database
				if session.query(Restaurant).count() == 0:
					output += "<h2>No Restaurants to show<h2>"

				else:
					# Query database for restaurants
					restaurants = session.query(Restaurant).order_by('name').all()

					# Loop through each restaurant, add HTML
					for restaurant in restaurants:
						output += restaurant.name
						output += "</br>"
						output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
						output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
						output += "</br></br>"

			elif self.path.endswith("/hello"):
				output += "<html><body>Hello!!"

				output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
				output += "<h2>What would you like me to say?</h2>"
				output += "<input name='message' type='text'><input type='submit' value='Submit'>"
				output += "</form>"
				output += "</body></html>"

			elif self.path.endswith("/hola"):
				output += "<html><body>&#161Hola!! <a href='/hello'>Back to Hello</a>"

				output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
				output += "<h2>What would you like me to say?</h2>"
				output += "<input name='message' type='text'><input type='submit' value='Submit'>"
				output += "</form>"
				output += "</body></html>"

			if output != "":
				# Send response/headers
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				# End HTML
				output += "</body></html>"

				# Write HTML output
				self.wfile.write(output)
				print output

				return


		except IOError:
			self.send_error(404, 'File not found %s' % self.path)

	def do_POST(self):
		try:
			# Return content/headers data
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)

				if self.path.endswith("/delete"):
					# Set up delete_restaurant_id
					delete_restaurant_id = self.path.split("/")[2]

					# Return this restaurant
					delete_restaurant = session.query(Restaurant).filter_by(id = delete_restaurant_id).one()

					session.delete(delete_restaurant)

				if self.path.endswith('/edit'):
					# Set up edit_restaurant_id
					edit_restaurant_id = self.path.split("/")[2]

					# Return this restaurant
					edit_restaurant = session.query(Restaurant).filter_by(id = edit_restaurant_id).one()

					edit_restaurant.name = bleach.clean(fields.get('restaurant')[0])

					# Add to database
					session.add(edit_restaurant)

				if self.path.endswith('/restaurants/new'):
					# Instantiate New restaurant object & set name field
					new_restaurant = Restaurant(name = bleach.clean(fields.get('restaurant')[0]))

					# Add to database
					session.add(new_restaurant)

				# Commit after POST action
				session.commit()

				# Send response/headers
				self.send_response(301)
				self.send_header('Content-type','text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

				return

		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)

		print "Web Server Started on port %s" % port

		server.serve_forever()

	except KeyboardInterrupt:
		print "^C pressed. Stopping Web Server..."
		server.socket.close()


if __name__ == '__main__':
	main()
