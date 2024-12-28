Quiz App Summary
This quiz application is built using Flask, SQLAlchemy, and JWT Authentication. It is designed to allow both users and admins to interact with the platform in different ways. The application offers various features such as user registration, login, quiz management, and user history tracking.

Key Features
1. User Authentication & Authorization
User Registration (/register): Allows new users to sign up by providing necessary credentials.
User Login (/login): Allows users to log in using their credentials. JWT tokens are used to authenticate the user.
Token Refresh (/refresh): A route to refresh JWT tokens for logged-in users.
2. Admin Routes for Quiz Management
Create Question (/admin/create_question): Admins can create new quiz questions.
Edit Question (/admin/edit_question/<int:question_id>): Admins can edit existing quiz questions by their ID.
Delete Question (/admin/delete_question/<int:question_id>): Admins can delete quiz questions by their ID.
Permanent Delete Question (/admin/delete_question/<int:question_id>): Admins can permanently delete a question.
Get Questions by Category (/admin/get_questions/<string:category>): Admins can view all questions in a specific category.
Get Question by ID (/admin/get_question/<int:question_id>): Admins can view a specific question by its ID.
Admin Results (/admin/results): Admins can view the results of all users.
3. User Routes for Quiz Interaction
Get Questions by Category (/questions/<string:category>): Users can fetch quiz questions from a specific category.
Get Categories (/categories): Users can fetch all available quiz categories.
Submit Answers (/submit_answers): Users can submit answers for a quiz they have taken.
Leaderboard (/leaderboard): Displays the leaderboard showing the top-performing users.
Quiz History (/user/history): Users can view their past quiz results and history.
4. Result Management
User Results (/user/results/<string:user_name>): Users can fetch their individual quiz results based on their username.
Technology Stack
Flask: The backend web framework used to handle HTTP requests and serve the API endpoints.
SQLAlchemy: ORM (Object Relational Mapping) used to manage database operations for storing users, questions, and results.
JWT Authentication: Secure token-based authentication to ensure that only authorized users (and admins) can access certain routes.
Security
JWT Tokens: Used for secure authentication. The tokens are issued upon successful login and must be included in the headers of requests to access protected resources (e.g., admin routes, submitting answers, etc.).
Admin & User Interaction
Admins can create, edit, and delete quiz questions, and can view quiz results for all users.
Users can take quizzes, submit answers, view their results, and see their history of attempted quizzes.
