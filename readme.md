# Description
![](./image/ws_submit.png)
This is a web application for pretrained ML model. <br>
User can submit csv file and receive a next month default prediction. <br>
There is also a possibility to upload csv file on the server for further utilization in data flow process. <br>
This web application is made using Flask framework. <br>
The model for default prediction is random forest. Model training steps are in the ipynb file.

# Source
https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset

# Instructions
Run `docker-compose up` command.

To submit file manually go to <br>
[http://localhost:5000/submit](http://localhost:5000/submit)

To get a prediction for the only one observation insert comma separated data after slash. <br>
For example `http://localhost:5000/submit/16,50000,2,3,3,23,1,2,0,0,0,0,50614,29173,28116,28771,29531,30211,0,1500,1100,1200,1300,1100`

To upload file use <br>
`curl --location 'localhost:5000/upload' --form 'file=@"./data.csv"'` <br>
or go to [http://localhost:5000/upload](http://localhost:5000/upload)
