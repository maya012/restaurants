from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bin = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Making an API Endpoint for getting restaruant menu(GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

# Making an API Endpoint for getting restaruant menu(GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def MenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)

# Create route for the root
@app.route('/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

# Create route for the restaurantMenu function
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

# Create route for newMenuItem function
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        if request.form['name']:
            newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course= request.form['course'], restaurant_id=restaurant_id)
            session.add(newItem)
            session.commit()
            flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuItem.html', restaurant_id=restaurant_id)

# Create route for editMenuItem function
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        if request.form['price']:
            editItem.price = request.form['price']
        if request.form['course']:
            editItem.course = request.form['course']
        session.add(editItem)
        session.commit()
        flash("Menu Item has been edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=editItem)

# Create a route for deleteMenuItem function
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("Menu Item has been deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuItem.html', i=deleteItem)

# Start local host web server with port numver 5000
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
