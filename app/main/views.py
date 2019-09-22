import markdown2
from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from .forms import PitchForm, CommentForm, UpvoteForm
from .. import db
from ..models import Pitch, User,Comment,Upvote,Downvote
from flask_login import login_required, current_user
from flask.views import View,MethodView



# Views
@main.route('/', methods = ['GET','POST'])
def index():

    '''
    View root page function that returns the index page and its data
    '''

    pitch= Pitch.query.filter_by().first()

    title = 'Home - Welcome to our pitch-app Website Online'

    pickup = Pitch.query.filter_by(category = "pickup")
    interview = Pitch.query.filter_by(category = "interview")
    promotion = Pitch.query.filter_by(category = "promotion")
    product = Pitch.query.filter_by(category = "product")
    
    upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)


    return render_template('category.html', title = title, pitch = pitch, pickup = pickup, interview = interview, promotion = promotion, product = product)



@main.route('/pitches/new/', methods = ['GET', 'POST'])
@login_required
def new_pitch():
    form = PitchForm()
    my_upvotes = Upvote.query.filter_by(pitch_id = Pitch.id)

    if form.validate_on_submit():
       description = form.description.data
       title = form.title.data
       owner_id = current_user
       category = form.category.data
       print(current_user._get_current_object().id)
       new_pitch = Pitch(owner_id = current_user._get_current_object().id, title = title, description=description, category=category)
       db.session.add(new_pitch)
       db.session.commit()
       return redirect(url_for('main.index'))
    return render_template('pitch.html',form=form)

@main.route('/comment/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def new_comment(pitch_id):
    form = CommentForm()
    pitch=Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, pitch_id = pitch_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', pitch_id= pitch_id))

    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    return render_template('comment.html', form = form, comment = all_comments, pitch = pitch )


@main.route('/pitch/upvote/<int:pitch_id>/upvote', methods = ['GET', 'POST'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id= pitch_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))


    new_upvote = Upvote(pitch_id=pitch_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))



@main.route('/pitch/downvote/<int:pitch_id>/downvote', methods = ['GET', 'POST'])
@login_required
def downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_downvotes = Downvote.query.filter_by(pitch_id= pitch_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))


    new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))




    
