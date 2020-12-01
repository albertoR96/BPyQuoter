from http.server import HTTPServer, BaseHTTPRequestHandler
from Article import *
from Address import *
from Customer import *
from Supplier import *
import re
import json

articlesFileName = '_data/articles.json'
customersFileName = '_data/customers.json'
suppliersFileName = '_data/suppliers.json'
purchasesFileName = '_data/purchases.json'
salesFileName = '_data/sales.json'

class RequestParameter:
    name = ''
    value = ''

    def __init__(self, x):
        self.name = x[0]
        self.value = x[1]

def getNewEntity(entityName):
    obj = None
    if (entityName == 'articles'):
        obj = Article()
    if (entityName == 'customers'):
        obj = Customer()
    if (entityName == 'suppliers'):
        obj = Supplier()
    #if (entityName == 'purchases'):
    #    obj = Article()
    #if (entityName == 'sales'):
    #    obj = Article()
    return obj

def getDataFromFile(fileName):
    try:
        file = open(fileName, 'r')
        data = json.loads(file.read())
    except:
        file = open(fileName, 'w')
        file.write('[]')
        data = []

    file.close()
    return data

def writeDataInFile(fileName, data):
    file = open(fileName, 'w')
    file.write(json.dumps(data))
    file.close()

def createNewEntity(entity, params, dataIn, fileName):
    obj = getNewEntity(entity)
    lastId = 1

    if (obj == None):
        raise TypeError('Entity not aviable')

    if (len(dataIn) > 0):
        lastId = int(dataIn[len(dataIn) - 1]['id']) + 1

    params['id'] = lastId
    obj.fetchFromDictionary(params)
    dataIn.append(obj.__dict__)
    writeDataInFile(fileName, dataIn)
    return True

def updateEntity(entity, params, dataIn, fileName):
    obj = getNewEntity(entity)

    if (obj == None):
        raise TypeError('Entity not aviable')

    obj.fetchFromDictionary(params)

    for i in range(0, len(dataIn)):
        if (dataIn[i]['id'] == obj.id):
            dataIn[i] = obj.__dict__

    writeDataInFile(fileName, dataIn)
    return True

def deleteEntity(entity, params, dataIn, fileName):
    obj = getNewEntity(entity)

    if (obj == None):
        raise TypeError('Entity not aviable')

    obj.fetchFromDictionary(params)
    for x in dataIn:
        if (x['id'] == obj.id):
            dataIn.remove(x)

    writeDataInFile(fileName, dataIn)
    return True

def query(entity, action, parameters):
    fileName = ''
    if (entity == 'articles'):
        fileName = articlesFileName
    if (entity == 'customers'):
        fileName = customersFileName
    if (entity == 'suppliers'):
        fileName = suppliersFileName
    if (fileName == ''):
        raise TypeError('Entiy not aviable')

    try:
        data = getDataFromFile(fileName)
    except:
        raise Exception('Bad read')

    if (action == ''):
        return data
    if (action == 'new'):
        return createNewEntity(entity, parameters, data, fileName)
    if (action == 'update'):
        return updateEntity(entity, parameters, data, fileName)
    if (action == 'delete'):
        return deleteEntity(entity, parameters, data, fileName)

class CustomHTTPInfo:
    def __init__(self, params):
        self.name = ''
        self.parameters = {}
        self.action = ''
        cnt = 0
        v = re.compile('\=')
        for x in params:
            lP = v.split(x)
            if (cnt == 1):
                self.name = x
            if (len(lP) > 1):
                if (cnt > 1 and lP[0] != 'action'):
                    self.parameters[lP[0]] = lP[1]
                else:
                    if (cnt > 1 and lP[0] == 'action'):
                        self.action = lP[1]

            cnt = cnt + 1

    def handle(self):
        response = query(self.name, self.action, self.parameters)
        if (response == True):
            return { 'code': 1, 'msg': 'OK' }
        else:
            return response

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        info = self.getRequestInfo()
        try:
            self.wfile.write(json.dumps(info.handle()).encode())
        except:
            self.wfile.write('{ "code": 0, "msg": "Al parecer ocurrio un error. Intentelo mas tarde" }'.encode())

    def getRequestInfo(self):
        p = re.compile('\/|\?|&')
        cnt = 0
        return CustomHTTPInfo(p.split(self.path))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(self.path.encode())
        self.getHeader('Content-Length')
        #length = int(self.headers)
        #print(self.rfile.read(length))

    def getHeader(self, header):
        p = re.compile('\n')
        headers = p.split(self.headers)
        print(headers)

def main():
    httpd = HTTPServer(('', 8000), RequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    main()