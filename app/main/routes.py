from .forms import EditProfileForm, EmptyForm, PostForm
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Post
from datetime import datetime, timezone
from app.main import bp

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live")
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(current_user.following_posts(), page=page,
                        per_page=current_app.config['POST_PER_PAGE'], error_out=False)
    next_url = url_for('main.index', page=posts.next_num) \
    if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
    if posts.has_prev else None
    # posts = db.session.scalars(current_user.following_posts()).all()
    return render_template("index.html", title='Home Page', form=form,
                           posts=posts, next_url=next_url, prev_url=prev_url)


@bp.route("/user/<username>")
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username==username))
    page = request.args.get('page', 1, int)
    query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=current_app.config['POST_PER_PAGE'],
                        error_out=False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form,
                           next_url=next_url, prev_url=prev_url)


@bp.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.about_me=form.about_me.data
        db.session.commit()
        flash("Changes have been applied")
        return redirect(url_for('main.edit_profile'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.about_me.data=current_user.about_me
    return render_template("edit_profile.html", form=form)



@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username==username)
        )
        if user is None:
            flash ("Username not found")
            return redirect(url_for("index"))
        if user == current_user:
            flash("You cannot follow yourself")
            return redirect(url_for("main.user", username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f"You are now following {username}")
        return redirect(url_for("main.user", username=username))
    else:
        return redirect(url_for("index"))
    


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username==username)
        )
        if user is None:
            flash ("Username not found")
            return redirect(url_for("index"))
        if user == current_user:
            flash("You cannot unfollow yourself")
            return redirect(url_for("main.user", username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f"You have unfollowed {username}")
        return redirect(url_for("main.user", username=username))
    else:
        return redirect(url_for("index"))
    
        
@bp.route('/explore')
@login_required
def explore():
    query = sa.select(Post).order_by(Post.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(query, page=page,
                        per_page=current_app.config['POST_PER_PAGE'], error_out=False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url= next_url, prev_url=prev_url)


@bp.route('/delete/<postId>', methods=['POST'])
@login_required
def delete(postId):
    query = current_user.posts.delete().where(Post.id==postId)
    db.session.execute(query)
    db.session.commit()
    flash(f'You post has been deleted.')
    return redirect(url_for('main.user', username=current_user.username))
