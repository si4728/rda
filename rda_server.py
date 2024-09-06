import paho.mqtt.client as mqtt
import time
import mysql.connector
from mysql.connector import Error
import json

# 클래스의 인스턴스 생성
my_instance = MyClass(parameter1_value, parameter2_value)

# MQTT Broker 정보
broker_address = "localhost"
broker_port = 1883

# Subscribe Topic
rda_request = "rda/iot/query"  #request/demo"

# Publish Topic
rda_response = "rda/iot/response"  #response/demo"

rda_db_name = "nplt"
rda_db_host = "localhost"
rda_db_user = "root"
rda_db_password = "P@ssw0rd!@#$"
rda_db_port ="3306"

def execute_query(sql):
    connection = mysql.connector.connect(host=rda_db_host,
                                            port=rda_db_port,
                                            database=rda_db_name,
                                            user=rda_db_user,
                                            password=rda_db_password)
    cursor = connection.cursor()
    try:

        cursor.execute(sql)

        if "SELECT" in sql.upper():
            field_names = [column[0] for column in cursor.description]
            print(f"Selected field names: {field_names}")
            field_values = cursor.fetchall()
            result={"error":0, "fields":field_names, "data":field_values}                  
        else:
            connection.commit()  # 0="Query executed successfully."
            result={"error":"0", "fields":"", "data":""}    

    except mysql.connector.Error as error:
        return {"error":error, "fields":"", "data":""}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()    
    return result

# Callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(rda_request)

def on_message(client, userdata, msg):
    print(f"\nReceived message on topic {msg.topic}: {str(msg.payload)}")
    sqlString = msg.payload.decode('utf-8') # query 문자열 획득
    result = execute_query(sqlString)  # Query 실행
    result_json_str = json.dumps(result, default=str) # 경과 json으로 저장
    client.publish(rda_response, result_json_str) # 수행결과 값 Publish
    
# MQTT instance 
client = mqtt.Client()

# callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to Broker
client.connect(broker_address, broker_port, 60)

# Start the loop
client.loop_start()

try:
    while True:
        message = str(input("If Input CTRL + C then this program terminate "))

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
    print("Disconnected.")
