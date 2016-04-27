=================
Building projects
=================

Editing templates
-----------------

Tarbell projects consist of simple HTML pages that may use `Jinja2 <http://jinja.pocoo.org/docs/>`_ templating features.

If you create a file in your project directory called ``chapter1.html``, you'll be able to preview the file at http://localhost:5000/chapter1.html and publish to the same file. This file can be straight up HTML, or it can inherit from a Tarbell blueprint file. 

Files and directories that start with an underscore (``_``) or a dot (``.``), like the ``_blueprint`` directory containing the Tarbell blueprint files, will not be rendered by the preview server or included in the generated static HTML.

Understanding Tarbell Blueprints
--------------------------------

Blueprints are exactly what they sound like –– a basic structure for building projects upon. From the `Flask documentation <http://flask.pocoo.org/docs/blueprints/>`_:

  Flask uses a concept of blueprints for making application components and supporting common patterns. Blueprints can greatly simplify how large applications work, but a blueprint is not actually an application. Rather it is a blueprint of how to construct or extend an application.

Tarbell ships with a default blueprint called _blueprint. This folder contains boilerplate code like advertising, analytics, and common page elements. Tarbell projects should inherit from blueprints.


Here's a simple ``_blueprint/_base.html`` example.

.. code-block:: html+jinja

  <html>
    <head>
      <title>{{ title }}</title>
      {% block css %}
      <link rel="stylesheet" type="text/css" href="css/style.css" />
      {% endblock css %}
    </head>
    <body>
      {% block content %}{% endblock content %}
    </body>
  </html>

To inherit from this template, you use the "extend" syntax in ``index.html`` or other project files you create. All your ``index.html`` needs to contain is:

.. code-block:: html+jinja

  {% extends '_base.html' %}

  {% block content %}
  <h1>{{ title }} </h1>
  {{ content|markdown }}
  {% endblock content %}

You might notice we're using the ``|markdown`` filter. Blueprint templates also define filters, enabled by Jinja2. See building blueprint templates for more, and the `Jinja2 <http://jinja.pocoo.org/docs/>`_ docs for more on Jinja2.

If a blueprint defines a static file or template (e.g. ``_blueprint.css``), it will be available relative to the project's base path (e.g. http://127.0.0.1:5000/style.css). If a project defines a file with the same name, the project's version will be used instead.

See the basic Tarbell template for a simple implementation of a Blueprint.

Template inheritance: Override files from Tarbell Blueprints by copying to your project directory
-------------------------------------------------------------------------------------------------

Any file in a Tarbell Blueprint can be overridden in your project files.

For example, if your blueprint includes a file ``_blueprint/_nav.html``, you can create a file named ``_nav.html`` in your project directory and it will be published instead of the blueprint version.

This works for all files, static or templates.

Files prefixed with underscores (``_``) will not be generated or published
--------------------------------------------------------------------------

To suppress a file from publishing, use a filename like ``_filename.txt``.

Configuring projects
--------------------

Project configuration is kept in the `tarbell_config.py` file in your project's blueprint directory.
See :ref:`tarbell-config` for configuration documentation.

Creating JSON
-------------

You can publish the data coming from your Google spreadsheet as JSON if so desired. To do this, set the `CREATE_JSON`
flag in `tarbell_config.py` to `True`. When you visit `yoursite.com/data.json`, Tarbell will create some JSON
that will look something like this:

.. code-block:: json

  {
    name: "ethelpayne",
    title: "Ethel Payne: A life in journalism",
    headline: "Ethel Payne, Chicago journalist",
    quote: "I stick to my firm, unshakeable belief that the black press is an advocacy press, and that I, as a part of that press, can’t afford the luxury of being unbiased ... when it come to issues that really affect my people, and I plead guilty, because I think that I am an instrument of change.",
    data: [
      {
        name: "Ethel Payne",
        known_for: "civil rights journalism",
        born: "8/14/1911",
        died: 33386
      }
      {
        name: "Grace Hopper",
        known_for: "mathematics and computer programming",
        born: "12/9/1906",
        died: 33604
      },
    ]
  }

The first block of keys and values comes from the `values` workbook. The `data`
array represents another workbook. Any other workbooks you create within your spreadsheet will be represented
as separate arrays.

