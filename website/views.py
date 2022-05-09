
import json
from flask import Blueprint, render_template , request ,flash ,jsonify
from flask_login import login_required,  current_user
from .models import Contact
import re
from . import db

# regular ecpression for email 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

views = Blueprint('views', __name__)


@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        print(name,phone,email,address)
        if len(name)< 2:
            flash("Name is too short" , category='error')
        elif len(phone) != 10 :
            flash("Phone no should contain 10 digit" , category='error')
        elif not re.fullmatch(regex, email) :
            flash("Please enter valid email" , category='error')
        elif len(address) < 1:
            flash("Please enter proper address" , category='error')
        else:
            new_contact= Contact(
            name = name ,
            phone_no = phone ,
            email = email,
            address = address, 
            user_id=current_user.id)
            print(new_contact)
            db.session.add(new_contact)
            db.session.commit()
            flash('Contact added successfully',category='success')


    return render_template('home.html', user=current_user)
# delete route

@views.route('/delete-contact' , methods=['DELETE'])
@login_required
def delete_note():
    contact=json.loads(request.data)
    contactId=contact['id']
    contact = Contact.query.get(contactId)
    if contact:
        if contact.user_id == current_user.id:
            db.session.delete(contact)
            db.session.commit()
            return jsonify({})

# update route
@views.route('/update_contact/<int:id>' , methods=['POST','UPDATE','GET'])
@login_required
def update_contact(id):
    contact_to_update = Contact.query.get_or_404(id)
    if request.method== "POST":
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        if len(name)< 2:
            flash("Name is too short" , category='error')
        elif len(phone) != 10 :
            flash("Phone no should contain 10 digit" , category='error')
        elif not re.fullmatch(regex, email) :
            flash("Please enter valid email" , category='error')
        elif len(address) < 1:
            flash("Please enter proper address" , category='error')
        else:
            contact_to_update.name=name
            contact_to_update.phone_no=phone
            contact_to_update.email=email
            contact_to_update.address=address
            try:
                db.session.commit()
                flash('Contact updated successfully',category='success')
                return render_template('update_contact.html',
                user=current_user,
                contact_to_update_details=contact_to_update
                )
            except:
                flash('Error. Looks like something went wrong , try again !',category='error')
                return render_template('update_contact.html',
                user=current_user,
                contact_to_update_details=contact_to_update
                )
    else:
         return render_template('update_contact.html',
                user=current_user,
                contact_to_update_details=contact_to_update
                )
    return render_template('update_contact.html',
                user=current_user,
                contact_to_update_details=contact_to_update
                )

# search route
@views.route('/search',methods=['POST','GET'])
@login_required
def search():
    if request.method=='POST':
        query=request.form.get('query')
        print(query)
        searched_contacts=Contact.query.filter(Contact.name.like("%"+query+"%") ).all()
        return(render_template('search.html',user=current_user,searched_contacts = searched_contacts))
    




    return(render_template('search.html',user=current_user))



            
            


   






