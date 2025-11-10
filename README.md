# Blogging-Platform
You are required to build a personal blog where you can write and publish articles. The blog will have two sections: a guest section and an admin section.
## Features
**Guest Section** — A list of pages that can be accessed by anyone:

- Home Page: This page will display the list of articles published on the blog.

- Article Page: This page will display the content of the article along with the date of publication.

**Admin Section** — are the pages that only you can access to publish, edit, or delete articles.

- Basic Authentication: The admin panel is protected by a simple username and password.

- Dashboard: This page will display the list of articles published on the blog along with the option to add a new article, edit an existing article, or delete an article.

- Add Article Page: This page will contain a form to add a new article. The form will have fields like title, content, and date of publication.

- Edit Article Page: This page will contain a form to edit an existing article. The form will have fields like title, content, and date of publication.

## Technologies Used
- Backend: Python, Flask
- Frontend: HTML, Jinja2 Templating
- Data Storage: PostgreSQL, Psycopg2

## Usage
### Guest
- Navigate to `http://127.0.0.1:5000/` to view all post
- Guest can view the post by clicking the title.

### Admin
- Navigate to `http://127.0.0.1:5000/admin` to access admin page
- Enter the Username and Password
- Admin can:
  - Edit a post
  - Add a new post
  - Delete a post
