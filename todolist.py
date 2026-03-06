import json
import os
from typing import List, Dict, Optional


class TodoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_data()

    # --- PERSISTENCE LOGIC ---
    def save_data(self):
        """Complexity: O(n) - Writes the current list to the JSON file."""
        with open(self.filename, "w") as f:
            json.dump({"tasks": self.tasks, "next_id": self.next_id}, f, indent=4)

    def load_data(self):
        """Complexity: O(n) - Reads data from the JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = data["tasks"]
                self.next_id = data["next_id"]
        else:
            self.tasks = [
                {"id": 1, "title": "Buy groceries", "priority": 1, "due_date": "2024-12-18", "status": "pending"},
                {"id": 2, "title": "Finish report", "priority": 1, "due_date": "2024-12-19", "status": "in_progress"},
                {"id": 3, "title": "Call dentist", "priority": 2, "due_date": "2024-12-20", "status": "pending"},
                {"id": 4, "title": "Read book", "priority": 3, "due_date": "2024-12-25", "status": "pending"},
                {"id": 5, "title": "Exercise", "priority": 2, "due_date": "2024-12-17", "status": "completed"}
            ]
            self.next_id = 6
            self.save_data()

    # --- CORE OPERATIONS ---
    def add_task(self, title: str, priority: int, due_date: str):
        task = {"id": self.next_id, "title": title, "priority": priority, "due_date": due_date, "status": "pending"}
        self.tasks.append(task)
        self.next_id += 1
        self.save_data()

    def delete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            self.save_data()
            return removed
        return None

    def update_task(self, index: int, key: str, value: any):
        """
        Complexity: O(1) for access.
        Prevents modification of ID to maintain data integrity.
        """
        if key.lower() in ['id', 'index']:
            print("Error: Identification fields cannot be modified.")
            return False

        if 0 <= index < len(self.tasks) and key in self.tasks[index]:
            # Type conversion for priority
            if key == 'priority':
                value = int(value)
            self.tasks[index][key] = value
            self.save_data()
            return True
        return False

    # --- ADVANCED ALGORITHMS ---

    def merge_sort(self, arr: List[Dict], primary: str, secondary: str) -> List[Dict]:
        """Stable Merge Sort: O(n log n)"""
        if len(arr) <= 1: return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid], primary, secondary)
        right = self.merge_sort(arr[mid:], primary, secondary)
        return self._merge(left, right, primary, secondary)

    def _merge(self, left, right, p, s):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            # Primary sort check, then secondary tie-breaker
            if left[i][p] < right[j][p] or (left[i][p] == right[j][p] and left[i][s] <= right[j][s]):
                result.append(left[i]);
                i += 1
            else:
                result.append(right[j]);
                j += 1
        result.extend(left[i:]);
        result.extend(right[j:])
        return result

    def binary_search_id(self, target_id: int) -> Optional[Dict]:
        """Binary Search: O(log n)"""
        temp_list = sorted(self.tasks, key=lambda x: x['id'])
        low, high = 0, len(temp_list) - 1
        while low <= high:
            mid = (low + high) // 2
            if temp_list[mid]['id'] == target_id:
                return temp_list[mid]
            elif temp_list[mid]['id'] < target_id:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def filter_tasks(self, attr: str, value: str):
        """Linear Search: O(n)"""
        return [t for t in self.tasks if str(t.get(attr, "")).lower() == value.lower()]

    def display(self, data=None):
        data = data if data is not None else self.tasks
        print(f"{'Idx':<4} | {'ID':<3} | {'Title':<15} | {'Pri':<3} | {'Due':<11} | {'Status'}")
        print("-" * 65)
        for i, t in enumerate(data):
            print(
                f"{i:<4} | {t['id']:<3} | {t['title']:<15} | {t['priority']:<3} | {t['due_date']:<11} | {t['status']}")


# --- MAIN INTERFACE ---
def main():
    todo = TodoList()
    while True:
        print("\n--- Project Task Manager (Auto-Save Enabled) ---")
        todo.display()
        print("\n1. Add Task | 2. Delete | 3. Update | 4. Sort | 5. Filter | 6. Search ID | 7. Exit")
        c = input("Selection: ")

        try:
            if c == '1':
                todo.add_task(input("Title: "), int(input("Priority (1-3): ")), input("Due Date (YYYY-MM-DD): "))

            elif c == '2':
                todo.delete_task(int(input("Index to delete: ")))

            elif c == '3':
                idx = int(input("Index: "))
                k = input("Field to update (title/priority/due_date/status): ")
                v = input("New Value: ")
                todo.update_task(idx, k, v)

            elif c == '4':
                print("1. Sort by Priority (Main) | 2. Sort by Due Date (Main)")
                sc = input("Choice: ")
                if sc == '1':
                    todo.tasks = todo.merge_sort(todo.tasks, "priority", "due_date")
                else:
                    todo.tasks = todo.merge_sort(todo.tasks, "due_date", "priority")
                todo.save_data()
                print("Tasks sorted.")

            elif c == '5':
                attr = input("Filter by (status/priority): ")
                val = input("Value: ")
                todo.display(todo.filter_tasks(attr, val))

            elif c == '6':
                tid = int(input("Search ID: "))
                res = todo.binary_search_id(tid)
                print(f"Result: {res}" if res else "Not found.")

            elif c == '7':
                break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()