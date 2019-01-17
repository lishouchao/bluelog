# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint
from flask_login import login_required, current_user

from bluelog.extensions import db
from bluelog.forms import SettingForm, PostForm, CategoryForm, LinkForm, ChannelForm, WebsiteForm
from bluelog.models import Post, Category, Comment, Link, Channel, Website
from bluelog.utils import redirect_back

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Setting updated.', 'success')
        return redirect(url_for('blog.index'))
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', page=page, pagination=pagination, posts=posts)

#lsc manage website
@admin_bp.route('/website/manage')
@login_required
def manage_website():
    page = request.args.get('page', 1, type=int)
    pagination = Website.query.order_by(Website.id.desc()).paginate(
        page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    websites = pagination.items
    return render_template('admin/manage_website.html', page=page, pagination=pagination, websites=websites)


@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        # same with:
        # category_id = form.category.data
        # post = Post(title=title, body=body, category_id=category_id)
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)

#lsc new a Website 
@admin_bp.route('/website/new', methods=['GET', 'POST'])
@login_required
def new_website():
    form = WebsiteForm()
    if form.validate_on_submit():
        #put form's value to variables
        title = form.title.data
        description = form.description.data
        url = form.url.data
        channel = Channel.query.get(form.channel.data)
        icon_file = form.icon_file.data
        icon_file_m = form.icon_file_m.data
        icon_file_s = form.icon_file_s.data
        flag = form.flag.data
        priority = form .flag.data

        website = Website(title=title, description=description,url=url, channel=channel,
                          icon_file=icon_file, icon_file_m=icon_file_m, icon_file_s=icon_file_s,
                          flag=flag, priority=priority)
        # same with:
        # category_id = form.category.data
        # post = Post(title=title, body=body, category_id=category_id)
        db.session.add(website)
        db.session.commit()
        flash('Website created.', 'success')
        return redirect(url_for('blog.show_website', website_id=website.id))
    return render_template('admin/new_website.html', form=form)


@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)

#lsc edit a website
@admin_bp.route('/website/<int:website_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_website(website_id):
    form = WebsiteForm()
    website = Website.query.get_or_404(website_id)
    if form.validate_on_submit():
        website.title = form.title.data
        website.description = form.description.data
        website.url = form.url.data
        website.channel = Channel.query.get(form.channel.data)
        website.icon_file = form.icon_file.data
        website.icon_file_m = form.icon_file_m.data
        website.icon_file_s = form.icon_file_s.data
        website.flag = form.flag.data
        website.priority = form.priority.data

        db.session.commit()
        flash('Website updated.', 'success')
        return redirect(url_for('blog.show_website', website_id=website.id))
    form.title.data = website.title
    form.description.data =website.description
    form.url.data = website.url
    form.channel.data = website.channel_id
    form.icon_file.data = website.icon_file
    form.icon_file_m.data = website.icon_file_m
    form.icon_file_s.data = website.icon_file_s
    form.flag.data = website.flag
    form.priority.data = website.priority

    return render_template('admin/edit_website.html', form=form)

@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect_back()

#lsc delete a website
@admin_bp.route('/website/<int:website_id>/delete', methods=['POST'])
@login_required
def delete_website(website_id):
    website = Website.query.get_or_404(website_id)
    db.session.delete(website)
    db.session.commit()
    flash('Website deleted.', 'success')
    return redirect_back()

@admin_bp.route('/post/<int:post_id>/set-comment', methods=['POST'])
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('Comment disabled.', 'success')
    else:
        post.can_comment = True
        flash('Comment enabled.', 'success')
    db.session.commit()
    return redirect_back()


@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    filter_rule = request.args.get('filter', 'all')  # 'all', 'unreviewed', 'admin'
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(from_admin=True)
    else:
        filtered_comments = Comment.query

    pagination = filtered_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html', comments=comments, pagination=pagination)


@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('Comment published.', 'success')
    return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect_back()


@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')

#lsc channel manage
@admin_bp.route('/channel/manage')
@login_required
def manage_channel():
    return render_template('admin/manage_channel.html')

@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Category created.', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html', form=form)

#lsc channel new
@admin_bp.route('/channel/new', methods=['GET', 'POST'])
@login_required
def new_channel():
    form = ChannelForm()
    if form.validate_on_submit():
        title = form.title.data
        description =  form.description.data
        icon_file = form.icon_file.data
        icon_file_m = form.icon_file_m.data
        icon_file_s = form.icon_file_s.data

        channel = Channel(name=name)
        db.session.add(channel)
        db.session.commit()
        flash('Channel created.', 'success')
        return redirect(url_for('.manage_channel'))
    return render_template('admin/new_channel.html', form=form)

@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not edit the default category.', 'warning')
        return redirect(url_for('blog.index'))
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated.', 'success')
        return redirect(url_for('.manage_category'))

    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)

#lsc Channel edit
@admin_bp.route('/channel/<int:channel_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_channel(channel_id):
    form = ChannelForm()
    channel = Channel.query.get_or_404(channel_id)
    if channel.id == 1:
        flash('You can not edit the default channel.', 'warning')
        return redirect(url_for('blog.index'))
    if form.validate_on_submit():
        channel.title = form.title.data
        channel.description = form.description.data
        channel.icon_file = form.icon_file.data
        channel.icon_file_m = form.icon_file.data
        channel.icon_file_s = form.icon_file.data

        db.session.commit()
        flash('Channel updated.', 'success')
        return redirect(url_for('.manage_channel'))

    form.title.data = channel.title
    form.description.data = channel.description
    form.icon_file.data = channel.icon_file
    form.icon_file_m.data = channel.icon_file_m
    form.icon_file_s.data = channel.icon_file_s

    return render_template('admin/edit_channel.html', form=form)

@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not delete the default category.', 'warning')
        return redirect(url_for('blog.index'))
    category.delete()
    flash('Category deleted.', 'success')
    return redirect(url_for('.manage_category'))

#lsc channel delete
@admin_bp.route('/channel/<int:channel_id>/delete', methods=['POST'])
@login_required
def delete_channel(channel_id):
    channel = Channel.query.get_or_404(channel_id)
    if channel.id == 1:
        flash('You can not delete the default channel.', 'warning')
        return redirect(url_for('blog.index'))
    channel.delete()
    flash('Channel deleted.', 'success')
    return redirect(url_for('.manage_channel'))

@admin_bp.route('/link/manage')
@login_required
def manage_link():
    return render_template('admin/manage_link.html')


@admin_bp.route('/link/new', methods=['GET', 'POST'])
@login_required
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        link = Link(name=name, url=url)
        db.session.add(link)
        db.session.commit()
        flash('Link created.', 'success')
        return redirect(url_for('.manage_link'))
    return render_template('admin/new_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_link(link_id):
    form = LinkForm()
    link = Link.query.get_or_404(link_id)
    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        db.session.commit()
        flash('Link updated.', 'success')
        return redirect(url_for('.manage_link'))
    form.name.data = link.name
    form.url.data = link.url
    return render_template('admin/edit_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Link deleted.', 'success')
    return redirect(url_for('.manage_link'))