Optionally, you can use the `CONTEXT_SOURCE_FILE` setting in `tarbell_config.py` to determine your data source,
which can be a URL, local file, CSV or Excel file.

.. note::

  The ``data.json`` file is created on the fly and will not appear in your project root. You can view and access
  it locally at ``127.0.0.1:5000/data.json``. If JSON creation is enabled, it will override any local file named
  ``data.json``.


Using context variables
-----------------------

Template data can come from Google spreadsheets, a local or remote CSV or Excel file, or 
tarbell_config.py's ``DEFAULT_CONTEXT``. The context source is configured in ``tarbell_config.py`` 
(see :ref:`tarbell-config` for reference). 

This simple ``DEFAULT_CONTEXT`` shows many of the key template features:

.. code-block:: python

  DEFAULT_CONTEXT = {
      'name': 'nellie-bly',
      'title': 'The Story of Nellie Bly',
      'font_size': '20px',
      # Nested dictionary
      'photos': {
          'intro': {
              'url': 'img/bly01.jpg',
              'caption': 'A caption',
          }
      },
      # Nested list
      'timeline': [
          {'year': '1902', 'description': 'Description...'},
          {'year': '1907', 'description': 'Description...'},
          {'year': '1909', 'description': 'Description...'},
      ],
    }
  }

To print the title in your template, use `{{ title }}`:

.. code-block:: html+jinja

  <h1>{{ title }}</h1>

Address a nested dictionary:

.. code-block:: html+jinja

  <img src="{{ photos.intro.url }}" alt="{{ photos.intro.caption }}" />
  <aside>{{ photos.intro.caption }}</aside>

Access a list of data:

.. code-block:: html+jinja

  <ul>
    {% for year in timeline %}
    <li><strong>{{ year }}</strong>: {{ description }}</li>
    {% endfor %}
  </ul>

In addition to `DEFAULT_CONTEXT`, Tarbell sets the following variables:

 - `PROJECT_PATH`: the filesystem path to the directory containing your `tarbell_config.py` file
 - `ROOT_URL`: the hostname for your site, initially `127.0.0.1:5000` (this changes when publishing)
 - `SPREADSHEET_KEY`: the `SPREADSHEET_KEY` variable in your `tarbell_config.py` (or `None` if not set)
 - `BUCKETS`: the `S3_BUCKETS` variable in your `tarbell_config.py`
 - `SITE`: the current Tarbell site object

When you run `tarbell publish`, Tarbell again sets additional context variables, based on your S3 settings. For example, if your `production` bucket is named `apps.example.com` in a project named `my-story`, these variables would be added to your site context when you run `tarbell publish production` (or `tarbell publish`):

 - `ROOT_URL`: the host and path you're publishing to (for example, `apps.example.com/my-story`)
 - `S3_BUCKET`: the name of the bucket you're publishing to (`apps.example.com`)
 - `BUCKET_NAME`: the name of the publishing target, `production` or `staging` (this is the first argument after `tarbell publish`)


Where can context variables be used?
------------------------------------

By default, context variables only work in HTML files. If rendering the file causes a Jinja
template error (which can happen if the file has Jinja-like markers), you'll see an error page with debugging information.

It is possible (and common) to use template variables inside `script` and `style` tags on HTML pages. For example:

.. code-block:: html

  <style type="text/css">
  #content { font-size: {{ font_size }}; }
  </style>

Similarly, a script tag could be included like so:

.. code-block:: html
  
  <script type="text/javascript">
  var data = {{ photos|tojson|safe }}
  console.log(photos.intro.url);
  </script>

Use this feature with care! Missing variables could easily break your CSS or Javascript.

Adding custom template types
----------------------------

By default, Tarbell will treat any file with a mimetype other than `text/html` as a static file as serve it as-is. This is by design, for both speed (all your Javascript files don't need to run through Jinja templating) and safety (it's easy to break your Javascript with a misplaced tag). But you may decide you need more than HTML rendered.

In that case, add the `TEMPLATE_TYPES` variable to your `tarbell_config.py` file with a list of additional mimetypes to render. For example:


.. code-block:: python

  # tarbell_config.py

  TEMPLATE_TYPES = ['text/plain', 'application/xml', 'text/css']

