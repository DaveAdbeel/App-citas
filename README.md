
# Python Flask Contacts CRUD

![image](https://repository-images.githubusercontent.com/651922840/de804023-b418-49ca-bfbc-1300c61abdc4)


## Prerequisites

Make sure you have the following installed on your system:

- Python (version 3.6 or higher)

## Installation

1. Clone this repository to your local machine:

   ```shellw
   git clone https://github.com/DaveAdbeel/App-citas.git
   ```

2. Change into the project directory

   ```shell
   cd App-citas
   ```

3. Initialize the virtual enviroment and install the required dependencies:

- First of all install the virtualenv tool if you don't already have it. You can install the following command in your terminal:

   ```
   pip install virtualenv
   ```

- Create the virtual environment by running the following command:

   ```
   python3 -m venv venv
   ```

  .This will create a new directory called "venv" which will contain all the files needed for your virtual environment.

- Activate the virtual environment. On Windows, run:

   ```
   venv\Scripts\activate
   ```

- On macOS or Linux, run:

   ```
   source venv/bin/activate
   ```

   .When the virtual environment is enabled, you will see the directory name in parentheses in your terminal, 
   indicating that you are working within the virtual environment, after that run this command.
   
   ```shell
   pip install -r requirements.txt
   ```

## Database Setup

1. Create a MySQL database for the project with [this sql script](https://pastebin.com/2rhJ1jW5).

2. Update the variables `MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE` in the `.env` file with your MySQL database connection details.

3. Also update the `SECRET_KEY` variable which is also in the `env` file, for security reasons


## Usage

1. Start the Flask development server:

   ```shell
   python3 app.py
   ```

   The server should now be running at `http://localhost:5000`.

2. Open your web browser and navigate to `http://localhost:5000`.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an 
issue or submit a pull request. Make sure to follow the existing code style and conventions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions, feel free to reach out to the project author:

- Name: [Dave Adbeel](https://github.com/DaveAdbeel)
- Email: [davidadbeelgonzalez@gmail.com](mailto:davidadbeelgonzalez@gmail.com)

