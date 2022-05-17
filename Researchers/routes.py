import os
import secrets
import glob
import xml.etree.ElementTree as ET
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from neo4j import GraphDatabase
from Researchers import app, db, bcrypt
from Researchers.forms import RegistrationForm, LoginForm, UpdateAccountForm, AdminLoginForm, DataForm, DataForm1
from Researchers.models import User

@app.route("/researchers/<name>/<lname>", methods=['GET','POST'])
def researchers(name, lname):
    return render_template('researchers.html',name = name, lname = lname)

@app.route("/xmlveri", methods=['GET','POST'])
def xmlveri():
    gdb = GraphDatabase.driver(uri="neo4j+s://d0e5fa0d.databases.neo4j.io:7687",
                               auth=("neo4j", "seE64dMcF-aJ-Nv5bQqNidDzFfN4OrIolYgGm6yM2yY"))
    session = gdb.session()

    xaadı = ""
    xsoyadı = ""
    xyadı = ""
    xyyılı = ""
    xtadı = ""
    xtyeri = ""
    for hepsi in range(len(glob.glob("./xmlfiles/*.xml"))):
        myroot = ET.parse(glob.glob("./xmlfiles/*.xml")[hepsi]).getroot()
        for x in range(len(myroot)):
            if (myroot[x].tag == "r"):
                for a in myroot[x]:
                    if (a.tag == "inproceedings"):
                        xtadı = "Bildiri"
                    elif (a.tag == "article"):
                        xtadı = "Makale"
                    elif (a.tag == "incollection"):
                        xtadı = "Kitap"
                    for b in reversed(a):
                        if (b.tag == "year"):
                            xyyılı = b.text
                        if (b.tag == "booktitle"):
                            xtyeri = b.text
                        elif (b.tag == "journal"):
                            xtyeri = b.text
                        if (b.tag == "title"):
                            xyadı = b.text
                        if (b.tag == "author"):
                            xaadı = b.text
                            if (len(xaadı.split()) == 2):
                                nodes = session.run(
                                    "match(a) where a.aadı='" + xaadı.split()[0] + "' and a.asoyadı='" + xaadı.split()[
                                        1] + "' return(a)")
                                aras = 0;
                                for node in nodes:
                                    aras += 1;
                                ynodes = session.run("match(a) where a.yadı='" + xyadı + "' return(a)")
                                byad = 0;
                                for ynode in ynodes:
                                    byad += 1;
                                nodes = session.run("MATCH (n:`Araştırmacı`) RETURN (n)")
                                aid = 1
                                for node in nodes:
                                    aid += 1
                                nodes = session.run("MATCH (n:`Türler`) RETURN (n)")
                                tid = 1
                                for node in nodes:
                                    tid += 1

                                print(aid, xaadı.split()[0], xaadı.split()[1], xyadı, xyyılı, tid, xtadı, xtyeri)
                                if (aras == 0 and byad == 0):
                                    session.run(
                                        " CREATE (a:`Araştırmacı`{aid:" + str(aid) + ", aadı:\"" + xaadı.split()[
                                            0] + "\",asoyadı:\"" + xaadı.split()[
                                            1] + "\"}) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"" + xyadı + "\",yyılı:\"" + xyyılı + "\"}) -[:YAYINLANIR] ->(c:`Türler`{tid:" + str(
                                            tid) + ",tadı:\"" + xtadı + "\", tyeri:\"" + xtyeri + "\"})")


                                elif (aras != 0 and byad == 0):
                                    session.run(
                                        " match(a:`Araştırmacı`{aadı:\"" + xaadı.split()[0] + "\",asoyadı:\"" +
                                        xaadı.split()[
                                            1] + "\"}) CREATE (a) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"" + xyadı + "\",yyılı:\"" + xyyılı + "\"}) -[:YAYINLANIR] -> (c:`Türler`{tid:" + str(
                                            tid) + ",tadı:\"" + xtadı + "\", tyeri:\"" + xtyeri + "\"})")


                                elif (aras == 0 and byad != 0):
                                    session.run(
                                        " match(b:`Yayınlar`{yadı:\"" + xyadı + "\"}) CREATE (a:`Araştırmacı`{aid:" + str(
                                            aid) + ",aadı:\"" + xaadı.split()[0] + "\", asoyadı:\"" + xaadı.split()[
                                            1] + "\"}) -[:YAYINLAR] -> (b)")

                                elif (a != 0 and b != 0):
                                    deneme = session.run(
                                        "MATCH (n:`Araştırmacı`{`aadı`:\"" + xaadı.split()[0] + "\",asoyadı:\"" +
                                        xaadı.split()[
                                            1] + "\"}) -[:YAYINLAR]->(b:Yayınlar{yadı:\"" + xyadı + "\"}) RETURN n,b ")
                                    bbb = 0
                                    for a in deneme:
                                        bbb += 1
                                    if (bbb == 0):
                                        session.run(
                                            "match(a:Araştırmacı{aadı:\"" + xaadı.split()[0] + "\",asoyadı:\"" +
                                            xaadı.split()[
                                                1] + "\"}), (b:Yayınlar {yadı:\"" + xyadı + "\"}) CREATE (a)-[:YAYINLAR]->(b)")
                                    elif (bbb == 1):
                                        print("Zaten YAYINLAR var")

                                else:
                                    print("Araştırmacı ID'sini kontrol ediniz...")

                            elif (len(xaadı.split()) == 3):
                                nodes = session.run(
                                    "match(a) where a.aadı='" + xaadı.split()[0] + " " + xaadı.split()[
                                        1] + "' and a.asoyadı='" + xaadı.split()[
                                        2] + "' return(a)")
                                aras = 0;
                                for node in nodes:
                                    aras += 1;
                                ynodes = session.run("match(a) where a.yadı='" + xyadı + "' return(a)")
                                byad = 0;
                                for ynode in ynodes:
                                    byad += 1;
                                nodes = session.run("MATCH (n:`Araştırmacı`) RETURN (n)")
                                aid = 1
                                for node in nodes:
                                    aid += 1
                                nodes = session.run("MATCH (n:`Türler`) RETURN (n)")
                                tid = 1
                                for node in nodes:
                                    tid += 1

                                print(aid, xaadı.split()[0], xaadı.split()[1], xyadı, xyyılı, tid, xtadı, xtyeri)
                                if (aras == 0 and byad == 0):
                                    session.run(
                                        " CREATE (a:`Araştırmacı`{aid:" + str(aid) + ", aadı:\"" + xaadı.split()[
                                            0] + " " +
                                        xaadı.split()[1] + "\",asoyadı:\"" + xaadı.split()[
                                            2] + "\"}) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"" + xyadı + "\",yyılı:\"" + xyyılı + "\"}) -[:YAYINLANIR] ->(c:`Türler`{tid:" + str(
                                            tid) + ",tadı:\"" + xtadı + "\", tyeri:\"" + xtyeri + "\"})")


                                elif (aras != 0 and byad == 0):
                                    session.run(
                                        " match(a:`Araştırmacı`{aadı:\"" + xaadı.split()[0] + " " + xaadı.split()[
                                            1] + "\",asoyadı:\"" +
                                        xaadı.split()[
                                            2] + "\"}) CREATE (a) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"" + xyadı + "\",yyılı:\"" + xyyılı + "\"}) -[:YAYINLANIR] -> (c:`Türler`{tid:" + str(
                                            tid) + ",tadı:\"" + xtadı + "\", tyeri:\"" + xtyeri + "\"})")

                                elif (aras == 0 and byad != 0):
                                    session.run(
                                        " match(b:`Yayınlar`{yadı:\"" + xyadı + "\"}) CREATE (a:`Araştırmacı`{aid:" + str(
                                            aid) + ",aadı:\"" + xaadı.split()[0] + " " + xaadı.split()[
                                            1] + "\", asoyadı:\"" + xaadı.split()[
                                            2] + "\"}) -[:YAYINLAR] -> (b)")

                                elif (a != 0 and b != 0):
                                    deneme = session.run(
                                        "MATCH (n:`Araştırmacı`{`aadı`:\"" + xaadı.split()[0] + " " + xaadı.split()[
                                            1] + "\",asoyadı:\"" + xaadı.split()[
                                            2] + "\"}) -[:YAYINLAR]->(b:Yayınlar{yadı:\"" + xyadı + "\"}) RETURN n,b ")
                                    bbb = 0
                                    for a in deneme:
                                        bbb += 1
                                    if (bbb == 0):
                                        session.run(
                                            "match(a:Araştırmacı{aadı:\"" + xaadı.split()[0] + " " + xaadı.split()[
                                                1] + "\",asoyadı:\"" + xaadı.split()[
                                                2] + "\"}), (b:Yayınlar {yadı:\"" + xyadı + "\"}) CREATE (a)-[:YAYINLAR]->(b)")
                                    elif (bbb == 1):
                                        print("Zaten YAYINLAR var")



                                else:
                                    print("Araştırmacı ID'sini kontrol ediniz...")

    nodes = session.run("MATCH (a)-[:YAYINLAR]->(m)<-[:YAYINLAR]-(b)RETURN a.aadı,b.aadı;")
    aad = []
    bad = []
    ortaklar = []
    for node in nodes:
        aad.append(dict(node)["a.aadı"])
        bad.append(dict(node)["b.aadı"])
    for i in range(len(aad)):
        tmpa = aad[i]
        tmpb = bad[i]
        for j in range(len(bad)):
            if (aad[j] == tmpa and bad[j] == tmpb and i != j):
                ortaklar.append(j)
    for i in reversed(range(len(list(dict.fromkeys(sorted(ortaklar)))))):
        aad.pop(list(dict.fromkeys(sorted(ortaklar)))[i])
        bad.pop(list(dict.fromkeys(sorted(ortaklar)))[i])

    for i in range(len(aad)):
        aaa = 0
        nodes = session.run(
            "MATCH (a:Araştırmacı {aadı:\"" + aad[i] + "\"})-[:ORTAK_ÇALIŞIR]->(b:Araştırmacı {aadı:\"" + bad[
                i] + "\"}) RETURN *")
        for node in nodes:
            aaa += 1
        if (aaa == 0):
            session.run(
                "MATCH (a:Araştırmacı {aadı:\"" + aad[i] + "\"}), (b:Araştırmacı {aadı:\"" + bad[
                    i] + "\"}) CREATE (a)-[:ORTAK_ÇALIŞIR] ->(b)")

    return render_template('xmlveri.html')

