## Back End

The "Proxy" part, responsible for the communication between web interface and the features provider, abstracting auth, user information and requests handling from the features provider.

Back end consists of two main parts:
* Request dispatcher (the part responsible for, well, transforming and passing requests from a user to the features provider, as well as serving as a result reception point for responses from the features provider. 
* Utility database, to store needed user information which is not directly related to the work experience, such as tokens, correspondence between auth tokens and user ids, probably some preferences etc.

Q: What is the specific architecture for the back end?
A: The inner workings are not defined yet, this is one of the tasks. However, it might be useful to design an API for interaction with both Web Interface and Features Provider.

Q: What is the technology choice? 
A: Idk, honestly. Probably we will come up with something for the API documentation soon, but as for the service itself -- that's up to the team responsible for this part. Python + Flask?

Btw, don't forget to update .gitignore so we won't have to deal with .idea on master.