This would add support for rendering plain text, XML and CSS files as templates. 


Anatomy of a project directory
------------------------------

When you run ``tarbell newproject`` with the default blueprint, a number of new files and
folders are created, many of them with special significance. Details may vary for other blueprints,
but they're likely to have many similar files and concepts.

Here's a rundown of what they all do.

**Files in the root directory:**

index.html
  The first page people will see when they visit your project. This is typically where most of
  the content lives, and is probably where you want to start editing.

tarbell_config.py
  The settings and context for this specific project, described in more detail in the
  `Configuring projects section above <#configuring-projects>`_.


**Files in the _blueprint directory:**

Keep in mind that you rarely want to edit the blueprint files in the ``_blueprint/`` directory - if you want
to change something, copy the file to the root directory and make the change there. If a file of the
same name exists in both the root directory and the ``_blueprint/`` directory, Tarbell will rely on the
one in the root directory.

The only time you should edit the files in the ``_blueprint/`` directory is when 
`you'd like to create or update the blueprint itself <base_templates.html>`_.

_base.html
  The base page template, containing ``<head>`` and ``<body>`` tags, and pointing to many of the Javascript
  and CSS files that will be loaded for each page in the project.

_footer.html
  The partial template containing anything you'd like to appear consistently in the footer at the
  bottom of each page.

_nav.html
  The partial template containing the nav bar that runs along the top of the page.

_spreadsheet.xlsx
  This is the template file that `Google spreadsheets will be based upon
  <google_spreadsheets.html>`_. Unlike most other files in ``_blueprint``, overriding it in your root
  directory won't do anything. However, if you want future projects to be created with a different
  spreadsheet template, you can edit this file and commit it to a repository you control; learn more
  about this feature in the `Developing blueprints <base_templates.html>`_ section.

base.css
  The base CSS file imported by the blueprint for this project. Override this file in your root
  directory if you'd like to make CSS changes.

blueprint.py
  A Python file that contains a default set of template filters for use in this project. Override
  this file in your root directory if you'd like to alter the behavior of these filters, or add your
  own. If you'd like to make your changes available to other projects, check out the `Developing
  blueprints <base_templates.html>`_ section.

favicon.ico
  Favicons are `small logos for websites <http://en.wikipedia.org/wiki/Favicon>`_ that typically
  appear next to a website's name in a browser tab. Change this file in order to change the logo
  associated with your site in users' browser tabs, though keep in mind that favicons have
  `a number of rules <http://www.w3.org/2005/10/howto-favicon>`_ about how they should be
  constructed.

favicon-preview.ico
  This is the icon for the in-development version of a site that appears next to the website's name
  in a browser tab, following the same rules as for favicon.ico above. The key difference is that
  this icon is meant to remind developers and testers that they're not looking at a live site.

index.html
  This is a fallback version of the project's front page, in case the ``index.html`` file in the root
  directory is removed or renamed. It begins life as an exact copy of the root directory's 
  ``index.html``.

Adding custom routes
--------------------

Sometimes, you'll find that you need create pages programatically, instead of simply adding template files. Or you may need to output data in a format other than HTML (like JSON, for example).

For example, here's a hook from a project's `tarbell_config.py` that publishes special social media stub
pages for each row in a worksheet. This allows individual items to be shared from a single-page 
listicle app:

.. code-block:: python

  from itertools import ifilter
  from flask import Blueprint, render_template
  from tarbell.hooks import register_hook

  # create a blueprint for this project
  # tarbell will consume this when the project loads
  blueprint = Blueprint('myproject', __name__)

  @blueprint.route('/rows/<id>.html')
  def social_stub(id):
      "Build a social stub for in-page permalinks"
      site = g.current_site

      # get our production bucket for URL building
      bucket = site.project.S3_BUCKETS.get('production', '')
      data = site.get_context()
      rows = data.get('list_items', [])

      # get the row we want, defaulting to an empty dictionary
      row = next(ifilter(lambda r: r['id'] == id, rows), {})

      # render a template, using the same template environment as everywhere else
      return render_template('_fb_template.html', bucket=bucket, **row)

Here's the `_fb_template` referenced above:

