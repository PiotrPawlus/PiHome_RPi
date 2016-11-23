GET device - curl http://127.0.0.1:5000/api/v1/device/1      -- get information about device
POST device - curl -X POST http://127.0.0.1:5000/api/v1/device   -- create new device
PUT device - curl -X PUT http://127.0.0.1:5000/api/v1/device/1   -- update device
DELETE device - curl -X DELETE http://127.0.0.1:5000/api/v1/device/1  -- delete device
GET devices - curl http://127.0.0.1:5000/api/v1/devices - get list of devices
GET device status - curl http://127.0.0.1:5000/api/v1/device/status/1 - get current device status

POST session - curl -X POST http://127.0.0.1:5000/api/v1/session - login user
DELETE session - curl -X DELETE http://127.0.0.1:5000/api/v1/session - logout user
