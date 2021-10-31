import re
from sys import version
from flask import Flask, json, jsonify, request
from flaskext.mysql import MySQL
from werkzeug.datastructures import UpdateDictMixin

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'

app.config['MYSQL_DATABASE_USER'] = 'root'

app.config['MYSQL_DATABASE_PASSWORD'] = ''

app.config['MYSQL_DATABASE_DB'] = 'Concesionario'
mysql.init_app(app)

@app.route('/')
def inicio():
    return "REST API DEL CONSESIONARIO"

@app.route('/vendedores',methods=['GET','POST'])
def index_vendedores():
    if(request.method=='POST'):
        new_vendedor= request.get_json()
        civ=new_vendedor['civ']
        nombre=new_vendedor['nombre']
        apellido=new_vendedor['apellido']
        nacimiento=new_vendedor['birthdate']
        tipo=new_vendedor['tipo']
        salario=new_vendedor['salario']
        residencia=new_vendedor['residencia']
        telefono=new_vendedor['telefono']
        porcentaje_comision=new_vendedor['porcentajeComision']
        monto_comision=new_vendedor['montoComision']
        conn=mysql.connect()
        cur=conn.cursor()
        cur.execute("INSERT INTO vendedores(`civ`, `nombre`, `apellido`, `birthdate`, `tipo`, `salario`, `residencia`, `telefono`, `porcentajeDeComision`, `montoDeComision`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(civ,nombre,apellido,nacimiento,tipo,salario,residencia,telefono,porcentaje_comision,monto_comision))
        conn.commit()
        cur.close()
        return jsonify({"response":"Vendedor created exitosamente"}),201
    else:
        conn = mysql.connect()
        cur=conn.cursor()
        cur.execute("SELECT * FROM vendedores")
        data_vendedores=cur.fetchall()
        responseData=[]
        for vendedores in data_vendedores:
            responseDataClients=[]
            query="SELECT cedula,nombre,apellido,telefono FROM clientes where civ="+str(vendedores[0])   
            cur.execute(query)
            data_clientes=cur.fetchall()
            for clientes in data_clientes:
                print(clientes)
                responseDataClients.append({
                    "cedula":clientes[0],
                    "nombre completo":clientes[1]+" "+clientes[2],
                    "telefono":clientes[3]
                })
            responseData.append({
                "civ":vendedores[0],
                "nombre completo":vendedores[1]+" "+vendedores[2],
                "nacimiento":vendedores[3],
                "tipo":vendedores[4],
                "salario":vendedores[5],
                "residencia":vendedores[6],
                "telefono":vendedores[7],
                "porcentaje comision":vendedores[8],
                "monto comision":vendedores[9],
                "clientes": responseDataClients
            })
        cur.close()
        return jsonify({"response":responseData}),200

@app.route('/vendedores/<int:civ>',methods=['GET','PUT'])
def vendedor_civ(civ):
    if(request.method=='GET'):
        conn = mysql.connect()
        cur=conn.cursor()
        cur.execute("SELECT * FROM vendedores where civ="+str(civ))
        data_vendedores=cur.fetchall()
        print(data_vendedores)
        responseData=[]
        print(len(responseData))
        for vendedores in data_vendedores:
            responseDataClients=[]
            query="SELECT cedula,nombre,apellido,telefono FROM clientes where civ="+str(civ)   
            cur.execute(query)
            data_clientes=cur.fetchall()
            for clientes in data_clientes:
               responseDataClients.append({
                    "cedula":clientes[0],
                    "nombre completo":clientes[1]+" "+clientes[2],
                    "telefono":clientes[3]
                })
            responseData.append({
                "civ":vendedores[0],
                "nombre completo":vendedores[1]+" "+vendedores[2],
                "nacimiento":vendedores[3],
                "tipo":vendedores[4],
                "salario":vendedores[5],
                "residencia":vendedores[6],
                "telefono":vendedores[7],
                "porcentaje comision":vendedores[8],
                "monto comision":vendedores[9],
                "clientes": responseDataClients
                })
        cur.close()
        if len(responseData)==0:
            return jsonify({"response":"No se encontraron vendedores para el CIV = "+str(civ)}),404
        else:    
            return jsonify({"response":responseData}),200
    if(request.method=='PUT'):
        conn=mysql.connect()
        cur=conn.cursor()
        info_update_vendedor=request.get_json()
        nombre=None
        apellido=None
        birthdate=None
        tipo=None
        salario=None
        residencia=None
        telefono=None
        montoComision=None
        if(info_update_vendedor!=None):
            if("nombre" in info_update_vendedor):
                nombre=info_update_vendedor['nombre']
            if("apellido" in info_update_vendedor):
                apellido=info_update_vendedor['apellido']
            if("birthdate" in info_update_vendedor):
                birthdate=info_update_vendedor['birthdate']
            if("tipo" in info_update_vendedor):
                tipo=info_update_vendedor['tipo']
            if("salario" in info_update_vendedor):
                salario=info_update_vendedor['salario']
            if("residencia" in info_update_vendedor):
                residencia=info_update_vendedor['residencia']
            if("telefono" in info_update_vendedor):
                telefono=info_update_vendedor['telefono']
            if("montoComision" in info_update_vendedor):
                montoComision=info_update_vendedor['montoComision']
        else:
            return jsonify({"response":"La informacion para actualizar a "+str(civ)+" esta incompleta"}),406
        if(nombre!=None and apellido!=None and birthdate!=None and tipo!=None and salario!=None and residencia!=None and telefono!=None and montoComision!=None):
            respuesta=cur.execute("UPDATE vendedores SET nombre=%s,apellido=%s,birthdate=%s,tipo=%s,salario=%s,residencia=%s,telefono=%s,montoDeComision=%s where civ=%s",(nombre,apellido,birthdate,tipo,salario,residencia,telefono,montoComision,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406
        elif(nombre!=None and apellido!=None and birthdate!=None and tipo!=None and salario!=None and residencia!=None and telefono!=None):
            respuesta=cur.execute("UPDATE vendedores SET nombre=%s,apellido=%s,birthdate=%s,tipo=%s,salario=%s,residencia=%s,telefono=%s where civ=%s",(nombre,apellido,birthdate,tipo,salario,residencia,telefono,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406  
        elif(nombre!=None and apellido!=None and birthdate!=None and tipo!=None and salario!=None and residencia!=None):
            respuesta=cur.execute("UPDATE vendedores SET nombre=%s,apellido=%s,birthdate=%s,tipo=%s,salario=%s,residencia=%s where civ=%s",(nombre,apellido,birthdate,tipo,salario,residencia,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406 
        elif(nombre!=None and apellido!=None and birthdate!=None and tipo!=None and salario!=None):
            respuesta=cur.execute("UPDATE vendedores SET nombre=%s,apellido=%s,birthdate=%s,tipo=%s,salario=%s where civ=%s",(nombre,apellido,birthdate,tipo,salario,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406
        elif(nombre!=None and apellido!=None and birthdate!=None and tipo!=None):
            respuesta=cur.execute("UPDATE vendedores SET nombre=%s,apellido=%s,birthdate=%s,tipo=%s where civ=%s",(nombre,apellido,birthdate,tipo,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406
        elif(nombre!=None and apellido!=None and birthdate!=None ):
            respuesta=cur.execute("UPDATE vendedores SET nombre=%s,apellido=%s,birthdate=%s where civ=%s",(nombre,apellido,birthdate,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406
        elif(nombre!=None and apellido!=None):
            respuesta=cur.execute("UPDATE vendedores SET nombre=%s,apellido=%s where civ=%s",(nombre,apellido,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406
        elif(nombre!=None):
            respuesta=cur.execute("UPDATE vendedores SET nombre=%s where civ=%s",(nombre,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406
        elif(apellido!=None):
            respuesta=cur.execute("UPDATE vendedores SET apellido=%s where civ=%s",(apellido,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406 
        elif(birthdate!=None):
            respuesta=cur.execute("UPDATE vendedores SET birthdate=%s where civ=%s",(birthdate,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406 
        elif(tipo!=None):
            respuesta=cur.execute("UPDATE vendedores SET tipo=%s where civ=%s",(tipo,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406
        elif(salario!=None):
            respuesta=cur.execute("UPDATE vendedores SET salario=%s where civ=%s",(salario,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406 
        elif(residencia!=None):
            respuesta=cur.execute("UPDATE vendedores SET residencia=%s where civ=%s",(residencia,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406
        elif(telefono!=None):
            respuesta=cur.execute("UPDATE vendedores SET telefono=%s where civ=%s",(telefono,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406
        elif(montoComision!=None):
            respuesta=cur.execute("UPDATE vendedores SET montoDeComision=%s where civ=%s",(montoComision,civ))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN VENDEDOR CON CIV= "+str(civ)}),406     
        else:
            return jsonify({"response":"ERROR CON LA INFORMACION"}),406
        conn.commit()
        cur.close()
        return jsonify({"response":"Vendedor con CIV="+str(civ)+" actualizado con exito"}),201
@app.route('/clientes', methods=['GET','POST'])  
def index_clientes():
    if(request.method=='POST'):
        new_cliente= request.get_json()
        cedula=new_cliente['cedula']
        tipoCedula =new_cliente['tipoCedula']
        nombre=new_cliente['nombre']
        apellido =new_cliente['apellido']
        calificacionCredito=new_cliente['calificacionCredito']
        residencia=new_cliente['residencia']
        telefono =new_cliente['telefono']
        birthdate =new_cliente['birthdate']
        civ=new_cliente['civ']
        conn=mysql.connect()
        cur=conn.cursor()
        cur.execute("INSERT INTO `clientes` (`cedula`, `tipoCedula`, `nombre`, `apellido`, `calificacionCredito`, `residencia`, `telefono`, `birthdate`, `civ`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(cedula,tipoCedula,nombre,apellido,calificacionCredito,residencia,telefono,birthdate,civ))
        conn.commit()
        cur.close()
        return jsonify({"response":"Cliente created exitosamente"}),201
    if(request.method=='GET'):
        conn = mysql.connect()
        cur=conn.cursor()
        cur.execute("SELECT * FROM clientes")
        data_clientes=cur.fetchall()
        responseData=[]
        for clientes in data_clientes:
            responseDataSellers=[]
            query="SELECT civ,nombre,apellido,telefono FROM vendedores where civ="+str(clientes[8])   
            cur.execute(query)
            data_vendedores=cur.fetchall()
            print(data_vendedores)
            for vendedores in data_vendedores:
                print(vendedores)
                responseDataSellers.append({
                    "civ":vendedores[0],
                    "nombre completo":vendedores[1]+" "+vendedores[2],
                    "telefono":vendedores[3]
                })
            responseDataCompras=[]
            query="SELECT cuv,codigoConsecutivo,monto,fechaVenta,marca,modelo,year FROM ventas where cedulaCliente="+str(clientes[0]) 
            cur.execute(query)
            data_compras=cur.fetchall()
            print(data_compras)
            for compras in data_compras:
                print(compras)
                responseDataCompras.append({
                    "cuv":compras[0],
                    "Codigo Consecutivo":compras[1],
                    "Monto":compras[2],
                    "Fecha de Venta":compras[3],
                    "Tipo de Auto Movil":str(compras[4])+" "+str(compras[5])+" "+str(compras[6])
                })   
            responseData.append({
                "cedula":clientes[0],
                "nombre completo":clientes[2]+" "+clientes[3],
                "nacimiento":clientes[7],
                "tipo de cedula":clientes[1],
                "calificacion credito":clientes[4],
                "residencia":clientes[5],
                "telefono":clientes[6],
                "Vendedor": responseDataSellers,
                "Compras": responseDataCompras
            })
        cur.close()
        return jsonify({"response":responseData}),200
@app.route('/clientes/<int:cedula>',methods=['GET','PUT'])
def cliente_cedula(cedula):
    if(request.method=='GET'):
        conn = mysql.connect()
        cur=conn.cursor()
        cur.execute("SELECT * FROM clientes where cedula="+str(cedula))
        data_clientes=cur.fetchall()
        responseData=[]
        for clientes in data_clientes:
            responseDataSellers=[]
            query="SELECT civ,nombre,apellido,telefono FROM vendedores where civ="+str(clientes[8])   
            cur.execute(query)
            data_vendedores=cur.fetchall()
            print(data_vendedores)
            for vendedores in data_vendedores:
                print(vendedores)
                responseDataSellers.append({
                    "civ":vendedores[0],
                    "nombre completo":vendedores[1]+" "+vendedores[2],
                    "telefono":vendedores[3]
                })
            responseDataCompras=[]
            query="SELECT cuv,codigoConsecutivo,monto,fechaVenta,marca,modelo,year FROM ventas where cedulaCliente="+str(clientes[0]) 
            cur.execute(query)
            data_compras=cur.fetchall()
            print(data_compras)
            for compras in data_compras:
                print(compras)
                responseDataCompras.append({
                    "cuv":compras[0],
                    "Codigo Consecutivo":compras[1],
                    "Monto":compras[2],
                    "Fecha de Venta":compras[3],
                    "Tipo de Auto Movil":str(compras[4])+" "+str(compras[5])+" "+str(compras[6])
                })   
            responseData.append({
                "cedula":clientes[0],
                "nombre completo":clientes[2]+" "+clientes[3],
                "nacimiento":clientes[7],
                "tipo de cedula":clientes[1],
                "calificacion credito":clientes[4],
                "residencia":clientes[5],
                "telefono":clientes[6],
                "Vendedor": responseDataSellers,
                "Compras": responseDataCompras
            })
        cur.close()
        if len(responseData)==0:
            return jsonify({"response":"No se encontraron clientes con cedula= "+str(cedula)}),404
        return jsonify({"response":responseData}),200
    if(request.method=='PUT'):
        conn=mysql.connect()
        cur=conn.cursor()
        info_update_cliente=request.get_json()
        ncedula=None
        tipoCedula=None
        nombre=None
        apellido=None
        calificacionCredito=None
        residencia=None
        telefono=None
        birthdate=None
        civ=None
        if(info_update_cliente!=None):
            if("cedula" in info_update_cliente):
                ncedula=info_update_cliente['cedula']
            if("tipoCedula" in info_update_cliente):
                tipoCedula=info_update_cliente['tipoCedula']
            if("nombre" in info_update_cliente):
                nombre=info_update_cliente['nombre']
            if("apellido" in info_update_cliente):
                apellido=info_update_cliente['apellido']
            if("calificacionCredito" in info_update_cliente):
                calificacionCredito=info_update_cliente['calificacionCredito']
            if("residencia" in info_update_cliente):
                residencia=info_update_cliente['residencia']
            if("telefono" in info_update_cliente):
                telefono=info_update_cliente['telefono']
            if("birthdate" in info_update_cliente):
                birthdate=info_update_cliente['birthdate']
            if("civ" in info_update_cliente):
                civ=info_update_cliente['civ']    
        else:
            return jsonify({"response":"La informacion para actualizar a "+str(cedula)+" esta incompleta"}),406
        if(ncedula!=None and tipoCedula!=None and nombre!=None and apellido!=None and calificacionCredito!=None and residencia!=None and telefono!=None and birthdate!=None and civ!=None):
            respuesta=cur.execute("UPDATE clientes SET cedula=%s,tipoCedula=%s,nombre=%s,apellido=%s,calificacionCredito=%s,residencia=%s,telefono=%s,birthdate=%s,civ=%s where cedula=%s",(ncedula,tipoCedula,nombre,apellido,calificacionCredito,residencia,telefono,birthdate,civ,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404
        elif(ncedula!=None and tipoCedula!=None and nombre!=None and apellido!=None and calificacionCredito!=None and residencia!=None and telefono!=None and birthdate!=None):
            respuesta=cur.execute("UPDATE clientes SET cedula=%s,tipoCedula=%s,nombre=%s,apellido=%s,calificacionCredito=%s,residencia=%s,telefono=%s,birthdate=%s where cedula=%s",(ncedula,tipoCedula,nombre,apellido,calificacionCredito,residencia,telefono,birthdate,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404
        elif(ncedula!=None and tipoCedula!=None and nombre!=None and apellido!=None and calificacionCredito!=None and residencia!=None and telefono!=None):
            respuesta=cur.execute("UPDATE clientes SET cedula=%s,tipoCedula=%s,nombre=%s,apellido=%s,calificacionCredito=%s,residencia=%s,telefono=%s where cedula=%s",(ncedula,tipoCedula,nombre,apellido,calificacionCredito,residencia,telefono,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404
        elif(ncedula!=None and tipoCedula!=None and nombre!=None and apellido!=None and calificacionCredito!=None and residencia!=None):
            respuesta=cur.execute("UPDATE clientes SET cedula=%s,tipoCedula=%s,nombre=%s,apellido=%s,calificacionCredito=%s,residencia=%s where cedula=%s",(ncedula,tipoCedula,nombre,apellido,calificacionCredito,residencia,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404 
        elif(ncedula!=None and tipoCedula!=None and nombre!=None and apellido!=None and calificacionCredito!=None):
            respuesta=cur.execute("UPDATE clientes SET cedula=%s,tipoCedula=%s,nombre=%s,apellido=%s,calificacionCredito=%s where cedula=%s",(ncedula,tipoCedula,nombre,apellido,calificacionCredito,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404  
        elif(ncedula!=None and tipoCedula!=None and nombre!=None and apellido!=None):
            respuesta=cur.execute("UPDATE clientes SET cedula=%s,tipoCedula=%s,nombre=%s,apellido=%s where cedula=%s",(ncedula,tipoCedula,nombre,apellido,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404 
        elif(ncedula!=None and tipoCedula!=None and nombre!=None):
            respuesta=cur.execute("UPDATE clientes SET cedula=%s,tipoCedula=%s,nombre=%s where cedula=%s",(ncedula,tipoCedula,nombre,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404 
        elif(ncedula!=None and tipoCedula!=None):
            respuesta=cur.execute("UPDATE clientes SET cedula=%s,tipoCedula=%s where cedula=%s",(ncedula,tipoCedula,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404
        elif(ncedula!=None):
            respuesta=cur.execute("UPDATE clientes SET cedula=%s where cedula=%s",(ncedula,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404   
        elif(tipoCedula!=None):
            respuesta=cur.execute("UPDATE clientes SET tipoCedula =%s where cedula=%s",(tipoCedula,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404 
        elif(nombre !=None):
            respuesta=cur.execute("UPDATE clientes SET nombre =%s where cedula=%s",(nombre ,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404 
        elif(apellido !=None):
            respuesta=cur.execute("UPDATE clientes SET apellido =%s where cedula=%s",(apellido ,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404 
        elif(calificacionCredito!=None):
            respuesta=cur.execute("UPDATE clientes SET calificacionCredito=%s where cedula=%s",(calificacionCredito,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404 
        elif( residencia!=None):
            respuesta=cur.execute("UPDATE clientes SET residencia=%s where cedula=%s",(residencia,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404 
        elif(telefono !=None):
            respuesta=cur.execute("UPDATE clientes SET telefono =%s where cedula=%s",(telefono ,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404 
        elif(birthdate!=None):
            respuesta=cur.execute("UPDATE clientes SET birthdate=%s where cedula=%s",(birthdate,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404 
        elif(civ!=None):
            respuesta=cur.execute("UPDATE clientes SET civ=%s where cedula=%s",(civ,cedula))
            print(respuesta)
            if(respuesta==0):
                return jsonify({"response":"NO HAY NINGUN CLIENTE CON CEDULA= "+str(cedula)}),404   
        else:
            return jsonify({"response":"ERROR CON LA INFORMACION"}),406
        conn.commit()
        cur.close()
        return jsonify({"response":"Cliente con Cedula="+str(cedula)+" actualizado con exito"}),201
@app.route('/ventas',methods=['POST','GET'])
def index_ventas():
    if(request.method=='POST'):
        new_venta= request.get_json()
        codigoConsecutivo=new_venta['codigoConsecutivo']
        numeroContrato=new_venta['numeroContrato']
        civ=new_venta['civ']
        cedulaCliente=new_venta['cedulaCliente']
        monto=new_venta['monto']
        fechaVenta=new_venta['fechaVenta']
        producto =new_venta['producto']
        marca=new_venta['marca']
        modelo=new_venta['modelo']
        year=new_venta['year']
        conn=mysql.connect()
        cur=conn.cursor()
        cur.execute("INSERT INTO `ventas` (`codigoConsecutivo`, `numeroContrato`, `civ`, `cedulaCliente`, `monto`, `fechaVenta`, `producto`, `marca`, `modelo`, `year`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(codigoConsecutivo,numeroContrato,civ,cedulaCliente,monto,fechaVenta,producto,marca,modelo,year))
        cur.execute("SELECT porcentajeDeComision,montoDeComision FROM vendedores where civ="+str(civ))
        datos=cur.fetchone()
        print(datos)

        porcentaje=float(datos[0])/100
        print(porcentaje)
        comisioncalc=float(monto)*porcentaje
        commisionsuma=float(datos[1])+comisioncalc
        print(commisionsuma)
        comisionsumafinal=int(commisionsuma)
        print(comisionsumafinal)

        cur.execute("UPDATE vendedores SET montoDeComision=%s WHERE civ=%s",(str(comisionsumafinal),civ))
        conn.commit()
        cur.close()
        return jsonify({"response":"Venta Registrada exitosamente"}),201
    if(request.method=='GET'):
        conn=mysql.connect()
        cur=conn.cursor()
        cur.execute("SELECT * FROM ventas")
        data_ventas=cur.fetchall()
        responseData=[]
        for ventas in data_ventas:
            responseDataClients=[]
            query="SELECT cedula,nombre,apellido,telefono FROM clientes where cedula="+str(ventas[4])   
            cur.execute(query)
            data_clientes=cur.fetchall()
            for clientes in data_clientes:
               responseDataClients.append({
                    "cedula":clientes[0],
                    "nombre completo":clientes[1]+" "+clientes[2],
                    "telefono":clientes[3]
                })
            responseDataSellers=[]
            query="SELECT civ,nombre,apellido,telefono FROM vendedores where civ="+str(ventas[3])   
            cur.execute(query)
            data_vendedores=cur.fetchall()
            print(data_vendedores)
            for vendedores in data_vendedores:
                print(vendedores)
                responseDataSellers.append({
                    "civ":vendedores[0],
                    "nombre completo":vendedores[1]+" "+vendedores[2],
                    "telefono":vendedores[3]
                })
            responseData.append({
                "cuv":ventas[0],
                "codigo consecutivo":ventas[1],
                "numero de contrato":ventas[2],
                "monto":ventas[5],
                "fecha venta":ventas[6],
                "producto":ventas[7],
                "tipo de vehiculo":str(ventas[8])+" "+str(ventas[9])+" "+str(ventas[10]),
                "vendedor": responseDataSellers,
                "comprador":responseDataClients
            })
        return jsonify({"response":responseData}),200
@app.route('/ventas/<int:cuv>',methods=['GET'])
def getVentaByID(cuv):
    conn=mysql.connect()
    cur=conn.cursor()
    cur.execute("SELECT * FROM ventas where cuv="+str(cuv))
    data_ventas=cur.fetchall()
    responseData=[]
    for ventas in data_ventas:
        responseDataClients=[]
        query="SELECT cedula,nombre,apellido,telefono FROM clientes where cedula="+str(ventas[4])   
        cur.execute(query)
        data_clientes=cur.fetchall()
        for clientes in data_clientes:
            responseDataClients.append({
                "cedula":clientes[0],
                "nombre completo":clientes[1]+" "+clientes[2],
                "telefono":clientes[3]
            })
        responseDataSellers=[]
        query="SELECT civ,nombre,apellido,telefono FROM vendedores where civ="+str(ventas[3])   
        cur.execute(query)
        data_vendedores=cur.fetchall()
        print(data_vendedores)
        for vendedores in data_vendedores:
            print(vendedores)
            responseDataSellers.append({
                "civ":vendedores[0],
                "nombre completo":vendedores[1]+" "+vendedores[2],
                "telefono":vendedores[3]
            })
        responseData.append({
            "cuv":ventas[0],
            "codigo consecutivo":ventas[1],
            "numero de contrato":ventas[2],
            "monto":ventas[5],
            "fecha venta":ventas[6],
            "producto":ventas[7],
            "tipo de vehiculo":str(ventas[8])+" "+str(ventas[9])+" "+str(ventas[10]),
            "vendedor": responseDataSellers,
            "comprador":responseDataClients
        })
    return jsonify({"response":responseData}),200
    





        












    

