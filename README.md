# Shotstack Pexels Demo

This project demonstrates how to use the Shotstack cloud video editing API to create 
a video using an HTML form and video sourced from the Pexels video library.

An HTML web form allows the user to search the Pexels library via the Pexels API, choose 
a soundtrack and add a title. A video is the created by the Shotstack API using the video
clips returned by the Pexels search and the track and title entered by the user.

View the live demo at: https://shotstack.io/demo/pexels/

The demo is built using Python and can be used with Flask Framework.

### Requirements

- Python 3+
- Pexels API key: https://www.pexels.com/api
- Shotstack API key: https://dashboard.shotstack.io/register

### Project Structure

The project is divided in to a two components:

#### Backend API

The backend API with an endpoint which searches the Pexels API, prepares the edit and posts 
the data to the Shotstack API. A status endpoint is also available which can be polled to 
return the status of the video as it renders.

The backend API source code is in the _api_ directory.

#### Frontend Web Form & Player

The frontend is a simple HTML form that allows the user to enter a search term and basic 
options to create a video. The form uses jQuery to submit the data to the backend API and 
poll the status of the current render. There is also a video player that is loaded with 
the final rendered video when ready.

The front end API source code is in the _web_ directory.

### Installation

Install python module dependencies:

```bash
cd api
pip3 install -r requirements.txt
```

### Configuration

Copy the .env.dist file and rename it .env. Replace the environment variables below with your
Pexels and Shotstack API key (staging key):

```bash
PEXELS_API_KEY=replace_with_your_pexels_key
SHOTSTACK_API_KEY=replace_with_your_shotstack_key
```

### Run Locally

To start the API and serve the front end form (from the _api_ directory):

```bash
cd api
flask run
```

Then visit [http://127.0.0.1:5000](http://127.0.0.1:5000)
