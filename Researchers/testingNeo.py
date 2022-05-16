import os


if('./static/a.jpg'):
    print("A")

# import glob
# from datetime import datetime
# from neo4j import GraphDatabase
# import xml.etree.ElementTree as ET
#
# gdb = GraphDatabase.driver(uri="neo4j+s://24ab16aa.databases.neo4j.io",
#                            auth=("neo4j", "G6tmsnc3xhwupcL5RwPq7tRXBpB5wgUnyWR3ch4Tfws"))
# session = gdb.session()
#
# xaadı = ""
# xsoyadı = ""
# xyadı = ""
# xyyılı = ""
# xtadı = ""
# xtyeri = ""
# start_time = datetime.now()
# for hepsi in range(len(glob.glob("./xmlfiles/*.xml"))):
#     myroot = ET.parse(glob.glob("./xmlfiles/*.xml")[hepsi]).getroot()
#     for x in range(len(myroot)):
#         if (myroot[x].tag == "r"):
#             for a in myroot[x]:
#                 if (a.tag == "inproceedings"):
#                     xtadı = "Bildiri"
#                 elif (a.tag == "article"):
#                     xtadı = "Makale"
#                 elif (a.tag == "incollection"):
#                     xtadı = "Kitap"
#                 for b in reversed(a):
#                     if (b.tag == "year"):
#                         xyyılı = b.text
#                     if (b.tag == "booktitle"):
#                         xtyeri = b.text
#                     elif (b.tag == "journal"):
#                         xtyeri = b.text
#                     if (b.tag == "title"):
#                         xyadı = b.text
#                     if (b.tag == "author"):
#                         xaadı = b.text
#                         if (len(xaadı.split()) == 2):
#                             nodes = session.run(
#                                 "match(a) where a.aadı='" + xaadı.split()[0] + "' and a.asoyadı='" + xaadı.split()[
#                                     1] + "' return(a)")
#                             aras = 0;
#                             for node in nodes:
#                                 aras += 1;
#                             ynodes = session.run("match(a) where a.yadı='" + xyadı + "' return(a)")
#                             byad = 0;
#                             for ynode in ynodes:
#                                 byad += 1;
#                             nodes = session.run("MATCH (n:`Araştırmacı`) RETURN (n)")
#                             aid = 1
#                             for node in nodes:
#                                 aid += 1
#                             nodes = session.run("MATCH (n:`Türler`) RETURN (n)")
#                             tid = 1
#                             for node in nodes:
#                                 tid += 1
#
#                             print(aid, xaadı.split()[0], xaadı.split()[1], xyadı, xyyılı, tid, xtadı, xtyeri)
#                             if (aras == 0 and byad == 0):
#                                 session.run(
#                                     " CREATE (a:`Araştırmacı`{aid:" + str(aid) + ", aadı:\"" + xaadı.split()[
#                                         0] + "\",asoyadı:\"" + xaadı.split()[
#                                         1] + "\"}) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"" + xyadı + "\",yyılı:\"" + xyyılı + "\"}) -[:YAYINLANIR] ->(c:`Türler`{tid:" + str(
#                                         tid) + ",tadı:\"" + xtadı + "\", tyeri:\"" + xtyeri + "\"})")
#
#
#                             elif (aras != 0 and byad == 0):
#                                 session.run(
#                                     " match(a:`Araştırmacı`{aadı:\"" + xaadı.split()[0] + "\",asoyadı:\"" +
#                                     xaadı.split()[
#                                         1] + "\"}) CREATE (a) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"" + xyadı + "\",yyılı:\"" + xyyılı + "\"}) -[:YAYINLANIR] -> (c:`Türler`{tid:" + str(
#                                         tid) + ",tadı:\"" + xtadı + "\", tyeri:\"" + xtyeri + "\"})")
#
#
#                             elif (aras == 0 and byad != 0):
#                                 session.run(
#                                     " match(b:`Yayınlar`{yadı:\"" + xyadı + "\"}) CREATE (a:`Araştırmacı`{aid:" + str(
#                                         aid) + ",aadı:\"" + xaadı.split()[0] + "\", asoyadı:\"" + xaadı.split()[
#                                         1] + "\"}) -[:YAYINLAR] -> (b)")
#
#                             elif (a != 0 and b != 0):
#                                 deneme = session.run(
#                                     "MATCH (n:`Araştırmacı`{`aadı`:\"" + xaadı.split()[0] + "\",asoyadı:\"" +
#                                     xaadı.split()[
#                                         1] + "\"}) -[:YAYINLAR]->(b:Yayınlar{yadı:\"" + xyadı + "\"}) RETURN n,b ")
#                                 bbb = 0
#                                 for a in deneme:
#                                     bbb += 1
#                                 if (bbb == 0):
#                                     session.run(
#                                         "match(a:Araştırmacı{aadı:\"" + xaadı.split()[0] + "\",asoyadı:\"" +
#                                         xaadı.split()[
#                                             1] + "\"}), (b:Yayınlar {yadı:\"" + xyadı + "\"}) CREATE (a)-[:YAYINLAR]->(b)")
#                                 elif (bbb == 1):
#                                     print("Zaten YAYINLAR var")
#
#                             else:
#                                 print("Araştırmacı ID'sini kontrol ediniz...")
#
#                         elif (len(xaadı.split()) == 3):
#                             nodes = session.run(
#                                 "match(a) where a.aadı='" + xaadı.split()[0] + " " + xaadı.split()[
#                                     1] + "' and a.asoyadı='" + xaadı.split()[
#                                     2] + "' return(a)")
#                             aras = 0;
#                             for node in nodes:
#                                 aras += 1;
#                             ynodes = session.run("match(a) where a.yadı='" + xyadı + "' return(a)")
#                             byad = 0;
#                             for ynode in ynodes:
#                                 byad += 1;
#                             nodes = session.run("MATCH (n:`Araştırmacı`) RETURN (n)")
#                             aid = 1
#                             for node in nodes:
#                                 aid += 1
#                             nodes = session.run("MATCH (n:`Türler`) RETURN (n)")
#                             tid = 1
#                             for node in nodes:
#                                 tid += 1
#
#                             print(aid, xaadı.split()[0], xaadı.split()[1], xyadı, xyyılı, tid, xtadı, xtyeri)
#                             if (aras == 0 and byad == 0):
#                                 session.run(
#                                     " CREATE (a:`Araştırmacı`{aid:" + str(aid) + ", aadı:\"" + xaadı.split()[0] + " " +
#                                     xaadı.split()[1] + "\",asoyadı:\"" + xaadı.split()[
#                                         2] + "\"}) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"" + xyadı + "\",yyılı:\"" + xyyılı + "\"}) -[:YAYINLANIR] ->(c:`Türler`{tid:" + str(
#                                         tid) + ",tadı:\"" + xtadı + "\", tyeri:\"" + xtyeri + "\"})")
#
#
#                             elif (aras != 0 and byad == 0):
#                                 session.run(
#                                     " match(a:`Araştırmacı`{aadı:\"" + xaadı.split()[0] + " " + xaadı.split()[
#                                         1] + "\",asoyadı:\"" +
#                                     xaadı.split()[
#                                         2] + "\"}) CREATE (a) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"" + xyadı + "\",yyılı:\"" + xyyılı + "\"}) -[:YAYINLANIR] -> (c:`Türler`{tid:" + str(
#                                         tid) + ",tadı:\"" + xtadı + "\", tyeri:\"" + xtyeri + "\"})")
#
#                             elif (aras == 0 and byad != 0):
#                                 session.run(
#                                     " match(b:`Yayınlar`{yadı:\"" + xyadı + "\"}) CREATE (a:`Araştırmacı`{aid:" + str(
#                                         aid) + ",aadı:\"" + xaadı.split()[0] + " " + xaadı.split()[
#                                         1] + "\", asoyadı:\"" + xaadı.split()[
#                                         2] + "\"}) -[:YAYINLAR] -> (b)")
#
#                             elif (a != 0 and b != 0):
#                                 deneme = session.run(
#                                     "MATCH (n:`Araştırmacı`{`aadı`:\"" + xaadı.split()[0] + " " + xaadı.split()[
#                                         1] + "\",asoyadı:\"" + xaadı.split()[
#                                         2] + "\"}) -[:YAYINLAR]->(b:Yayınlar{yadı:\"" + xyadı + "\"}) RETURN n,b ")
#                                 bbb = 0
#                                 for a in deneme:
#                                     bbb += 1
#                                 if (bbb == 0):
#                                     session.run(
#                                         "match(a:Araştırmacı{aadı:\"" + xaadı.split()[0] + " " + xaadı.split()[
#                                             1] + "\",asoyadı:\"" + xaadı.split()[
#                                             2] + "\"}), (b:Yayınlar {yadı:\"" + xyadı + "\"}) CREATE (a)-[:YAYINLAR]->(b)")
#                                 elif (bbb == 1):
#                                     print("Zaten YAYINLAR var")
#
#
#
#                             else:
#                                 print("Araştırmacı ID'sini kontrol ediniz...")
#
# nodes = session.run("MATCH (a)-[:YAYINLAR]->(m)<-[:YAYINLAR]-(b)RETURN a.aadı,b.aadı;")
# aad = []
# bad = []
# ortaklar = []
# for node in nodes:
#     aad.append(dict(node)["a.aadı"])
#     bad.append(dict(node)["b.aadı"])
# for i in range(len(aad)):
#     tmpa = aad[i]
#     tmpb = bad[i]
#     for j in range(len(bad)):
#         if(aad[j] == tmpa and bad[j] == tmpb and i!=j):
#             ortaklar.append(j)
# for i in reversed(range(len(list(dict.fromkeys(sorted(ortaklar)))))):
#     aad.pop(list(dict.fromkeys(sorted(ortaklar)))[i])
#     bad.pop(list(dict.fromkeys(sorted(ortaklar)))[i])
#
# for i in range(len(aad)):
#     aaa = 0
#     nodes = session.run(
#         "MATCH (a:Araştırmacı {aadı:\"" + aad[i] + "\"})-[:ORTAK_ÇALIŞIR]->(b:Araştırmacı {aadı:\"" + bad[
#             i] + "\"}) RETURN *")
#     for node in nodes:
#         aaa += 1
#     if(aaa == 0):
#         session.run(
#             "MATCH (a:Araştırmacı {aadı:\"" + aad[i] + "\"}), (b:Araştırmacı {aadı:\"" + bad[
#                 i] + "\"}) CREATE (a)-[:ORTAK_ÇALIŞIR] ->(b)")
#
#
# end_time = datetime.now()
# print('Duration: {}'.format(end_time - start_time))
#



