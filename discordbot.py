from discord.ext import commands
import os
import traceback
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials



token = os.environ['DISCORD_BOT_TOKEN']




client = discord.Client()

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet-test-325817-6abf40d4b607.json', scope)

gc = gspread.authorize(credentials)

SPREADSHEET_KEY = '1IX9Lw4nsTnxc6g2YlDQNIOJ35D_zL3pqdfudOEOpqSI'
workbook = gc.open_by_key(SPREADSHEET_KEY)

def monthcheck():
    worksheet_list = workbook.worksheets()              #ワークシートの一覧を取得
    today = datetime.date.today().strftime('%Y%m')    #今日の日付を取得し文字列の形で記録する
    exist = False
    for current in worksheet_list :
        if current.title == today :
            exist = True                                #今月の分のシートがあればフラグを立てる
    if exist == False :                                 #今月の分のシートがなければここで作成する
         workbook.add_worksheet(title=today, rows = 100, cols = 4)      #余裕を持って行数は100行、幅は4行のシートを新規作成する
         newsheet = workbook.worksheet(today)           #作成したシートの初期値を設定する
         newsheet.update('A1','収入')
         newsheet.update('C1','支出')
    return workbook.worksheet(today)                #作成したシートを戻り値として返す。

def add_income(worksheet, name, amount):#引数で受け取ったシートに引数で受け取った収入を記録する関数
    lists = worksheet.get_all_values()  #シートの内容を配列で取得
    rows = len(lists) + 1               #入力されているデータの数を取得し、末端に書き込むときのインデックスとして利用する為+1する
    worksheet.update_cell(rows,1,name)  #引数で受け取った名前をセルに入力
    worksheet.update_cell(rows,2,amount)#引数で受け取った金額をセルに入力
    
def add_spending(worksheet, name, amount):#引数で受け取ったシートに引数で受け取った支出を記録する関数
    lists = worksheet.get_all_values()  #シートの内容を配列で取得
    rows = len(lists) + 1               #入力されているデータの数を取得し、末端に書き込むときのインデックスとして利用する為+1する
    worksheet.update_cell(rows,3,name)  #引数で受け取った名前をセルに入力
    worksheet.update_cell(rows,4,amount)#引数で受け取った金額をセルに入力

def check_total(worksheet):             #引数で受け取ったシートに収支の合計を記録する関数
    lists = worksheet.get_all_values()  #シートの内容を配列で取得
    rows = len(lists)                   #入力されているデータの数を取得
    worksheet.update('B1','=SUM(B2:B'+str(rows)+')',value_input_option='USER_ENTERED')  #SUM関数を用いて収入の合計をセルに入力
    worksheet.update('D1','=SUM(D2:D'+str(rows)+')',value_input_option='USER_ENTERED')  #SUM関数を用いて支出の合計をセルに入力

    today = datetime.date.today().strftime('%Y/%m')          #今日の日付を取得し文字列の形で記録する
    con_worksheet = workbook.worksheet('まとめ')                    #記録をまとめているシートを取得する
    conclusion = con_worksheet.get_all_values()
    exist = False
    index = 1
    for day in conclusion :                                     #まとめに今月の分の記載があるかを確認する
        if day[0] == today :
            exist = True
            break
        index = index + 1
   
    if exist == False :                                         #記載がなければ、末端に追加する準備をする
        index = len(conclusion) + 1
        con_worksheet.update_cell(index,1,today)
            
    con_worksheet.update_cell(index,2,worksheet.acell('B1').value)
    con_worksheet.update_cell(index,3,worksheet.acell('D1').value)

    conclusion = con_worksheet.get_all_values()                 #まとめが記載し終わった後のシートの要素数を確認する
    con_rows = len(conclusion) 
    
    con_worksheet.update('B2','=SUM(B3:B'+str(con_rows)+')',value_input_option='USER_ENTERED')  #SUM関数を用いて収入の合計をセルに入力
    con_worksheet.update('C2','=SUM(C3:C'+str(con_rows)+')',value_input_option='USER_ENTERED')  #SUM関数を用いて支出の合計をセルに入力
    return

def check_income(worksheet):            #引数で受け取ったシートの収入合計を返す関数
    return worksheet.acell('B1').value  #受け取ったワークシートの収入合計の部分を返す

def check_spending(worksheet):          #引数で受け取ったシートの支出合計を返す関数
    return worksheet.acell('D1').value  #受け取ったワークシートの支出合計の部分を返す

@client.event
async def on_message(message):          #メッセージを受け取ったときの挙動
    if message.author.bot :             #拾ったメッセージがBotからのメッセージだったら(=Bot自身の発言だったら弾く)
        return

    #if type(message.channel) == discord.DMChannel : #受け取ったメッセージがDMであることを確認する(置いてあるサーバーでむやみに動かないようにする)

    worksheet = monthcheck()

    if message.content == 'シート' :
            await message.channel.send('https://docs.google.com/spreadsheets/d/******************************************/edit?usp=sharing')
            return
    if message.content == '今月の収入' :         #収入の確認だったら取得し返信して処理を閉じる
            await message.channel.send('今月の収入は'+str(int(check_income(worksheet)))+'円です。')
            return
            
    if message.content == '今月の支出' :         #支出の確認だったら取得し返信して処理を閉じる
            await message.channel.send('今月の支出は'+str(int(check_spending(worksheet)))+'円です。')
            return

    receipt = message.content.split(',')

    if len(receipt) != 3 :                      #支出、収入の入力がフォーマットに沿ってなかったら弾く
            await message.channel.send('入力が無効')
            return
    receipt[2] = receipt[2].replace('円','')     #金額に円と付いてたらその部分を取り除く
    if receipt[0] == '収入' :
            add_income(worksheet,str(receipt[1]),int(receipt[2]))   #収入を書き込む
            check_total(worksheet)  #収支の合計をチェックし入力させる
            await message.channel.send(''+receipt[1]+'による収入'+receipt[2]+'円を記録しました。\r\n記録後の今月の収入は'+str(int(check_income(worksheet)))+'円です。')
            return
    elif receipt[0] == '支出' :
            add_spending(worksheet,str(receipt[1]),int(receipt[2]))   #収入を書き込む
            check_total(worksheet)  #収支の合計をチェックし入力させる
            await message.channel.send(''+receipt[1]+'による支出'+receipt[2]+'円を記録しました。\r\n記録後の今月の支出は'+str(int(check_spending(worksheet)))+'円です。')
            return
    else :
            await message.channel.send('入力が無効')
            return

client.run(TOKEN)



    

