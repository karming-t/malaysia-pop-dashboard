# 🇲🇾 Malaysia Population Dashboard

A simple web dashboard built with Flask and Dash to visualize Malaysia's population data from the [data.gov.my](https://api.data.gov.my/data-catalogue?id=population_malaysia) API.

![Dashboard Demo](https://imgur.com/a/pop-dashboard-image-rKBdACc)

## 🚀 Getting Started: Set Up and Run the App

Follow these steps to run the app locally on your machine.

---

### 1. Navigate to Project Directory

Download the project and open your powershell terminal and change to the directory where the folder is located.

eg. cd path/to/your/project-directory

### 2. Create a Virtual Environment

Create a Python virtual environment to keep dependencies isolated.

e.g. python -m venv my-pop-env

### 3. Activate The Virtual Environment

With the command below, activate the virtual environment. You should see (my-pop-env) in your terminal prompt after activation.

e.g. my-pop-env\Scripts\activate

### 4. Install Required Packages

Install Flask, Dash and Pandas with the command below and use pip list to check the list of installed packages after.

e.g. pip install flask dash pandas
e.g. pip list

### 5. Run the Application

Once everything is installed, run your app using the command below. The app wil be available at [http://localhost:5000/dashboard/](http://localhost:5000/dashboard/).
To view the population created with Flask which was an optional task in the assignment, switch the endpoint to "/population" or [http://localhost:5000/population](http://localhost:5000/population).

e.g. python app.py

### 6. Deactivate the Virtual Environment

After you're done using the app, you can deactivate the virtual environment with the command below

e.g. deactivate