.. code-block:: html+jinja
  
  <html>

  <head>
    <script>
      document.location = "http://{{ bucket }}/#{{ row.id }}";
    </script>

    <meta property="og:url" content="http://{{ bucket }}/rows/{{ row.id }}.html" />
    <meta property="og:title" content="Great moments in history: {{ row.heading }}" />
    <meta property="og:description" content="{{ row.og }}" />
    <meta property="og:image" content="http://{{ bucket }}/img/{{ row.img }}" />
  </head>

  <body></body>

  </html>


Since this is a custom route, we need to tell Tarbell to build it as an HTML file when we call `tarbell generate` or `tarbell publish`. There are two ways to do this: `url_for` tags, or URL generators.

.. note::
    
  Under the hood, Tarbell uses `Frozen-Flask <http://pythonhosted.org/Frozen-Flask/>`_ to generate static pages, so you can consult that project's documentation for more details and further customization.

Auto-linking:

In your main `index.html` template, generate a link for each stub:

.. code-block:: html+jinja

  {% for row in list_items %}
  <a href="{{ url_for('myproject.social_stub', id=id) }}">Stub</a>
  {% endfor %}

Frozen-Flask will automatically track every call to `url_for` and build out those URLs. If that doesn't make sense for your project, you can also write a generator function, and use a `Tarbell hook <hooks.html>`_ to register it at build-time.

.. code-block:: python

  # in tarbell_config.py

  def social_stub_urls():
      "Generate a URL for every social stub"
      site = g.current_site
      data = site.get_context()
      rows = data.get('list_items', [])

      for row in rows:
          yield ('myproject.social_stub', {'id': row['id']})

  @register_hook('generate')
  def register_social_stubs(site, output_root, extra_context):
      "This runs before tarbell builds the static site"
      site.freezer.register_generator(social_stub_urls)

Using Flask Extensions
----------------------

The Flask ecosystem includes all sorts of useful `extensions <http://flask.pocoo.org/extensions/>`_ for building web applications. 

Every Tarbell site includes a Flask app that handles request routing and template rendering. You can hook into this underlying app to take advantage of Flask extensions to speed up your development process.

1. Define a Tarbell Blueprint in your `tarbell_config.py` file. (Your variable name must be `blueprint` for Tarbell to find it.)
2. Use the `blueprint.record <http://flask.pocoo.org/docs/0.10/api/#flask.Blueprint.record>`_ decorator to tell Flask to run a function when the blueprint is loaded onto an app. This will happen at the end of your Tarbell site's `__init__` method. The function will be passed a `state` object, with a reference to your Flask app at `state.app`.
3. Create an instance of the extension you're using. Inside the function you decorated with `blueprint.record`, run the extension's `init_app` method with your site's Flask app. (You can also initialize the extension with the app in one step, if you don't need a reference to the extension outside that function.)
4. Add any configuration settings the extension needs to `state.app.config`.

Here's how to use `flask-thumbnails <https://github.com/silentsokolov/flask-thumbnails>`_ with Tarbell:

.. code-block:: python

  # tarbell_config.py

  from flask import Blueprint
  from flask.ext.thumbnails import Thumbnail

  # initialize a blueprint and thumbnails extension
  blueprint = Blueprint('project', __name__)
  thumbnails = Thumbnail()

  # media settings, note that these are relative paths
  MEDIA_FOLDER = "img/uploads"
  MEDIA_THUMBNAIL_FOLDER = "img/thumbnails"

  # this function will run when Tarbell's underlying Flask app
  # adds this blueprint
  @blueprint.record
  def app_setup(state):
      "Configure thumbnails"

      # configure thumbnails with the active app
      state.app.config['MEDIA_FOLDER'] = MEDIA_FOLDER
      state.app.config['MEDIA_THUMBNAIL_URL'] = MEDIA_FOLDER
      thumbnails.init_app(state.app)

Now, in your templates, you can use the `thumbnail` filter:

.. code-block:: html+jinja

  <img src="{{ 'image.jpg'|thumbnail('200x200') }}" alt="A cropped image">
  <img src="{{ 'image.jpg'|thumbnail('200x200', crop='fit', quality=100) }}" alt="A cropped image">





