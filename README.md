# Motion Activated Weather Station

Using opencv and motion detection, retrieve the latest hourly weather conditions

How to run socket:
gunicorn -k flask_sockets.worker service:app