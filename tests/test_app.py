from tasks.models import Task


def test_landing_page_loads(client):
    assert client.get("/").status_code == 200


def test_empty_list_shows_message(client):
    res = client.get("/tasks/")
    assert res.status_code == 200
    assert b"No tasks found" in res.data


def test_create_task(client, app):
    res = client.post("/tasks/create", data={
        "title": "Write tests", "description": "pytest", "priority": "High",
    })
    assert res.status_code == 302
    with app.app_context():
        task = Task.query.one()
        assert task.title == "Write tests"
        assert task.priority == "High"
        assert task.user_id == 1


def test_blank_title_is_rejected(client, app):
    client.post("/tasks/create", data={"title": "", "priority": "Low"})
    with app.app_context():
        assert Task.query.count() == 0


def test_list_is_newest_first(client):
    client.post("/tasks/create", data={"title": "First", "priority": "Low"})
    client.post("/tasks/create", data={"title": "Second", "priority": "Low"})
    body = client.get("/tasks/").data
    assert body.index(b"Second") < body.index(b"First")


def test_default_priority_is_medium(client, app):
    client.post("/tasks/create", data={"title": "No priority"})
    with app.app_context():
        assert Task.query.one().priority == "Medium"
