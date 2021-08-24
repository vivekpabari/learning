import requests




#get method
d = {'user':'vivek','password':'123@abc'}
req = requests.get('https://httpbin.org/get',params=d)
print(req.url)
print(req.text)


#post method
req = requests.post('https://httpbin.org/post',data=d)
print(req.url)
print(req.text)



#