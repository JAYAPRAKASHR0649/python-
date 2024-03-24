import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pymongo import MongoClient
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Permanent prices for products in rupees
product_prices = {
    "Milk 1L": 60,
    "Coffee Powder 500g": 80,
    "Biscuits 1pc": 30,
    "Bread 1pc": 40,
    "Bun 1pc": 25,
    "Rice 1KG": 100,
    "Shampoo 100ML": 120,
    "Soap 1pc": 50,
    "Brush 1pc": 40,
    "Toothpaste 100gm": 35,
    "Ghee 1L": 150,
    "Butter 1pc": 70,
    "Buttermilk": 25,
    "Tomato 1KG": 20,
    "Onion 1KG": 15,
    "Potato 1KG": 45,  # Updated price for potatoes
    "Carrot 1KG": 30,
    "Beans 1KG": 35,
    "Beetroot 1KG": 40,
    "Cauliflower 1KG": 50,
    "Cabbage 1KG": 45,
    "Drumstick 1KG": 30,
    "Apple 1KG": 70,
    "Orange 1KG": 60,
    "Mango 1KG": 80,
    "Banana 1KG": 20,
    "Grapes 1KG": 100,
    "Watermelon 1KG": 40,
    "Papaya 1KG": 50,
    "Guava 1KG": 45,
    "Kiwi 1KG": 90,
    "Refined Oil 1L": 120,
    "Sunflower Oil 1L": 100,
    "Olive Oil 1L": 200,
    "Groundnut Oil 1L": 150,
    "Avocado Oil 1L": 180,
    "Pepsi 1L": 45,
    "Coca Cola 1L": 45,
    "Sprite 1L": 45,
    "Miranda 1L": 40,
    "Sting 1L": 50,
    "Bovonto 1L": 35,
    "Fruiti 1L": 30,
    "Slice 1L": 40,
    "Maaza 1L": 50,
    "Redbull 1L": 100,
    "Fizz 1L": 35,
    "Smoothie 1L": 60
}


# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['invoice_database']
collection = db['invoices']

# Function to generate PDF
def generate_pdf(data):
    file_name = f"Invoice_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    # Add store name to the PDF
    c.drawString(100, 750, "ABC Store Invoice")
    c.drawString(100, 730, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 710, f"Customer: {data['customer_name']}")
    c.drawString(100, 690, f"Phone: {data['customer_phone']}")
    c.drawString(100, 670, "Products:")
    y = 650
    for product, details in data['products'].items():
        c.drawString(120, y, f"{product}: ₹{details['price']} x {details['quantity']} = ₹{details['total']}")
        y -= 20
    c.drawString(100, y - 30, f"Total: ₹{data['total']}")
    c.save()