@app.route("/genelsonuc", methods=['GET', 'POST'])
def genelsonuc():
    gdb = GraphDatabase.driver(uri="neo4j+s://d0e5fa0d.databases.neo4j.io:7687",
                               auth=("neo4j", "seE64dMcF-aJ-Nv5bQqNidDzFfN4OrIolYgGm6yM2yY"))
    session = gdb.session()
    nodes = session.run("MATCH p = (a)-[r:YAYINLAR]->(b) RETURN a,b")
    tmpaadı = []
    tmpasoyadı = []
    tmpyadı = []
    tmpyyılı = []
    tmptadı = []
    tmptyeri = []
    for node in nodes:
        tmpaadı.append(dict(dict(node)['a'])['aadı'])
        tmpasoyadı.append(dict(dict(node)['a'])['asoyadı'])
        tmpyadı.append(dict(dict(node)['b'])['yadı'])
        tmpyyılı.append(dict(dict(node)['b'])['yyılı'])

    nodes = session.run("MATCH p = (a)-[r:YAYINLANIR]->(b) RETURN a,b")
    tmp2yadı = []
    tmp2yyılı = []
    tmp2tadı = []
    tmp2tyeri = []
    for node in nodes:
        tmp2yadı.append(dict(dict(node)['a'])['yadı'])
        tmp2yyılı.append(dict(dict(node)['a'])['yyılı'])
        tmp2tadı.append(dict(dict(node)['b'])['tadı'])
        tmp2tyeri.append(dict(dict(node)['b'])['tyeri'])

    for i in range(len(tmpyadı)):
        for j in range(len(tmp2yadı)):
            if (tmpyadı[i] == tmp2yadı[j]):
                tmptadı.append(tmp2tadı[j])
                tmptyeri.append(tmp2tyeri[j])

    nodes = session.run("Match (a:Araştırmacı) return a")
    tmp3aadı = []
    tmp3asoyadı = []
    for node in nodes:
        tmp3aadı.append(dict(dict(node)['a'])["aadı"])
        tmp3asoyadı.append(dict(dict(node)['a'])['asoyadı'])

    tmp4a = []
    for i in reversed(range(len(tmp3aadı))):
        for j in range(len(tmpaadı)):
            if (tmp3aadı[i] == tmpaadı[j] and tmp3asoyadı[i] == tmpasoyadı[j]):
                tmp4a.append(i)

    tmp4a = list(dict.fromkeys(tmp4a))
    for i in range(len(tmp4a)):
        tmp3aadı.pop(tmp4a[i])
        tmp3asoyadı.pop(tmp4a[i])

    for i in range(len(tmp3aadı)):
        tmpaadı.append(tmp3aadı[i])
        tmpasoyadı.append(tmp3asoyadı[i])
        tmpyadı.append("-")
        tmpyyılı.append("-")
        tmptadı.append("-")
        tmptyeri.append("-")

    aadı = request.form.get("aadı")
    asoyadı = request.form.get("asoyadı")
    yadı = request.form.get("yadı")
    yyılı = request.form.get("yyılı")

    if (aadı and asoyadı and not yadı and not yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpaadı[i] == aadı and tmpasoyadı[i] == asoyadı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (aadı and asoyadı and yadı and not yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpaadı[i] == aadı and tmpasoyadı[i] == asoyadı and tmpyadı[i] == yadı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (aadı and asoyadı and not yadı and yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpaadı[i] == aadı and tmpasoyadı[i] == asoyadı and tmpyyılı[i] == yyılı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (aadı and asoyadı and yadı and yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpaadı[i] == aadı and tmpasoyadı[i] == asoyadı and tmpyadı[i] == yadı and tmpyyılı[i] == yyılı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (aadı and not asoyadı and not yadı and not yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpaadı[i] == aadı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (aadı and not asoyadı and yadı and not yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpaadı[i] == aadı and tmpyadı[i] == yadı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (aadı and not asoyadı and not yadı and yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpaadı[i] == aadı and tmpyyılı[i] == yyılı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (aadı and not asoyadı and  yadı and yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpaadı[i] == aadı and tmpyyılı[i] == yyılı and tmpyadı[i] == yadı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (not aadı and asoyadı and not yadı and not yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpasoyadı[i] == asoyadı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (not aadı and asoyadı and yadı and not yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpasoyadı[i] == asoyadı and tmpyadı[i] == yadı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (not aadı and asoyadı and not yadı and yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpasoyadı[i] == asoyadı and tmpyyılı[i] == yyılı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (not aadı and asoyadı and yadı and yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpasoyadı[i] == asoyadı and tmpyyılı[i] == yyılı and tmpyadı[i] == yadı  ):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (not aadı and not asoyadı and yadı and yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpyadı[i] == yadı and tmpyyılı[i] == yyılı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (not aadı and not asoyadı and yadı and not yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpyadı[i] == yadı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (not aadı and not asoyadı and not yadı and yyılı):
        iaadı = []
        iasoyadı = []
        iyadı = []
        iyyılı = []
        itadı = []
        ityeri = []
        for i in range(len(tmpyadı)):
            if (tmpyyılı[i] == yyılı):
                iaadı.append(tmpaadı[i])
                iasoyadı.append(tmpasoyadı[i])
                iyadı.append(tmpyadı[i])
                iyyılı.append(tmpyyılı[i])
                itadı.append(tmptadı[i])
                ityeri.append(tmptyeri[i])
        return render_template('genelsonuc.html', count=len(iaadı), r1=iaadı, r2=iasoyadı, r3=iyadı, r4=iyyılı,
                               r5=itadı, r6=ityeri)
    elif (not aadı and not asoyadı and not yadı and not yyılı):
        return render_template('genelsonuc.html', count=len(tmpyadı), r1=tmpaadı, r2=tmpasoyadı, r3=tmpyadı,
                               r4=tmpyyılı,
                               r5=tmptadı, r6=tmptyeri)
    else:
        return render_template('genelsonuc.html', count=len(tmpyadı), r1=tmpaadı, r2=tmpasoyadı, r3=tmpyadı,
                               r4=tmpyyılı,
                               r5=tmptadı, r6=tmptyeri)


@app.route("/neodb1", methods=['GET', 'POST'])
@login_required
def neodb1():
    form = DataForm1()
    gdb = GraphDatabase.driver(uri="neo4j+s://d0e5fa0d.databases.neo4j.io:7687",
                               auth=("neo4j", "seE64dMcF-aJ-Nv5bQqNidDzFfN4OrIolYgGm6yM2yY"))
    session = gdb.session()
    error = None
    if form.validate_on_submit():
        ############ARAŞTIRMACI EKLE EĞER İSİM SOYİSİM VAR İSE EKLEME
        idnodes = session.run("match (a:`Araştırmacı`) return (a)")
        idn = 0
        for id in idnodes:
            idn += 1

        nodes = session.run(
            "match(a) where a.aadı='" + form.aadı.data + "' and a.asoyadı='" + form.asoyadı.data + "' return(a)")
        a = 0;
        for node in nodes:
            a += 1;
        if (a == 0 and int(form.aid.data) > idn):
            session.run(
                "create (a:`Araştırmacı`{aid:" + form.aid.data + ",aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"})")
            error = 'Araştırmacı Başarı ile Eklendi'
        else:
            print("Zaten Var")
            error = 'Zaten Var'
    else:
        flash('Girdiğiniz bilgileri kontrol ediniz', 'danger')
        error = 'Girdiğiniz bilgileri kontrol ediniz'
    if current_user.username == "admin" or current_user.username == "derin":
        return render_template('neodb1.html', form=form, error=error)
    else:
        return render_template('about.html')


@app.route("/neodb", methods=['GET', 'POST'])
@login_required
def neodb():
    form = DataForm()
    gdb1 = GraphDatabase.driver(uri="neo4j+s://d0e5fa0d.databases.neo4j.io:7687",
                                auth=("neo4j", "seE64dMcF-aJ-Nv5bQqNidDzFfN4OrIolYgGm6yM2yY"))
    session = gdb1.session()
    error = None
    if form.validate_on_submit():
        ############ARAŞTIRMACI VE YAYINLAR EĞER İSİM SOYİSİM VAR YAYIN ADI YOK İSE

        idnodes = session.run("match (a:`Araştırmacı`) return (a)")
        idn = 0
        for id in idnodes:
            idn += 1
        nodes = session.run(
            "match(a) where a.aadı='" + form.aadı.data + "' and a.asoyadı='" + form.asoyadı.data + "' return(a)")
        a = 0;
        for node in nodes:
            a += 1;

        ynodes = session.run("match(a) where a.yadı='" + form.yadı.data + "' return(a)")
        b = 0;
        for ynode in ynodes:
            b += 1;

        tnodes = session.run("MATCH (n:`Türler`) RETURN n")
        c = 1;
        for tnode in tnodes:
            c += 1;

        if (a == 0 and b == 0 and int(form.aid.data) > idn):
            session.run(
                " CREATE (a:`Araştırmacı`{aid:" + form.aid.data + ", aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"}) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"" + form.yadı.data + "\",yyılı:\"" + form.yyılı.data + "\"}) -[:YAYINLANIR] ->(c:`Türler`{tid:" + str(
                    c) + ",tadı:\"" + form.tadı.data + "\", tyeri:\"" + form.tyeri.data + "\"})")
            error = "Araştırmacı ve Yayın başarı ile eklendi"



        elif (a != 0 and b == 0):
            session.run(
                " match(a:`Araştırmacı`{aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"}) CREATE (a) -[:YAYINLAR] -> (b:`Yayınlar`{yadı:\"" + form.yadı.data + "\",yyılı:\"" + form.yyılı.data + "\"}) -[:YAYINLANIR] -> (c:`Türler`{tid:" + str(
                    c) + ",tadı:\"" + form.tadı.data + "\", tyeri:\"" + form.tyeri.data + "\"})")
            error = "Var olan araştırmacıya girilen yayın başarı ile eklendi"




        elif (a == 0 and b != 0 and int(form.aid.data) > idn):
            session.run(
                " match(b:`Yayınlar`{yadı:\"" + form.yadı.data + "\"}) CREATE (a:`Araştırmacı`{aid:" + form.aid.data + ",aadı:\"" + form.aadı.data + "\", asoyadı:\"" + form.asoyadı.data + "\"}) -[:YAYINLAR] -> (b)")

            nodes = session.run(
                "MATCH (a:Araştırmacı{aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"})-[:YAYINLAR]->(m)<-[:YAYINLAR]-(b) RETURN b.aadı, b.asoyadı;")
            bad = []
            basoyad = []
            ortaklar = []
            for node in nodes:
                bad.append(dict(node)["b.aadı"])
                basoyad.append(dict(node)["b.asoyadı"])

            for i in range(len(bad)):
                tmpa = bad[i]
                tmpb = basoyad[i]
                for j in range(len(bad)):
                    if (bad[j] == tmpa and basoyad[j] == tmpb and i != j):
                        ortaklar.append(j)
            for i in reversed(range(len(list(dict.fromkeys(sorted(ortaklar)))))):
                bad.pop(list(dict.fromkeys(sorted(ortaklar)))[i])
                basoyad.pop(list(dict.fromkeys(sorted(ortaklar)))[i])

            for i in range(len(bad)):
                aaa = 0
                nodes = session.run(
                    "MATCH (a:Araştırmacı {aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"})-[:ORTAK_ÇALIŞIR]->(b:Araştırmacı {aadı:\"" +
                    bad[
                        i] + "\", asoyadı:\"" + basoyad[i] + "\"}) RETURN *")
                for node in nodes:
                    aaa += 1
                if (aaa == 0):
                    session.run(
                        "MATCH (a:Araştırmacı {aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"}), (b:Araştırmacı {aadı:\"" + bad[
                            i] + "\", asoyadı:\"" + basoyad[i] + "\"}) CREATE (a)-[:ORTAK_ÇALIŞIR] ->(b)")
                    session.run(
                        "MATCH (a:Araştırmacı {aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"}), (b:Araştırmacı {aadı:\"" +
                        bad[
                            i] + "\", asoyadı:\"" + basoyad[i] + "\"}) CREATE (b)-[:ORTAK_ÇALIŞIR] ->(a)")

            error = "Var olan yayına girilen araştırmacı başarı ile eklendi"





        elif (a != 0 and b != 0):
            denemenodes = session.run("match(a:Araştırmacı{aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"})-[:YAYINLAR]->(b:Yayınlar {yadı:\"" + form.yadı.data + "\"}) return *")

            yayınlarvarmı = 0
            for node in denemenodes:
                yayınlarvarmı += 1

            if(yayınlarvarmı == 0):
                session.run(
                    "match(a:Araştırmacı{aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"}), (b:Yayınlar {yadı:\"" + form.yadı.data + "\"}) CREATE (a)-[:YAYINLAR]->(b)")

            elif(yayınlarvarmı==1):
                error="Eşleşme zaten var"

            nodes = session.run(
                "MATCH (a:Araştırmacı{aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"})-[:YAYINLAR]->(m)<-[:YAYINLAR]-(b) RETURN b.aadı, b.asoyadı;")
            bad = []
            basoyad = []
            ortaklar = []
            for node in nodes:
                bad.append(dict(node)["b.aadı"])
                basoyad.append(dict(node)["b.asoyadı"])

            for i in range(len(bad)):
                tmpa = bad[i]
                tmpb = basoyad[i]
                for j in range(len(bad)):
                    if (bad[j] == tmpa and basoyad[j] == tmpb and i != j):
                        ortaklar.append(j)
            for i in reversed(range(len(list(dict.fromkeys(sorted(ortaklar)))))):
                bad.pop(list(dict.fromkeys(sorted(ortaklar)))[i])
                basoyad.pop(list(dict.fromkeys(sorted(ortaklar)))[i])

            for i in range(len(bad)):
                aaa = 0
                nodes = session.run(
                    "MATCH (a:Araştırmacı {aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"})-[:ORTAK_ÇALIŞIR]->(b:Araştırmacı {aadı:\"" +
                    bad[
                        i] + "\", asoyadı:\"" + basoyad[i] + "\"}) RETURN *")
                for node in nodes:
                    aaa += 1
                if (aaa == 0):
                    session.run(
                        "MATCH (a:Araştırmacı {aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"}), (b:Araştırmacı {aadı:\"" +
                        bad[
                            i] + "\", asoyadı:\"" + basoyad[i] + "\"}) CREATE (a)-[:ORTAK_ÇALIŞIR] ->(b)")
                    session.run(
                        "MATCH (a:Araştırmacı {aadı:\"" + form.aadı.data + "\",asoyadı:\"" + form.asoyadı.data + "\"}), (b:Araştırmacı {aadı:\"" +
                        bad[
                            i] + "\", asoyadı:\"" + basoyad[i] + "\"}) CREATE (b)-[:ORTAK_ÇALIŞIR] ->(a)")
            error = "Var olan araştırmacı, var olan yayına eklendi"


        else:
            error = "Araştırmacı ID'sini kontrol ediniz..."
    else:
        flash('Login Unsuccessful. Please check email and password', 'danger')

    if current_user.username == "admin" or current_user.username == "derin":
        return render_template('neodb.html', form=form, error=error)
    else:
        return render_template('about.html')


@app.route("/homeadmin")
@login_required
def homeadmin():
    return render_template('homeadmin.html')


@app.route("/home")
@login_required
def home():
    return render_template('home.html')


@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.username.data == 'admin' or form.username.data == 'derin':
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, admin=1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('adminlogin'))

        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and not user.is_admin():
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('about'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for('homeadmin'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.is_admin():
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('homeadmin'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('adminlogin.html', title='Admin Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('about'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# @app.route('/delete/<id>/', methods=['GET', 'POST'])
# def delete(id):
#     alldata = User.query.get(id)
#     db.session.delete(alldata)
#     db.session.commit()
#     flash("Deleted")
#     return redirect(url_for('index'))
#
#
# @app.route('/update', methods=['GET', 'POST'])
# def update():
#     if request.method == 'POST':
#         mydata = User.query.get(request.form.get('id'))
#         mydata.username = request.form['username']
#         mydata.email = request.form['email']
#         a = request.form['password']
#         hw = bcrypt.generate_password_hash(a).decode("utf-8")
#         mydata.password = hw
#         db.session.commit()
#         flash("Updated Successfully")
#         return redirect(url_for('index'))
#
#
# @app.route('/insert', methods=['POST'])
# def insert():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#         mydata = User(username=username, email=email, password=hashed_password)
#         db.session.add(mydata)
#         db.session.commit()
#         flash("Added Successfully")
#         return redirect(url_for('index'))
#
