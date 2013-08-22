DevDetails.com
==============

Install
-------

    npm install .
    pip install -r requirements.txt

Development
-----------

- Add content in the content directory.
- Change styles with theme/static/css/style.less
- Change templates in theme/templates
- Run dev server: `make devserver`
- Stop dev server: `make stopserver`

Build
-----

    make html

Deploy on Github Pages
----------------------

*Note*: This destroys the master branch and overwrites it with the content from output:

    make github