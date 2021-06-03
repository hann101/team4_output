from .myspark import spark as spark
from pyspark.sql import functions as F
import re
import pandas as pd
import pymysql

def main1(search):

    # 이미지 경로 검색
    @F.udf()
    def image_tag(x,a,b,c,search):
        # 검색어가 개인정보에 있을 때
        if (search in a) or (search in b) or (search in c) :
            path_list = []
            p = re.compile('({)(.*?)(})')
            m = p.findall(x)
            for i in range(len(m)):
                image_info = m[i][1]
                # print(m[i][1])
                # 검색어가 개인정보에도 있고 이미지 태그에도 있을 때
                if search in image_info:
                    temp = image_info.split(',')[0]
                    image_path = temp.split(':')[1]
                    #print(image_path)
                    path_list.append(image_path)
                temp = image_info.split(',')[0]
                image_path = temp.split(':')[1]
                #print(image_path)
                path_list.append(image_path)
            return set(path_list) #중복 이미지경로 제거
        else:
            # 검색어가 이미지 태그에만 있을 때
            path_list = []
            p = re.compile('({)(.*?)(})')
            m = p.findall(x)
            for i in range(len(m)):
                image_info = m[i][1]
                if search in image_info:
                    temp = image_info.split(',')[0]
                    image_path = temp.split(':')[1]
                    # print(image_path)
                    path_list.append(image_path)
                else:
                    pass
            if len(path_list) <1:
                #검색어에 해당하는 이미지 없을 때, null값 넣기 
                return None
            else:
                return set(path_list)

    #개인정보 DB 조회
    conn = pymysql.connect(host='mybide.cutyxjtrt78p.us-east-1.rds.amazonaws.com', user='admin', password='wqend1001', port=3306, db='login', charset='utf8')
    cursor = conn.cursor()

    query = "SELECT * FROM level1"
    cursor.execute(query)
    conn.commit()

    pymysql.install_as_MySQLdb()

    df = pd.read_sql_query(query,conn)
    df = spark.createDataFrame(df)

    df1 = spark.read.csv('image_data.csv',header=True)

    df = df.join(df1,on=['id'],how='inner')
    df = df.withColumn('image',image_tag(F.col('image'),F.col('age'),F.col('sex'),F.col('address'),F.lit(search)))
    df = df.drop("_id") #id
    df = df.filter(F.col('image').isNotNull())

    # image_path 리스트로 출력
    result_pdf=df.select("*").toPandas()
    image_list = []
    for string_path in result_pdf['image'] :
        p = re.compile("(')(.*?)(')")
        m = p.findall(string_path)
        for i in range(len(m)):
            image_list.append(m[i][1])

    print('\nlevel 1 success\n')   

    return image_list
    #ex ['test1.png', 'test11.png']
