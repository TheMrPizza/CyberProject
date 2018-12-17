import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate(r'C:\Users\Guy\Downloads\cyberproject-ec385-firebase-adminsdk-sxzt7-5b7e34d38f.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cyberproject-ec385.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference()
new_user = ref.child('users').child('q2mzuvxdpNFW8YEZ4hEv').push({
    'username': 'guy1guy1'
})
