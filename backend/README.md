# Smart Brain Backend
This is the backend server for the Smart Brain application, which is built using the MERN (MongoDB, Express.js, React.js, Node.js) stack. The purpose of this backend server is to handle the API requests from the frontend, communicate with the MongoDB database, and provide the necessary functionality for smart brain.

# Installation
To set up the backend server locally, follow these steps:

1. Clone the repository: 
    ``` shell
    git clone https://github.com/Harshdev625/Smart-Brain-Backend
    ```

2. Install the required dependencies by running npm install.
   ```shell
   npm install
   ```
3. Create a MongoDB Atlas account and set up a cluster.
4. Create a .env file in the root folder and add the following environment variables:
    ``` shell
    MONGODB_URI: The connection string for your MongoDB cluster.
    ```
5. Run the server using 
    ``` shell
    nodemon index.js
    ```
6. The backend server is now running on http://localhost:3001.

# API Endpoints
The backend server provides the following API endpoints for the Smart Brain application:
- POST /signin: Sign in a user with their email and password.
- POST /register: Register a new user with their name, email, and password.
- GET /profile/:id: Get the profile information of a user with the specified user ID.
- PUT /image: Incrementing the user's image count.

The backend server uses MongoDB as the database to store user information and image counts. The MongoDB Atlas cluster is utilized to ensure seamless scalability and data persistence.

# Contributing
Contributions to the Smart Brain Backend are welcome! If you encounter any bugs, issues, or have ideas for improvements, please open an issue on the repository. Pull requests with enhancements are also appreciated.


# Tech Stack Used
 - Node.js
 - Express.js
 - MongoDB

Please note that the frontend repository (Smart-Brain) needs to be set up and connected to this backend server for the complete functionality of the application.