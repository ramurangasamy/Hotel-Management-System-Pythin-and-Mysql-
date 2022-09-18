from tabulate import tabulate

#MYSQL CONNECTION 
import mysql.connector
con = mysql.connector.connect(
  host="localhost",
  user="root",
  password="priyaramu",
  database="fooddb"
)
res =con.cursor()

#MYSQL QUERY
"""
create database fooddb;
use fooddb; 
# drop table foods;
CREATE TABLE foods (
	id	int primary key auto_increment,
	name varchar(52) NOT NULL UNIQUE,
	quantity int,
	price float
);
"""

def insert(name,quantity,price):
    sql="insert into foods(name,quantity,price) values(%s,%s,%s)"
    data=(name,quantity,price)
    res.execute(sql,data)
    con.commit()
    print(f"New Food Item {name} Added Successfully")

def delete(id):
    sql="delete from foods where id=%s"
    res.execute(sql,(id,))
    con.commit()
    print(f"Food Item {id} Deleted Successfully")

def show():
    sql="select*from foods"
    res.execute(sql)
    result=res.fetchall()
    print(tabulate(result,headers=["ID","NAME","QUANTITY","PRICE"]))

def update(quantity,price,id):
    sql="update foods set quantity=%s,price=%s where id=%s"
    data=(quantity,price,id)
    res.execute(sql,data)
    con.commit()
    print(f"Food Item {id} Updated Successfully")

def placeorder(cart):
    print('\n')
    total_price=0
    n=len(cart)
    food_cart=[]
    for i in range(n):
        item_id=int(cart[i][0])
        order_item_quantity=int(cart[i][1])
        sql="select name,price,quantity from foods where id=%s"
        data=(item_id,)
        res.execute(sql,data)
        result=res.fetchone()
        food_name=str(result[0])
        food_price=float(result[1])
        food_quantity=int(result[2])
        data=(item_id,food_name,food_price,food_quantity,order_item_quantity)
        food_cart.append(data)

    order_len=len(food_cart)
    order_summery=[]
    for j in range(order_len):
        order_item_id=int(food_cart[j][0])
        order_item_name=str(food_cart[j][1])
        order_item_price=float(food_cart[j][2])
        total_item_quantity=int(food_cart[j][3])
        order_item_quantity_count=int(food_cart[j][4])
        if order_item_quantity_count<=total_item_quantity:
            total_price_per_item=order_item_quantity_count*order_item_price
            new_quantity=total_item_quantity-order_item_quantity
            total_price+=total_price_per_item
            update_query="update foods set quantity=%s where id=%s"
            update_data=(new_quantity,order_item_id)
            res.execute(update_query,update_data)
            con.commit()
            order_summery.append(f"{order_item_name} : Rs.{order_item_price} X {order_item_quantity_count} = {round(total_price_per_item,2)}")
        elif(order_item_quantity_count>total_item_quantity):
            order_summery.append(f"Quantity More,Availabe item is {total_item_quantity}")
        else:
            print("Something Went Wrong! Try Again")
  
    print("--------------------------------------------------------")
    print("                      ORDER SUMMARY                     ") 
    print("--------------------------------------------------------")       
    print("########################################################")
    for datal in order_summery:
        print(datal)
    print("--------------------------------------------------------")    
    print(f"Order Placed Successfully and Total Amount is {round(total_price,2)}")
    print("########################################################")
 
food_info="""
--------------------
  FOOD ORDER SYSTEM
--------------------
1.List Food Items
2.Update Food Items
3.Add Food Items
4.Delete Food Items
5.Place Order
6.Exit
"""

while True:
    print(food_info)
    ch=int(input("Enter Your Choice : "))
    if(ch==1):
        print("-----------------------------------------")
        print("            All Food Items Menu          ")
        print("-----------------------------------------")
        show()
    elif(ch==2):
        f_id=int(input("Enter Food Item ID : "))
        f_price=float(input("Enter Item Price : "))
        f_quantity=int(input("Enter Item Quantity : "))
        update(f_quantity,f_price,f_id)
    elif(ch==3):
        f_name=input("Enter New Food Item Name : ")
        f_price=float(input("Enter New Food Item Price : "))
        f_quantity=int(input("Enter New Food Item Quantity : "))
        insert(f_name,f_quantity,f_price)
    elif(ch==4):
        f_id=int(input("Enter Food Item ID : "))
        delete(f_id)
    elif(ch==5):
        cart=[]
        n=int(input("How Many Items You Want To Place : "))
        for i in range(n):
            item_id=int(input("Enter Item ID : "))
            order_quantity=int(input("Enter Quantity : "))    
            data=(item_id,order_quantity)
            cart.append(data)
        placeorder(cart)
    elif(ch==6):
        exit()
    else:
        print("Something Went Wrong! Try Again")