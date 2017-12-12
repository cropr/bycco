import plivo
import time

auth_id = "MANJK1ZGNHYMMXMMNIZW"
auth_token = "YWFmM2VmOWNkNTBmNTg1MGU1OGFhODgwNDEyYTdh"
sender = "32495706782"

ps = None

def setup():
    global ps
    ps = plivo.RestAPI(auth_id, auth_token)
    print("ps", ps)


def sendsms(message, receiver):
    """
    sends an sms to Plivo
    :param message: 
    :param receiver: 
    :return: 
    """
    t = time.time()
    response = ps.send_message({
        'src': sender,
        'dst': receiver,
        'text': message,
    })
    if response[0] != 202:
        print("Error response:", response)

if __name__ == "__main__":
    setup()
    sendsms("I have a cunning plan that cannot fail", "32477571313")

