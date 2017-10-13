f = open('decrypted_passwords.txt', 'rb')

usernames = open('usernames.txt', 'w')
passwords = open('passwords.txt', 'w')


lst = []
for line in f:
	stuff = line.split('\t')
	indexofnull = stuff.index('00')
	user = list(filter(lambda x: x != '00', stuff[:indexofnull]))
	password = stuff[-4:]
	password = list(map(lambda x: x.replace('\n', ''), password))
	user = list(map(lambda x: x.decode('hex'), user))
	
	userstring = ''.join(user) 
	usernames.write(userstring + '\n')
	passstring = ''.join(password)	
	passwords.write(passstring + '\n')








	
