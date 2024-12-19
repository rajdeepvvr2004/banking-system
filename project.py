import urllib.parse
import webbrowser

import random
otp=random.randint(100000,999999)
import smtplib
email="godwrestle49@gmail.com"
email=email.strip()
message=f"{otp}"
import urllib.parse

def generate_upi_link(upi_id, payee_name, amount):
    """
    Generates a UPI payment link with given details.
    """
    # Encode special characters to make the URL valid
    upi_link = f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(payee_name)}&am={amount}&cu=INR"
    return upi_link
try:
    text=f"{message}"
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email,"rlfv btzv xsio xqdq")
except:
     print("please check if your system is connected to internet")    

import time

ctime=time.strftime("%H:%M:%S")
date=time.strftime("%d/%m/%y")
# import random
engine=random.randint(10000000,99999999)

import mysql.connector as sql
conn= sql.connect(
   host="localhost",
   user="root",
   password="raj123",
   database="raj"  
       )
cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bank_account (
accountno varchar(30) unique,
username varchar(20) ,
balance int,
password  varchar(20)unique,
gmail varchar(30) unique

);
""")
conn.commit()
print("Database and table are ready.")



while True:
    print("Do you want to sign in or sign up?")
    d1=int(input("enter 1 for sign in               enter 2 for sign up  :  "))
    if d1 == 1:
                
                unam= input("Enter your username: ")
                unam=unam.strip()
                passwo = input("Enter your password: ")
                passwo=passwo.strip()
                
                cursor = conn.cursor()
                select_query = "select *  from bank_account ;"
                cursor.execute(select_query)
                
                rows = cursor.fetchall()
                row=list(rows)
                for r in row:
                    if((passwo in r and unam not in r) or (unam in r and passwo not in r) ):
                        print("username or password you entered was incorrect ")
                        print("do you want to know your username and password")
                        print("the password you entered was incorrect ")
                        print("do you want to know your password")
                        resetp=(input("enter 1 if you want to reset your password :          enter 2 if you want to reset your username : "))
                        resetp=resetp.strip()
                        if resetp=="1":
                            em=input("enter your email")
                            em=em.strip()
                            if em in r:
                                server.sendmail(email,em,text)
            
                            em=em.strip()
                            if em in r:
                                server.sendmail(email,em,text)
                                ottp=input("enter the otp we sent to your mail")
                                ottp=ottp.strip()
                                if ottp==message:
                                    print(f"your password is {r[3]}")
                                    break
                            else:
                                print("please enter a valid mail id")
                                break
                                    
                        elif resetp=="2":
                            em=input("enter your email")                 
                            ottp=input("enter the otp we sent to your mail")
                            ottp=ottp.strip()
                            if ottp==message:
                                    print(f"your username is {r[1]}")
                                    break
                            else:
                                print("sorry email is invalid")
        
            
                    elif unam in r and passwo in r:
                        print("Access granted")
                        while True:
                            print(f"Account number: {r[0]}, Account holder: {r[1]}, Balance: {r[2]}")
                            choice = int(input("Enter 1 for withdrawal, 2 for deposit, 3 to quit ,enter 4 for checking your transaction history , \nenter 5 if you want to change your pin :"))
                            if choice == 1:
                                withdrawal = int(input("Enter the amount to withdraw: "))
                                if withdrawal <= r[2]:
                                        reciever=r[4]
                                        reciever=reciever.strip()
                                        try:
                                         server.sendmail(email,reciever,text)
                                        except:
                                             print("you dont have proper internet connection") 
                                        print("otp has been sent")
                                        ottp=(input("enter the otp that we have sent to your mail : "))
                                        ottp=ottp.strip()
                                        if ottp==message:
                                            new_balance = r[2] - withdrawal
                                            update_query = "UPDATE bank_account SET balance = %s WHERE username = %s;"
                                            cursor.execute(update_query,(new_balance,unam))
                                            conn.commit()
                                            print(f"Balance updated. Current balance: {new_balance}")
                                            f=open(f"{unam}",'a')
                                            f.write(f"{ctime}          you withdrew {withdrawal} rupees.avaliable balance ={new_balance}            {date}\n")
                                            f.close()
                                        else:
                                            print("please enter correct otp and try again")
                                            break


                                else:
                                  print("Insufficient balance!")
                                  break
                            
                            elif choice == 2:
                                deposit = int(input("Enter the amount to deposit: "))
                                reciever=r[4]
                                reciever=reciever.strip()
                                server.sendmail(email,reciever,text)
                                print("otp has been sent")

                                ottp=(input("enter the otp that we have sent to your mail : "))
                                ottp=ottp.strip()
                                if ottp==message:

                                    # Generate UPI payment link
                                    upi_id = "rajdeep.s1874-1@oksbi"  # Your UPI ID
                                    payee_name = "Rajdeep Singh"      # Your name
                                    upi_link = generate_upi_link(upi_id, payee_name, deposit)

                                    print("\nPlease use the following link to complete the payment:")
                                    print(upi_link)
                                    
                                    # Optional: Open the UPI link in the browser
                                    import webbrowser
                                    webbrowser.open(upi_link)

                                    # Confirm the payment manually
                                    confirmation = input("Enter 'yes' if the payment is successful: ").strip().lower()
                                    if confirmation == "yes":
                                        # Update database with deposit amount
                                        new_balance = r[2] + deposit
                                        update_query = "UPDATE bank_account SET balance = %s WHERE username = %s"
                                        cursor.execute(update_query, (new_balance, unam))
                                        conn.commit()

                                        print(f"Payment successful! Balance updated. Current balance: {new_balance}")
                                        
                                        # Log the transaction
                                        with open(f"{unam}", 'a') as f:
                                            f.write(f"{ctime}  You deposited {deposit} rupees. Available balance = {new_balance}  {date}\n")
                                        
                                        # Send email confirmation
                                        try:
                                            reciever = r[4].strip()
                                            server.sendmail(email, reciever, f"Payment of {deposit} INR was successful.\nNew Balance: {new_balance}")
                                            print("Confirmation email sent.")
                                        except:
                                            print("Failed to send email confirmation.")
                                    else:
                                        print("Payment not confirmed. Please try again.")

                                    new_balance = r[2] + deposit
                                    update_query = "UPDATE bank_account SET balance = %s WHERE username= %s"
                                    cursor.execute(update_query,(new_balance,unam))
                                    conn.commit()
                                    print(f"Balance updated. Current balance: {new_balance}")
                                    f=open(f"{unam}",'a')
                                    f.write(f"{ctime}          you deposited {deposit} rupees.avaliable balance ={new_balance}          {date}\n")
                                    f.close() 
                                    break
                            elif choice == 3:
                                    print("Thank you!")
                                    break
                            elif choice==4:
                                    f=open(f"{unam}","r")
                                    c=f.read()
                                    print(c)
                                    reciever=r[4]
                                    reciever=reciever.strip()
                                    server.sendmail(email,reciever,c)
                                    break
                            elif choice ==5:
                                 upin=input("enter your current pin")
                                 upin=upin.strip()
                                 if upin==passwo:
                                      reciever=r[4]
                                      reciever=reciever.strip()
                                      server.sendmail(email,reciever,text)
                                      otttp=input("enter the otp sent to yoiur mail")
                                      otttp=otttp.strip()
                                      if otttp==message:
                                        newpin=input("enter new pin")
                                        newpin=newpin.strip()
                                        query="update bank_account set password=%s where username= %s"
                                        cursor.execute(query,(newpin,unam))
                                        conn.commit()
                                        print("done successfully")
                                 else:
                                      print("enter correct pin")
                                      break
                                       
                            else:
                              print("Invalid username or password")
            # except:
            #     print("Please enter valid options")

    elif d1 == 2:
            a1="savings account"
            a2="current account"
            a3="zero balance account"
            b="row"
            while True:
                print("enter the type of account you want to open")
                type=input("enter 1 for savings(minimum balance =500),  2 for current account(minimum bal=50,000),\n  3 for zero bal account(minimum bal=0) : ")
                type=type.strip()
                cursor = conn.cursor()
                select_query = "SELECT * FROM bank_account"
                cursor.execute(select_query)
                rows = cursor.fetchall()
                row=list(rows)
                query='''delete from bank_account where gmail="row";'''
                cursor.execute(query)
                conn.commit()
                
                uname = "row"
                uname=uname.strip()
                password = "ro"
                password=password.strip()
                password=str(password)
                gmail="row"
                account_no=engine
                balance=0
                if type=="1":
                    query = "INSERT INTO bank_account VALUES (%s,%s,%s,%s,%s);"
                    cursor.execute(query,(account_no, uname, balance, password,gmail))
                    print("Successfully registered!")
                elif type=="2":
                    query = "INSERT INTO bank_account VALUES (%s,%s,%s,%s,%s);"
                    cursor.execute(query,(account_no,uname,balance,password,gmail))
                    conn.commit()
                    print("Successfully registered!")
                elif type=="3":
                    query = "INSERT INTO bank_account VALUES (%s,%s,%s,%s,%s);"
                    cursor.execute(query,(account_no,uname,balance,password,gmail))
                    conn.commit()
                    print("Successfully registered!")
                    
                try:
                    u=input("please enter your username : ")
                    u=u.strip()
                    query="update bank_account set username =%s where username = %s;"
                    cursor.execute(query,(u,uname))
                    conn.commit()
                    print("done")


                except:
                        print("please enter a valid value")
                        query=''' delete from bank_account where gmail="row";'''
                        cursor.execute(query)
                        conn.commit()
                        break
            
                try:
                    p=input("please enter your password : ")
                    p=p.strip() 
                    query="update bank_account set password = %s where password = %s;"
                    cursor.execute(query,(p,password))
                    conn.commit()
                    print("done")  
                except:
                    print("sorry this password already exists please try a different one")
                    query=''' delete from bank_account where gmail="row";'''
                    cursor.execute(query)
                    conn.commit()
                    break
                    
                ba=int(input("enter the balance you want to deposit"))
                if type=="1" and ba<500:
                                    print("sorry minimum balnce to be maintained is 500")
                                    query=f'''delete from bank_account where password="{p}"'''
                                    cursor.execute(query)
                                    conn.commit()
                elif type =="2" and ba<50000:
                                    print("sorry minimum balance to be maintained is 50,000")
                                    query=f'''delete from bank_account where password="{p}"'''
                                    cursor.execute(query)
                                    conn.commit()
                elif(type=="3" and ba<0):
                                    print("minimum balance is 0")
                                    query=f'''delete from bank_account where password="{p}"'''
                                    cursor.execute(query)
                                    conn.commit()


                else:
                    query="update bank_account set balance = %s where balance = %s;"
                    cursor.execute(query,(ba,balance))
                    conn.commit()
                    print("done") 
            





















                try:
                    g=input("please enter your gmail id : ")
                    g=g.strip()
                    for r in row:
                         if g in r:
                              print("sorry this gmail already exists")
                              break
                         else:   
                            reciever=g
                            server.sendmail(email,reciever,text)
                            ottp=input("please enter the otp we have sent to your mail: ")
                            ottp=ottp.strip()
                            if ottp==message:
                                query="update bank_account set gmail = %s where gmail = %s;"
                                cursor.execute(query,(g,gmail))
                                conn.commit()
                                print("done")
                                
                                
                            else:
                                print("you have entered incorrect otp") 
                                query=''' delete from bank_account where gmail="row";'''
                                cursor.execute(query)
                                conn.commit()
                                break
                        
                except:
                    print("sorry but his gmail id already exists")
                    query=''' delete from bank_account where gmail="row";'''
                    cursor.execute(query)
                    conn.commit()
                    break
                
        


