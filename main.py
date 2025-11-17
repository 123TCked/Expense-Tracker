import json
import os
import argparse
from datetime import datetime

# -------------------------- load/save --------------------------

def load_expense():
    if not os.path.exists("expenses.json"):
        return []
    with open("expenses.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_expense(expenses):
    with open("expenses.json", "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii= False, indent=4)

# -------------------------- 功能函数 --------------------------

def add_expense(description, amount):
    expenses = load_expense()
    new_id = expenses[-1]["ID"] + 1 if expenses else 1
    new_expense = {
        "ID": new_id,
        "Description": description,
        "Amount": float(amount),
        "Date": datetime.now().strftime("%Y-%m-%d")
    }
    expenses.append(new_expense)
    save_expense(expenses)
    print(f"已添加费用：{new_expense}")

def update_expense(id, new_description, new_amount):
    expenses = load_expense()
    found = False
    for e in expenses:
        if e["ID"] == id:
            e["Description"] = new_description
            e["Amount"] = float(new_amount)
            found = True
            break
    if found:
        save_expense(expenses)
        print(f"已更新ID={id}的费用->描述: {new_description}  金额: {new_amount}")
    else:
        print(f"未找到ID为{id}的费用")

def delete_expense(id):
    expenses = load_expense()
    found = False
    delete_item = None
    for e in expenses:
        if e["ID"] == id:
            found = True
            delete_item = e
            break
    if found:
        expenses.remove(delete_item)
        save_expense(expenses)
        print(f"已删除费用: {delete_item}")
    else:
        print(f"未找到ID为{id}的费用")

def list_expenses():
    expenses = load_expense()
    if not expenses:
        print("暂无任何费用记录")
        return
    print("当前所有费用：")
    print("-" * 40)
    for e in expenses:
        print(f"ID: {e['ID']}, 描述: {e['Description']}, 金额: {e['Amount']}, 日期: {e['Date']}")
    print("-" * 40)

def summary():
    expenses = load_expense()
    all_expense = 0
    item_num = len(expenses)
    for e in expenses:
        all_expense += e["Amount"]
    print(f"总条数: {item_num}")
    print(f"总金额: {all_expense}")

def summary_by_month(month):
    expenses = load_expense()
    month_total = 0
    count = 0

    month = str(month).zfill(2)

    for e in expenses:
        date = e["Date"]
        exp_month = date[5:7]
        if exp_month == month:
            month_total += e["Amount"]
            count += 1
    print(f"{month}月总条数: {count}")
    print(f"{month}月总金额: {month_total}")

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("description", type=str, help="Description of the expense")
    add_parser.add_argument("amount", type=float, help="Amount of the expense")

    list_parser = subparsers.add_parser("list", help= "List all expense")

    delete_parser = subparsers.add_parser("delete", help="Delete the specified expense")
    delete_parser.add_argument("id", type=int, help="ID of the expense")

    update_parser = subparsers.add_parser("update", help="Update the specified expense")
    update_parser.add_argument("id", type=int, help="ID of the expense")
    update_parser.add_argument("description", type=str, help="Description of the expense")
    update_parser.add_argument("amount", type=float, help="Amount of the expense")

    summary_parser = subparsers.add_parser("summary", help="Summary the expenses")
    summary_parser.add_argument("month", nargs="?", help="Month of expense")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "list":
        list_expenses()
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount)
    elif args.command == "summary":
        if args.month:
            summary_by_month(args.month)
        else:
            summary()

if __name__ == "__main__":
    main()