# nodes = session.run("MATCH p = (a)-[r:YAYINLAR]->(b) RETURN a,b")
# tmpaadı = []
# tmpasoyadı = []
# tmpyadı = []
# tmpyyılı= []
# tmptadı = []
# tmptyeri = []
# for node in nodes:
#     tmpaadı.append(dict(dict(node)['a'])['aadı'])
#     tmpasoyadı.append(dict(dict(node)['a'])['asoyadı'])
#     tmpyadı.append(dict(dict(node)['b'])['yadı'])
#     tmpyyılı.append(dict(dict(node)['b'])['yyılı'])
#
# nodes = session.run("MATCH p = (a)-[r:YAYINLANIR]->(b) RETURN a,b")
# tmp2yadı = []
# tmp2yyılı = []
# tmp2tadı = []
# tmp2tyeri = []
# for node in nodes:
#     tmp2yadı.append(dict(dict(node)['a'])['yadı'])
#     tmp2yyılı.append(dict(dict(node)['a'])['yyılı'])
#     tmp2tadı.append(dict(dict(node)['b'])['tadı'])
#     tmp2tyeri.append(dict(dict(node)['b'])['tyeri'])
#
# for i in range(len(tmpyadı)):
#     for j in range (len(tmp2yadı)):
#         if(tmpyadı[i] == tmp2yadı[j]):
#             tmptadı.append(tmp2tadı[j])
#             tmptyeri.append(tmp2tyeri[j])
#
#
#
# nodes = session.run("Match (a:Araştırmacı) return a" )
# tmp3aadı = []
# tmp3asoyadı = []
# for node in nodes:
#     tmp3aadı.append(dict(dict(node)['a'])["aadı"])
#     tmp3asoyadı.append(dict(dict(node)['a'])['asoyadı'])
#
# tmp4a = []
# for i in reversed(range(len(tmp3aadı))):
#     for j in range(len(tmpaadı)):
#         if (tmp3aadı[i] == tmpaadı[j]):
#             tmp4a.append(i)
#
# tmp4a = list(dict.fromkeys(tmp4a))
# for i in range(len(tmp4a)):
#     tmp3aadı.pop(tmp4a[i])
#     tmp3asoyadı.pop(tmp4a[i])
#
# for i in range(len(tmp3aadı)):
#     tmpaadı.append(tmp3aadı[i])
#     tmpasoyadı.append(tmp3asoyadı[i])
#     tmpyadı.append("-")
#     tmpyyılı.append("-")
#     tmptyeri.append("-")
#     tmptadı.append("-")