# Function to save data to MongoDB and generate PDF
def save_to_mongodb():
    # Get customer info from entries
    customer_name = customer_name_entry.get().strip()
    customer_phone = customer_phone_entry.get().strip()
    # Validate customer name and phone number
    if not customer_name or not customer_phone:
        messagebox.showwarning("Warning", "Please enter customer name and phone number.")
        return

    # Construct data dictionary
    data = {
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "date_time": datetime.now(),
        "products": products,
        "total": total_cost.get()
    }

    # Insert data into MongoDB
    try:
        collection.insert_one(data)
        generate_pdf(data)
        messagebox.showinfo("Success", "Invoice saved and PDF generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to reset the form
# Function to reset the form
def new_bill():
    customer_name_entry.delete(0, 'end')
    customer_phone_entry.delete(0, 'end')
    product_combobox.set('')
    category_combobox.set('')
    quantity_combobox.current(0)  # Reset quantity to default
    product_combobox['values'] = []
    product_listbox.delete(*product_listbox.get_children())  # Clear product list
    total_cost.set(0)  # Reset total cost
    products.clear()  # Clear products dictionary


# Function to update product dropdown based on selected category
def update_product_dropdown(event):
    category = category_combobox.get()
    if category == 'Daily Essentials':
        products_list = ["Milk 1L", "Coffee Powder 500g", "Biscuits 1pc", "Bread 1pc", "Bun 1pc", "Rice 1KG", "Shampoo 100ML", "Soap 1pc", "Brush 1pc", "Toothpaste 100gm", "Ghee 1L", "Butter 1pc", "Buttermilk"]
    elif category == 'Vegetables':
        products_list = ["Tomato 1KG", "Onion 1KG", "Potato 1KG", "Carrot 1KG", "Beans 1KG", "Beetroot 1KG", "Cauliflower 1KG", "Cabbage 1KG", "Drumstick 1KG"]
    elif category == 'Fruits':
        products_list = ["Apple 1KG", "Orange 1KG", "Mango 1KG", "Banana 1KG", "Grapes 1KG", "Watermelon 1KG", "Papaya 1KG", "Guava 1KG", "Kiwi 1KG"]
    elif category == 'Oil':
        products_list = ["Refined Oil 1L", "Sunflower Oil 1L", "Olive Oil 1L", "Groundnut Oil 1L", "Avocado Oil 1L"]
    elif category == 'Beverages':
        products_list = ["Pepsi 1L", "Coca Cola 1L", "Sprite 1L", "Miranda 1L", "Sting 1L", "Bovonto 1L", "Fruiti 1L", "Slice 1L", "Maaza 1L", "Redbull 1L", "Fizz 1L", "Smoothie 1L"]
    else:
        products_list = []
    product_combobox['values'] = products_list


# Function to add product to the list
def add_product():
    product = product_combobox.get().strip()
    quantity = quantity_combobox.get()  # Get the selected quantity
    if product:
        price = product_prices.get(product, 0)  # Get the price from the dictionary
        total_price = price * int(quantity)
        products[product] = {'price': price, 'quantity': int(quantity), 'total': total_price}
        product_listbox.insert('', 'end', values=(product, price, quantity, total_price))
        total_cost.set(sum(detail['total'] for detail in products.values()))

# GUI setup
root = tk.Tk()
root.title("Bill Invoice Maker")
root.geometry("800x600")  # Set the window size
root.configure(bg='#E6E6FA')  # Set background color

# Store Name
store_name_label = ttk.Label(root, text="ABC Store", font=('Helvetica', 24, 'bold'), background='#E6E6FA')
store_name_label.pack(pady=10)

# Customer info
customer_frame = ttk.Frame(root)
customer_frame.pack(padx=10, pady=10)

ttk.Label(customer_frame, text="Customer Name:").grid(row=0, column=0, padx=5, pady=5)
customer_name_entry = ttk.Entry(customer_frame)
customer_name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(customer_frame, text="Phone Number:").grid(row=1, column=0, padx=5, pady=5)
customer_phone_entry = ttk.Entry(customer_frame)
customer_phone_entry.grid(row=1, column=1, padx=5, pady=5)

# Category and Product info
product_frame = ttk.Frame(root)
product_frame.pack(padx=10, pady=10)

ttk.Label(product_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
category_combobox = ttk.Combobox(product_frame, values=["Daily Essentials", "Vegetables", "Fruits", "Oil", "Beverages"])
category_combobox.grid(row=0, column=1, padx=5, pady=5)
category_combobox.bind("<<ComboboxSelected>>", update_product_dropdown)

ttk.Label(product_frame, text="Product:").grid(row=0, column=2, padx=5, pady=5)
product_combobox = ttk.Combobox(product_frame)
product_combobox.grid(row=0, column=3, padx=5, pady=5)

# Quantity info
ttk.Label(product_frame, text="Quantity:").grid(row=0, column=4, padx=5, pady=5)
quantity_combobox = ttk.Combobox(product_frame, values=[str(i) for i in range(1, 11)])  # Scale from 1 to 10
quantity_combobox.grid(row=0, column=5, padx=5, pady=5)
quantity_combobox.current(0)  # Set default quantity to 1

add_button = ttk.Button(product_frame, text="Add Product", command=add_product)
add_button.grid(row=0, column=6, padx=5, pady=5)

# Product list
product_listbox = ttk.Treeview(root, columns=('Product', 'Price', 'Quantity', 'Total Price'))
product_listbox.pack(padx=10, pady=10)
product_listbox.heading('Product', text='Product')
product_listbox.heading('Price', text='Price')
product_listbox.heading('Quantity', text='Quantity')
product_listbox.heading('Total Price', text='Total Price')

# Total cost
total_cost = tk.IntVar()
ttk.Label(root, text="Total Cost:").pack(pady=5)
ttk.Entry(root, textvariable=total_cost, state='readonly').pack()

# Save and New Bill Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

save_button = ttk.Button(button_frame, text="Save", command=save_to_mongodb)
save_button.grid(row=0, column=0, padx=5)

new_bill_button = ttk.Button(button_frame, text="New Bill", command=new_bill)
new_bill_button.grid(row=0, column=1, padx=5)

# Initialize product dictionary
products = {}

root.mainloop()

