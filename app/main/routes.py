from flask import render_template, url_for, redirect, flash, request, jsonify, session, abort
from app.extensions.forms import  EditProfile, community, searchForm
from app.extensions.models import User, Community, community_members, Messages
from app.main import bp
from flask import current_app 
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions.greeting import greeting
import requests
import random
from app import socketio, db
from flask_socketio import join_room, leave_room, send
from sqlalchemy import select, and_

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    
@bp.route('/welcome', methods=['GET', 'POST'])
@login_required
def dashboard():
    
    if current_user.confirmed != True:
        return redirect(url_for('auth.inactive'))
    
    greet = greeting()
    created_communities = Community.query.filter_by(created_by_user_id=current_user.id)
    global_communities = Community.query.all() 
        
    joined = User.query.get(current_user.id).communities
                
    return render_template('main/Dashboard.html', title='Dashboard', greeting=greet, my_communities=created_communities,
                           globals=global_communities, joined=joined)   


@bp.route('/coin-data', methods=['GET'])
def get_latest_prices(limit=50, convert='USD'):
    CMC_API_KEY = current_app.config.get("CMC_API_KEY")
    page = int(request.args.get('page', 1))
    offset = (page - 1) * limit
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    params = {
        'start': offset + 1,
        'limit': limit,
        'convert': convert
    }
    headers = {
        'X-CMC_PRO_API_KEY': CMC_API_KEY
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    coins_data = data['data']
    total_count = data['status'].get('total_count', 0)
    coins = []
    for coin in coins_data:
        coins.bpend({
            'name': coin['name'],
            'symbol': coin['symbol'],
            'rank' : coin['cmc_rank'],
            'price': round(float(coin['quote'][convert]['price']), 2),
            'circulating_supply': round(float(coin['circulating_supply'])),
            'volume_24h': round(float(coin['quote'][convert]['volume_24h'])),
            'percent_change_in_1h': round(float(coin['quote'][convert]['percent_change_1h']), 2),
            'percent_change_in_24h': round(float(coin['quote'][convert]['percent_change_24h']), 2),
            'percent_change_in_7d': round(float(coin['quote'][convert]['percent_change_7d']), 2)
        })
    return jsonify({'coins': coins, 'total_count': total_count})

@bp.route('/coin-listing', methods=['GET', 'POST'])
def coin_listing():
    greet = greeting()       
    return render_template('main/coins.html', title='Coins and Prices', greeting=greet)

@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    if username == current_user.username:
        user = User.query.filter_by(username=username).first_or_404()
        greet = greeting()
        user_created = Community.query.filter_by(created_by_user_id=current_user.id).all()
        joined = User.query.get(current_user.id).communities
        return render_template('main/profile.html', title='Profile', user=user, greeting=greet,
                               user_group=user_created, joined=joined)
    else:
        user = User.query.filter_by(username=username).first_or_404()
        greet = greeting()
        user_created = Community.query.filter_by(created_by_user_id=user.id).all()
        joined = User.query.get(user.id).communities
        
        return render_template('main/visitor_profile.html', title='Profile', user=user, greeting=greet,
                               user_group=user_created, joined=joined)
        
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    greet = greeting()
    form = EditProfile(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile has been updated!!!', 'success')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html', title='Edit Profile', form=form, greeting=greet)
                        
@bp.route('/create_community', methods=['GET','POST'])
@login_required
def create_community():
    form = community()
    if form.validate_on_submit():
        # form is valid, proceed with creating the community
        communities = Community(name=form.name.data, about=form.about.data, created_by_user_id=current_user.id )
        db.session.add(communities)
        db.session.commit()
        flash(f'{communities.name} has been created successfully!!!', 'success')
        return redirect(url_for('dashboard'))
    else:
        return render_template('main/create_community.html', user=current_user, form=form)
       
@bp.route('/about')
def about():
    greet = greeting()
    return render_template('main/about.html', greeting=greet)
  
@bp.route('/delete/<community>', methods=["GET", "POST"])
@login_required
def remove_community(community):
 
    group= Community.query.filter_by(name=community).first()
      
    if group:
        db.session.delete(group)
        db.session.commit()
        
        flash(f"{group.name} has been deleted successfully", "success")
    else:
        db.session.rollback()
        flash("Operation was not successful!!!", "warning")
    return redirect(url_for('user', username=current_user.username))
 
@bp.route('/join_community/<int:community_id>', methods=["GET", "POST"])
@login_required
def join_community(community_id):
    creator_id = Community.query.get(community_id).created_by_user_id
    
    if current_user.id != creator_id:
        stmt = select(community_members).where(and_(
            community_members.c.user_id == current_user.id, 
            
            community_members.c.community_id == community_id
            ))
        
        result = db.session.execute(stmt)
        
        row = result.fetchone()
        
        if row is not None:
                flash("You have already joined this group!!!", "warning")
                return redirect(url_for('dashboard'))
                    
        else: 
                db.session.execute(
                    community_members.insert().values(
                    community_id = community_id,
                    user_id = current_user.id
                    )
                )
                db.session.commit()
                db.session.close()
        flash('You have joined the group!!!', "success")
        return redirect(url_for('dashboard'))
    
    else:
        
        flash("You created this group!!!", "warning")
        return redirect(url_for('dashboard'))
    
@bp.route('/leave_community/<int:community_id>', methods=['GET', 'POST'])
@login_required
def leave_group(community_id):
    user_id = current_user

    if current_user:
        db.session.query(community_members).filter(
            community_members.c.community_id == community_id,
            community_members.c.user_id == current_user.id
        ).delete()
        db.session.commit()
        flash("You have left the group!!!", 'success')
        
        return redirect(url_for('user', username=current_user.username))
            
@bp.route('/community/<community>', methods=['GET', 'POST'])
@login_required
def community_chat(community):
    user = User.query.filter_by(username=current_user.username).first_or_404()
    session['room'] = community
    room = session.get('room')
    colors = ['red', 'blue', 'green', 'cyan', 'purple', 'crimson', 'beige', 'chocolate']
    color = random.choice(colors)
    
    if room is None or session.get('room') is None:
        return redirect(url_for('dashboard'))
    
    return render_template('community_room/community.html', user=user, group_name=room, colors=color)  

@socketio.on("message")
def message(data):
    room = session.get("room")
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    room_id = Community.query.filter_by(name=room).first_or_404().id
    message = Messages(content=data['data'], user_id=current_user.id, sender_type=current_user.username, timestamp=datetime.now(), community_id=room_id)
    db.session.add(message)
    db.session.commit()
    send(content, to=room)
    
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on('connect')
def connect(auth):
    room = session.get('room')
    
    if not room:
        return
    
    if room is None:
        leave_room(room)
    
    join_room(room)
    community = Community.query.filter_by(name=room).first_or_404()
    room_id = community.id

    # Fetch all messages for the community in a single query
    messages = Messages.query.filter_by(community_id=room_id).all()

    # Loop through each message
    for message in messages:
        user = User.query.get(message.user_id)
        if not user:
            abort(404, description=f"User with ID {message.user_id} not found")

        # Format the timestamp
        try:
            dt = datetime.strptime(str(message.timestamp), "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            dt = datetime.strptime(str(message.timestamp), "%Y-%m-%d %H:%M:%S")
        
        formatted_date = dt.strftime("%B %d, %Y %H:%M")
        
        # Construct the message
        sms = f"{message.content} {formatted_date}"
        
        # Print and send the message
        print(user.username)
        print(sms)
        send({"name": user.username, "message": sms}, to=room)

@socketio.on('disconnect')
def disconnect():
    room = session.get('room')
    name = session.get('name')
    leave_room(room)
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room")

@bp.route('/search', methods=['GET', 'POST'])
def search(convert='USD'):
    CMC_API_KEY=current_app.config.get("CMC_API_KEY")
    form = searchForm()
    if request.method == "POST":
        session['search_term'] = request.form.get('search')
        data = session.get('search_term')
        groups = Community.query.filter(Community.name.like('%' + data + '%')).all() 
        users = User.query.filter(User.username.like('%' + data + '%')).all()
        groups_count = Community.query.filter(Community.name.like('%' + data + '%')).count()
        users_count = User.query.filter(User.username.like('%' + data + '%')).count()
        count = groups_count + users_count
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        
    params = {
            'symbol': data,
            'convert': convert
        }
        
    headers = {
            'X-CMC_PRO_API_KEY': CMC_API_KEY
        }
    try:       
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
                
        coin_data = response.json()
                
        coins_data = coin_data['data']
        
        
        coins = []
                
    
        for coin_symbol, coin in coins_data.items(): 
            '''Note the coin_symbol and coin serve as key/value pairs for the coins_data dictionary which is returned as 
            a tuple when .items() method is used, the search term operates using the symbol of the coin to fetch value of coins'''
            coins.append({
                'name': coin['name'],
                'symbol': coin['symbol'],
                'rank' : coin['cmc_rank'],
                'price': round(float(coin['quote'][convert]['price']), 2),
                'circulating_supply': round(float(coin['circulating_supply'])),
                'volume_24h': round(float(coin['quote'][convert]['volume_24h'])),
                'percent_change_in_1h': round(float(coin['quote'][convert]['percent_change_1h']), 2),
                'percent_change_in_24h': round(float(coin['quote'][convert]['percent_change_24h']), 2),
                'percent_change_in_7d': round(float(coin['quote'][convert]['percent_change_7d']), 2)
            })
                    
    except requests.exceptions.RequestException as e:
        pass
    

    count += len(coins) 
      
    
    return render_template('search.html', form=form, result=data, groups=groups, users=users, 
                            count=count, greeting=greeting(), coins=coins)
        
@bp.context_processor
def base():
    form = searchForm()
    return dict(form=form)



        

