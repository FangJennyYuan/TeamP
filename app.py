from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__) #create the Flask app

when = "global"
data = "global"

def connect(time):
    ''""" Connect to the PostgreSQL database server """
    localhost = "findmyspot.cmpdtcyalbuc.us-west-2.rds.amazonaws.com"
    dbname = "TeamP"
    username = "TeamP"
    userpsw = "teampteamp"

    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=localhost, database=dbname, user=username, password=userpsw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('Top 10 spots near Capitol Hill: ')
        cur.execute("SELECT * from top10spots(%s);", (time,))

        # display the PostgreSQL database server version
        db_version = cur.fetchall()
        coords = []
        for i in range(len(db_version)):
            coordz = db_version[i][4].split("POINT (", 2)[1].split(" ")
            lat = coordz[0]
            long = coordz[1].split(")")[0]
            latlong = [lat, long]
            coords.append(latlong)
        # return render_template("index.html", name=top20)
        return coords
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)



@app.route("/", methods=['GET', 'POST']) #allow both GET and POST requests
def home():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        when = request.form.get('when')
        #what = request.form['']
        #print(what)
        coords = connect(when)
        return render_template("Map.html", lat1=coords[0][0], long1=coords[0][1],
                               lat2=coords[1][0], long2=coords[1][1], lat3=coords[2][0], long3=coords[2][1],
                               lat4=coords[3][0], long4=coords[3][1], lat5=coords[4][0], long5=coords[4][1],
                               lat6=coords[5][0], long6=coords[5][1], lat7=coords[6][0], long7=coords[6][1],
                               lat8=coords[7][0], long8=coords[7][1], lat9=coords[8][0], long9=coords[8][1],
                               lat10=coords[9][0], long10=coords[9][1])

    return '''<form method="POST">
                      Hello! Wondering where there may be parking spots near Seattle U? What time?<br>
                      <select name="when">
                          <option value="8">8 am</option>
                          <option value="9">9 am</option>
                          <option value="10">10 am</option>
                          <option value="11">11 am</option>
                          <option value="12">12 pm</option>
                          <option value="13">1 pm</option>
                          <option value="14">2 pm</option>
                          <option value="15">3 pm</option>
                          <option value="16">4 pm</option>
                          <option value="17">5 pm</option>
                          <option value="18">6 pm</option>
                          <option value="19">7 pm</option>
                          <option value="20">8 pm</option>
                          <option value="21">9 pm</option>
                    </select>
                      <br><br><input type="submit" id="closest" value="Show Closest Spots"><br><br>
                      <input type="submit" id="best" value="Show Best Spots"><br>
                  </form>'''


if __name__ == "__main__":
    app.run(debug=True)

#http://127.0.0.1:5000/
