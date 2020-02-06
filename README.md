# mb_api

#### Steps to Run the project.

#### Dependencies
 - docker
 - docker-compose


Project is deployed with passenger/nginx, to handle requests and responses and mysql for database.

- Clone the project from github
```
git clone https://github.com/deb999983/mb_api.git
```

- CD into the mb_api directory of the project
```
cd mb_api
```

- Start the services.
```
sudo ./scripts/start-services.sh
```

**Note** : Please wait for mysql to be ready, don't terminate the process. There will be some error messages but ultimately mysql will be ready to accept connections and then migrations for the project are run.


#### Demo
The project is hosted at http://ec2-13-232-196-189.ap-south-1.compute.amazonaws.com/docs/


#### APIs

#### Screen list
```
URL: http://ec2-13-232-196-189.ap-south-1.compute.amazonaws.com/screens/
RESPONSE: [
...
 {
  "name": "inox",
  "seatInfo": {
     "A": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "B": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "C": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "D": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
   }
},
 {
  "name": "inox1",
  "seatInfo": {
     "A": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "B": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "C": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "D": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
   }
}
...
]
```


#### Create a new screen
```
URL: http://ec2-13-232-196-189.ap-south-1.compute.amazonaws.com/screens/
DATA: {
  "name": "inox",
  "seatInfo": {
     "A": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "B": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "C": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "D": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
   }
}
RESPONSE: {
  "name": "inox",
  "seatInfo": {
     "A": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "B": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "C": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "D": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
   }
}
```

#### Screen Details
```
URL: http://ec2-13-232-196-189.ap-south-1.compute.amazonaws.com/screens/{screen_name}/
RESPONSE: {
  "name": "inox",
  "seatInfo": {
     "A": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "B": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "C": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
     "D": {"numberOfSeats": 12, "aisleSeats": [5,6,10,11]},
   }
}
```

#### Reserve seats of a screen
```
URL: http://ec2-13-232-196-189.ap-south-1.compute.amazonaws.com/screens/{screen_name}/reserve/
DATA: {
  "seats": {
     "A": [5,6,10,11],
     "B": [1,2,8,9]
   }
}
```


#### Cancel seats of a screen
```
URL: http://ec2-13-232-196-189.ap-south-1.compute.amazonaws.com/screens/{screen_name}/cancel/
DATA: {
  "seats": {
     "A": [5,6,10,11],
     "B": [1,2,8,9]
   }
}
```

#### Get reserved and unrerved seats of a screen
```
URL: http://ec2-13-232-196-189.ap-south-1.compute.amazonaws.com/screens/{screen_name}/seats/?status=reserved
DATA: {
  "seats": {
     "A": [5,6,10,11],
     "B": [1,2,8,9]
   }
}
```




