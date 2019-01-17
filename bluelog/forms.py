# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from bluelog.models import Category, Channel


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 70)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]

#lsc
class WebsiteForm(FlaskForm):
    title = StringField('Website Title', validators=[DataRequired(), Length(1, 60)])
    channel = SelectField('Channel', coerce=int, default=1)
    description = TextAreaField('Description')
    url = StringField('URL')
    icon_file = StringField('Image_URL')
    icon_file_m = StringField('Image_URL')
    icon_file_s = StringField('Image_URL')
    flag = IntegerField()
    priority = IntegerField()
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(WebsiteForm, self).__init__(*args, **kwargs)
        self.channel.choices = [(channel.id, channel.title)
                                 for channel in Channel.query.order_by(Channel.title).all()]

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')

#lsc
class ChannelForm(FlaskForm):
    title = StringField('Channel Title', validators=[DataRequired(), Length(1, 30)])
    description = TextAreaField('Description')
    icon_file = StringField('Image_URL')
    icon_file_m = StringField('Image_URL')
    icon_file_s = StringField('Image_URL')
    submit = SubmitField()

    def validate_name(self, field):
        if Channel.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()

#lsc
#class ChannelForm(FlaskForm):
#    name = StringField('Channel Name',validators = [DataRequired(), Length(1,30)])
#    submit = SubmitField()

#    def validate_name(self, field):
#        if Channel.query.filter_by(name=field.data).first():
#            raise ValidationError('Name already in use.')
#lsc
#class WebsiteForm(FlaskForm):
#    name = StringField('Web Name', validators = [DataRequired(), Length(1,30)])
#    channel = SelectField('Channel', coerce=int, default=1)
#    submit = SubmitField()
	
#    def __init__(self, *args, **kwargs):
#        super(WebsiteForm, self).__init__(*args, **kwargs)
#        self.channel.choices = [(channel.id, channel.name)
#                                 for channel in Channel.query.order_by(Channel.name).all()]


