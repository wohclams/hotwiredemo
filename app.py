import time
import datetime

from flask import Flask, render_template, request, redirect, url_for, Response

from turbo import Turbo

app = Flask(__name__)

turbo = Turbo(app)

comments = [{"id":1,"text":"Hello, great site!"},{"id":2,"text":"Super cool demo!"},{"id":3,"text":"Bitcoin!"}]


@app.route('/')
def homepage():
	current_time = int(time.time())

	return render_template('homepage.html', current_time=current_time)

@app.route('/about/')
def about():
	return render_template('about.html')

@app.route('/slow/')
def slow():
	time.sleep(5)
	current_time = int(time.time())
	return render_template('slow.html', current_time=current_time)

@app.route('/extra-data/')
def extra_data():
	return render_template('extra.html')

@app.route('/comments/', methods=['GET', 'POST'])
def get_comments():
	if request.method == 'POST':
		next_id = comments[-1].get('id') + 1
		text = request.form.get('text')
		comment = {"id":next_id,"text":text}
		comments.append(comment)
		return redirect(url_for('get_comments'),code=303)

		# if turbo.can_stream():
		# 	return turbo.stream(turbo.append(render_template('_comment.html', comment=comment), target='comment-list'),)
	else:
		return render_template('view_comments.html', comments=comments)

@app.route('/comments/<comment_id>/edit/', methods=['GET', 'PUT'])
def edit_comment(comment_id):
	comment = next((item for item in comments if item['id'] == int(comment_id)), None)
	if request.method == 'PUT':
		comment['text'] = request.form.get('text')
		#return render_template('view_comments.html', comments=comments)
		#return redirect(url_for('get_comments'),code=303)
		if turbo.can_stream():
			return turbo.stream(turbo.update(render_template('_comment.html', comment=comment), target='comment-num-'+str(comment['id'])),)
	else:
		return render_template('edit_comment.html', comment=comment)

