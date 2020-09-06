# import os, os.path, json
# from datetime import datetime, timedelta
# from time import time
# from starlette.testclient import TestClient

# from .. import app

# client = TestClient(app)

# def setup_module(module):
#     """ 
#     setup any state specific to the execution of the given module.
#     """
#     pass

# def teardown_module(module):
#     """ 
#     teardown any state that was previously setup with a setup_module
#     method.
#     """
#     pass

# def test_api_get_consent():
#     """
#     """
#     response = client.get("/consent?usermail=robin.stroobants.ext@delijn.be")
#     assert response.status_code == 200

# def test_api_update_optin():
#     """
#     """
#     response = client.put("/optin/495005")
#     assert response.status_code == 200

# def test_api_update_optout():
#     """
#     """
#     response = client.put("/optout/495005")
#     assert response.status_code == 200

# def test_api_create_optin():
#     """
#     """
#     response = client.post("/optin", json={
#         'usermail': 'ruben.decrop.ext@delijn.be',
#         'channel': 'test',
#     })
#     assert response.status_code == 200