# nodes = session.run("MATCH (a)-[:YAYINLAR]->(m)<-[:YAYINLAR]-(b)RETURN a.aadı,b.aadı;")
#
# aad = []
# bad = []
# for node in nodes:
#     aad.append(dict(node)["a.aadı"])
#     bad.append(dict(node)["b.aadı"])
#
# ortaki = []
# for i in range(len(aad)):
#         nodes = session.run(
#         "MATCH (a:Araştırmacı {aadı:\""+aad[i]+"\"})-[:ORTAK_ÇALIŞIR]->(b:Araştırmacı {aadı:\""+bad[i]+"\"}) RETURN *")
#         for node in nodes:
#             ortaki.append(i)
#
# for i in reversed(range(len(ortaki))):
#     aad.pop(ortaki[i])
#     bad.pop(ortaki[i])
#
# for i in range(len(aad)):
#     session.run(
#         "MATCH (a:Araştırmacı {aadı:\""+aad[i]+"\"}), (b:Araştırmacı {aadı:\""+bad[i]+"\"}) CREATE (a)-[:ORTAK_ÇALIŞIR] ->(b)")


#     a += 1;
#     print(node)
# if(a==0):
#     session.run("create (a:`Araştırmacı`{aid:3,aadı:\"Ersin\",asoyadı:\"Aslan\"})")
# else:
#     print("Zaten Var")
#
# ############ARAŞTIRMACI VE YAYINLAR EĞER İSİM SOYİSİM VAR YAYIN ADI YOK İSE
# nodes = session.run("match(a) where a.aadı='Tekila' and a.asoyadı='Yılmaz' return(a)")
# a = 0;
# for node in nodes:
#     a += 1;
#     print(node)
#
# ynodes = session.run("match(a) where a.yadı='Kedi Maması' return(a)")
# b = 0;
# for ynode in ynodes:
#     b += 1;
#     print(ynode)
#
# tnodes = session.run("MATCH (n:`Türler`) RETURN n")
# c = 1;
# for tnode in tnodes:
#     c += 1;
#     print(tnode)
#
# if(a==0 and b==0):
#     session.run(" CREATE (a:`Araştırmacı`{aid:5, aadı:\"Tekila\",asoyadı:\"Yılmaz\"}) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"Kedi Maması\",yyılı:\"2003\"}) -[:YAYINLANIR] ->(c:`Türler`{tid:"+str(c)+",tadı:\"Gazete\", tyeri:\"Kediviskas\"})")
# elif (a!=0 and b==0):
#     session.run(" match(a:`Araştırmacı`{aadı:\"Tekila\",asoyadı:\"Yılmaz\"}) CREATE (a) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"MichaelJack\",yyılı:\"2001\"}) -[:YAYINLANIR] -> (c:`Türler`{tid:5,tadı:\"Gazete\", tyeri:\"KesKesKes\"})")
# elif(a==0 and b!=0):
#     session.run(" match(b:`Yayınlar`{yadı:\"Michael\"}) CREATE (a:`Araştırmacı`{aid:6,aadı:\"Furkan\", asoyadı:\"Göz\"}) -[:YAYINLAR] -> (b)")
# elif (a!=0 and b!=0):
#     print("Girilen araştırmacı ve yayın zaten var")
# else:
#     print(" Bu nasıl error la")
