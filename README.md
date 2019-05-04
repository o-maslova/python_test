# python_test
Simple web application

Dependencies: flask, redis, redis-server

Firstly, if it wasn't previosly installed, you need to install required packages for app deployment:
  - cd  _directory_in_which_you_clone_the_app
  - sudo pip install -r directory/requirements.txt

The app is implemented in two ways: with simple GUI (visual_app) and without it (simple_app).
For testing visual_app you need to run file visual_app/visual.py. Then open new terminal window and enter next commands:
  - to show main page response:
      curl -i http://127.0.0.1:5000
  - to add new list:
      curl -H "Content-type: application/json" http://127.0.0.1:5000/add_new_list -d '{"key": "value"}'
  - to show your lists:
      curl -H "Content-type: application/json" http://127.0.0.1:5000/show_lists

For testing simple_app you nedd to run simple_app/simple.py. Then open web browser and go to next pages:
  - to show main page:
      http://127.0.0.1:5000
  - to add new list:
      http://127.0.0.1:5000/add_new_list
  - to show your lists:
      http://127.0.0.1:5000/show_lists
