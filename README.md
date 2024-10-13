#You can test the following endpoints using Postman or curl:

### User Management:
POST /api/users/ to create a new user (Admin only).
GET /api/users/ to list all users (Admin only).

### Books Management:
POST /api/books/ to create a new book (Admin only).
GET /api/books/ to list all books or filter by availability.
PUT /api/books/{id}/ to update a book (Admin only).
DELETE /api/books/{id}/ to delete a book (Admin only).

### Transaction Management:
POST /api/transactions/{id}/checkout/ to check out a book.
POST /api/transactions/{id}/return/ to return a book.
GET /api/transactions/ to list all transactions for the authenticated user.

### Search by Title:
GET /api/books/?search=The Great Gatsby