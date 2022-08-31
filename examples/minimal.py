from pydispatch import dispatcher

metaKey = "moo"
MyNode = object()
event = {"sample": "event"}


def callback(event=None):
    """Handle signal being sent"""
    print("Signal received", event)


dispatcher.connect(callback, sender=MyNode, signal=metaKey)
dispatcher.send(metaKey, MyNode, event=event)
