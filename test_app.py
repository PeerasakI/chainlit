import chainlit as cl

@cl.on_message
def main(msg:str):
    resp = msg.title()
    

    cl.Message(content = f"here is a message{resp}")