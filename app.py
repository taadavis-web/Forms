from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.secret_key = 'top-secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

admin = Admin(app, name='frmstr')


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    quan = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text)
    rel = db.Column(db.String(50), nullable=False)
    accommodations = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


admin.add_view(ModelView(Profile, db.session))


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


admin.add_view(ModelView(Feedback, db.session))

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return redirect(url_for('profile'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        quan = request.form.get('quan', '').strip()
        comments = request.form.get('comments', '').strip()
        rel = request.form.get('rel', '').strip()
        accommodations = request.form.get(
            'accommodations') == "yes"  # True if checked

        # Validation
        if not name or not email or not quan or not rel:
            error = "Please fill in all required fields"
            return render_template('profileForm.html', error=error)

        # Create new profile in database
        try:
            new_profile = Profile(
                name=name,
                email=email,
                quan=int(quan),
                comments=comments,
                rel=rel,
                accommodations=accommodations
            )
            db.session.add(new_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = "An error occurred while saving your profile. Please try again."
            return render_template('profileForm.html', error=error)

        return render_template(
            'profileSuccess.html',
            name=name,
            email=email,
            quan=quan,
            comments=comments,
            rel=rel,
            accommodations=accommodations
        )

    return render_template('profileForm.html')


@app.route('/admin/profiles/delete_first')
def admin_profiles_deleteFirst():
    try:

        all_profiles = Profile.query.order_by(Profile.id).all()

        if len(all_profiles) < 1:
            error = "You have no profiles to delete"
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)

        first_profile = all_profiles[0]

        db.session.delete(first_profile)
        db.session.commit()

        return redirect(url_for('admin_profiles'))
    except Exception as e:
        error = f"Error deleting profile: {str(e)}"
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=error)


@app.route('/admin/profiles/deleteCoworker')
def admin_profiles_deleteCoworker():
    try:
        deleted_count = Profile.query.filter_by(rel="coworker etc.").delete()

        db.session.commit()

        return redirect(url_for('admin_profiles'))
    except Exception as e:
        error = f"Error deleting coworker profiles: {str(e)}"
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=error)


@app.route('/admin/profiles/deleteAudaciousGuest')
def admin_profiles_delete_audacious_guests():
    try:
        deleted_count = Profile.query.filter(Profile.quan > 5).delete()

        db.session.commit()

        return redirect(url_for('admin_profiles'))
    except Exception as e:
        error = f"Error deleting audacious profiles: {str(e)}"
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=error)


@app.route('/admin/profiles/deleteQuantity', methods=['POST'])
def admin_profilesDeleteByQuantity():
    try:
        quantity_str = request.form.get('quantity', '').strip()

        if not quantity_str:
            error = "Please enter a quantity"
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)

        try:
            quantity = int(quantity_str)
        except ValueError:
            error = "Please enter a valid number"
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)

        profiles_to_delete = Profile.query.filter(Profile.quan >= quantity)

        if not profiles_to_delete:
            error = f"No profiles found with {quantity} or more guests."
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profile, error=error)

        for profile in profiles_to_delete:
            db.session.delete(profile)

        db.session.commit()

        return redirect(url_for('admin_profiles'))

    except Exception as e:
        error = f"Error deleting profiles: {str(e)}"
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=error)


@app.route('/admin/profiles/AppendComments')
def admin_profiles_appendComments():
    try:
        profiles_to_update = Profile.query.filter_by(accommodations=True).all()

        for profile in profiles_to_update:
            if "email accommodations form" not in profile.comments:
                profile.comments += " - email accommodations form"

        db.session.commit()

        # profiles = Profile.query.all()
        # return render_template('admin_profiles.html', profiles=profiles, error=errorMsg)

        return redirect(url_for('admin_profiles'))

    except Exception as e:
        db.session.rollback()
        errorMsg = f"Error updating profiles: {str(e)}"
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=errorMsg)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    method = request.form.get('requestMethod', '')

    if request.method == 'DELETE' or method == 'DELETE':
        id = request.form.get('feedbackId')
        try:
            # thisFeedback = Feedback.query.filter_by(id=id).delete()

            feedback = db.session.query(Feedback).filter(
                Feedback.id == id).first()
            db.session.delete(feedback)
            db.session.commit()

            # user = db.session.query(User).filter(User.my_id==1).first()
            # db.session.delete(user)
        except Exception as e:
            db.session.rollback()
            error = "An error occurred while deleting the record. Please try again."
            return redirect(url_for('admin_feedback'))
        return redirect(url_for('admin_feedback'))
    elif request.method == 'POST':
        rating = request.form.get('rating', '').strip()
        comment_text = request.form.get('feedback', '').strip()
        if not rating:
            error = "Please provide a rating"
            return render_template('feedbackForm.html', error=error)

        # Create new feedback in database
        try:
            new_feedback = Feedback(
                rating=int(rating),
                comment=comment_text
            )
            db.session.add(new_feedback)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = "An error occurred while saving your feedback. Please try again."
            return render_template('feedbackForm.html', error=error)

        return render_template(
            'feedbackSuccess.html',
            rating=rating,
            comment=comment_text
        )

    return render_template('feedbackForm.html')


@app.route('/admin/profiles')
def admin_profiles():
    profiles = Profile.query.all()
    return render_template('admin_profiles.html', profiles=profiles)


@app.route('/admin/profiles/sibling')
def admin_profiles_sibling():
    profiles = Profile.query.filter(Profile.rel == "sibling").all()
    return render_template('admin_profiles.html', profiles=profiles)


@app.route('/admin/feedback')
def admin_feedback():
    feedbacks = Feedback.query.all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)


@app.route('/admin/feedback/rating_1')
def admin_feedback_rating_1():
    feedbacks = Feedback.query.filter_by(rating=1).all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)


@app.route('/admin/feedback/bad_review')
def admin_feedback_bad_review():
    feedbacks = Feedback.query.filter(Feedback.rating <= 3,
                                      Feedback.comment.isnot(None),
                                      Feedback.comment != "").all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)


if __name__ == '__main__':
    app.run(debug=True)
