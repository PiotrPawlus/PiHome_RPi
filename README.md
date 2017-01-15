GET device - curl http://127.0.0.1:5000/api/v1/device/1      -- get information about device
POST device - curl -X POST http://127.0.0.1:5000/api/v1/device   -- create new device
PUT device - curl -X PUT http://127.0.0.1:5000/api/v1/device/1   -- update device
DELETE device - curl -X DELETE http://127.0.0.1:5000/api/v1/device/1  -- delete device
GET devices - curl http://127.0.0.1:5000/api/v1/devices - get list of devices
GET device status - curl http://127.0.0.1:5000/api/v1/device/status/1 - get current device status

POST session - curl -X POST http://127.0.0.1:5000/api/v1/session - login user
DELETE session - curl -X DELETE http://127.0.0.1:5000/api/v1/session - logout user



POST - create user:
curl -H "Content-Type: application/json" -X POST -d '{"username":"a","password":"xyz", "first_name":"f", "last_name":"l"}' http://localhost:5000/api/v1/registration

POST - login:
curl -H "Content-Type: application/json" -X POST -d '{"username":"a","password":"xyz"}' http://localhost:5000/api/v1/authentication

POST - token:
curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4NDU4NjI2OCwiaWF0IjoxNDg0NTg1NjY4fQ.eyJpZCI6MX0.bq_R3A3LoTxsKHn5HG34MBxS7p8Bph_AF09VRVjVtNA:none -i -X GET http://127.0.0.1:5000/api/v1/token
