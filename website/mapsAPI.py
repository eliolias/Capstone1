from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import urllib.request, json
import requests
from . import db
from .models import SavedRoute
from .apiKey import api_key

mapsAPI = Blueprint('mapsAPI', __name__)

endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'


#waypoints = []


@mapsAPI.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        origin = request.form.get('origin').replace(' ','+')
        destination = request.form.get('destination').replace(' ','+')
        destinationRaw = request.form.get('destination')
        originRaw = request.form.get('origin')
        routeName = request.form.get('routeName')
        if len(origin) < 1:
            flash('Empty origin, try again!', category='error')
        elif len(destination) < 1:
            flash('Empty destination, try again!', category='error')
        elif len(routeName) < 1:
            flash('Empty route name, try again!', category='error')
        else:
            nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
            APIrequest = endpoint + nav_request
            response = urllib.request.urlopen(APIrequest).read()
            directions = json.loads(response)
            routes = directions['routes']

            savedRoute = SavedRoute.query.filter_by(routeName=routeName).first()
            if savedRoute:
                flash('Route already exists!', category='error')
            elif directions == []:
                flash('Invalid route, try again!', category='error')
            elif routes == []:
                flash('Invalid route, try again!', category='error')
            else:
                print('QQQQQ', routes)
                summary = routes[0]['summary']
                newRoute = SavedRoute(routeName=routeName, origin=origin, originRaw=originRaw, destination=destination, destinationRaw=destinationRaw, summary=summary, user_id=current_user.id )
                db.session.add(newRoute)
                db.session.commit()
                flash('Route Saved!', category='success')
        
    return render_template("home.html", user=current_user)

@mapsAPI.route('/delete-route', methods=['POST'])
def delete_route():
    route = json.loads(request.data)
    routeId = route['routeId']
    route = SavedRoute.query.get(routeId)
    if route:
        if route.user_id == current_user.id:
            db.session.delete(route)
            db.session.commit()
    flash('Route deleted!', category='success')
    return jsonify({})

