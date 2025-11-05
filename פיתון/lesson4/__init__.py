def countWord(p):
    count=0
    with open(p,'r') as file:
        content = file.read()
        words=content.split()
        return len(words)


print(countWord('a.txt'))

# ex2
import csv

def People(people_list):
    with open('people.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['First Name', 'Last Name', 'Age', 'Place of Residence'])
        writer.writerow(people_list)




people_list = [
    ['John', 'Doe', 30, 'New York'],
    ['Jane', 'Smith', 25, 'Los Angeles'],
    ['Peter', 'Jones', 45, 'Chicago'],
    ['Alice', 'Williams', 35, 'Houston']
]
People(people_list)
# ex3
import  json
def Data(data):
    with open("data.json", 'w') as f:
        json.dump(data, f,)
    with open("data.json", 'r') as f2:
        read_data = json.load(f2)
    print(read_data)


data = {
        "product": "Laptop",
        "price": 1200.50,
        "in_stock": True
    }
Data(data)
