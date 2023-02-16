from fastapi.testclient import TestClient
from app.main import app
from app.models.models import Authority
from app.models.models import TaskTag
from app.models.models import Slot 
from app.models.models import User
from app.cruds.user import user_register,user_get
from conftest import test_client
import pytest

def test_add_task(test_client):
    task={
        "name":"testTask",
        "detail":"This is the task json for testing (これはテスト用のTaskオブジェクトです)",
        "authority":[],
        "tag":[]
    }
    response=test_client.post("/tasks/",json=task)
    assert response.status_code == 200

def test_add_slot(test_client):
    task=test_client.get("/tasks/?name=testTask").json()
    slot={
        "name":"testslot",
        "start_time":{ "year":2022,"month":12,"day":30,"hour":22,"minute":0,},
        "end_time":{ "year":2022,"month":12,"day":31,"hour":8,"minute":0},
        "task":task.get("id")
    }
    
    slot=test_client.post("/slots/",json=slot)
    assert slot.status_code == 200
    assert slot.json().get("name")=="testslot"
    assert slot.json().get("start_time")=={ "year":2022,"month":12,"day":30,"hour":22,"minute":0,}
    assert slot.json().get("end_time")=={ "year":2022,"month":12,"day":31,"hour":8,"minute":0}

def test_open_bid(test_client):
    slot=test_client.get("/slots/?name=testslot").json()
    bid={
        "name":"testBid",
        "open_time":{"year":2022,"month":12,"day":30,"hour":23,"minute":0},
        "close_time":{"year":2022,"month":12,"day":31,"hour":23,"minute":0},
        "slot":slot.get("id"),
        "start_point":10,
        "buyout_point":3
    }
    response=test_client.post("/bid/",json=bid)
    assert response.status_code == 200
    assert response.json().get("name")=="testBid"
    assert response.json().get("open_time")=={"year":2022,"month":12,"day":30,"hour":23,"minute":0}
    assert response.json().get("close_time")=={"year":2022,"month":12,"day":31,"hour":23,"minute":0}
    assert response.json().get("buyout_point")==3
def test_patch_task(test_client):
    task=test_client.get("/tasks/?name=testTask").json()
    update_data={
        "max_woker_num":3,
        "min_woker_num":1,
        "exp_woker_num":1,
    }
    response=test_client.patch("/tasks/"+task.get("id"),json=update_data)
    assert response.status_code == 200
    assert response.json().get("max_worker_num")==3
    assert response.json().get("min_worker_num")==1
    assert response.json().get("exp_worker_num")==1
def test_place_bid(test_client):
    task=test_client.get("/tasks/?name=testTask").json()
    add_task={
        "exp_task":[task.get("id")]
    }
    responsess=test_client.patch("/users/task",json=add_task,headers={"Authorization":f'Bearer {test_client.access_token_2}'})
    assert responsess.status_code == 200
    assert responsess.json().get("exp_task")==[task]
    bid=test_client.get("/bid/?name=testBid").json()
    tender_point={"tender_point":7}
    response=test_client.post("/bid/"+bid.get("id")+"/tender",json=tender_point)
    assert response.status_code == 200
    assert response.json().get("user_id")==test_client.user.get("id")
    response = test_client.get("/bidder/?bid_id="+bid.get("id")).json()
    assert response[0].get("point")==3
    response=test_client.post("/bid/"+bid.get("id")+"/tender",
                              headers={"Authorization":f'Bearer {test_client.access_token_2}'},
                              json=tender_point)
    assert response.status_code == 200
    assert response.json().get("user_id")==test_client.user2.get("id")
    response =test_client.get("/bidder/?bid_id="+bid.get("id")).json()
    assert response[0].get("point")==7
    response=test_client.post("/bid/"+bid.get("id")+"/close")
    assert response.status_code == 200
    assert response.json().get("assignees")==[test_client.user,test_client.user2]
    end=test_client.post("/slot/"+response.json().get("id")+"/complete")
    assert end.status_code == 200
    assert end.json().get("point")==3
    assert end.json().get("exp_task")==[task]

{ "name":"testuser","password":"testpassword","block":"B3","room_number":"B310"}