# HW 19. Bootstrap, JQuery, JSON, AJAX

## Task

In any of the repositories, implement or change the ContactForm functionality that will send a letter to the mail (via celery) but will be available from any page of the site that uses one of the basic templates.<br/>
Add a modal window from bootstrap to the base template (project or application or application template group) in which you will load the form or success message.<br/>
Add or change the endpoint view so that it sends data in json format.<br/>
Add a script that will load the form in the modal window, submit the form from the window, and load back the result - a form with checked fields with errors or a success message.<br/>

(For example, the "Contact us" button in the header on every page)<br/>

## Realised

1. [Created logic of leave comment with jQuery and modal-form](https://github.com/goldaev51/blog_django/blob/main/blog/views.py#L118)
2. [Created logic of feedback with jQuery and modal-form](https://github.com/goldaev51/blog_django/blob/main/blog/views.py#L129)
3. [jQuery code](static/js/comments.js)


## Launch

* clone current repository
* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate
* Create superuser with 'python manage.py createsuperuser'
* Fill db with 'python manage.py fill_db'
* python manage.py runserver
* In new terminal tab run  celery -A core worker -l INFO
* Go to http://127.0.0.1:8000/blog/posts/
* Check logic of leaving feedback and create comment for the post
