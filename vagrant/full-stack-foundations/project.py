# Import Flask
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

# Imports for SQLAlchemy 
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

# Import Restaurant Database
from database_setup import Base, Restaurant, MenuItem


#Create instance of Flask
app = Flask(__name__)

# Set up SQLite database session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Make API Endpoints (GET requests)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')

def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id). one()
	menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)

	return jsonify(MenuItems=[item.serialise for item in menuItems])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')

def restaurantMenuItem(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	
	return jsonify(MenuItem=[menuItem.serialise])

@app.route('/')
@app.route('/restaurants/')

def restaurantList():
	restaurants = session.query(Restaurant).all()

	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurants/new/')

def restaurantNew():
		return redirect(url_for('restaurantList'))


@app.route('/restaurants/<int:restaurant_id>/')

def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id). one()
	menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)

	return render_template('menu.html', restaurant = restaurant, items = menuItems)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET', 'POST'])

def newMenuItem(restaurant_id):
	if request.method == "POST":
		newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)

		session.add(newItem)
		session.commit()

		flash('New menu item created')

		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET', 'POST'])

def editMenuItem(restaurant_id, menu_id):
	editItem = session.query(MenuItem).filter_by(id = menu_id).one()

	if request.method == "POST":
		editItem.name = request.form['name']

		session.add(editItem)
		session.commit()

		flash('Menu Item edited')

		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

	else:
	    return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editItem)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])

def deleteMenuItem(restaurant_id, menu_id):
	deleteItem = session.query(MenuItem).filter_by(id = menu_id).one()

	if request.method == "POST":
		session.delete(deleteItem)
		session.commit()

		flash('Menu Item deleted')

		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

	else:
	    return render_template('deletemenuitem.html', item = deleteItem)



if __name__ == '__main__':
	app.secret_key = 'my_totally_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)